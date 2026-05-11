"""
Thin Qt bridge between the tracker daemon thread and the PySide6 GUI.

Polls tracker state on a QTimer and emits Qt Signals on state transitions.
All hard logic lives in tracker.py — this file only translates thread state
into signal-based reactivity for the GUI layer.
"""

import copy
from PySide6.QtCore import QObject, Signal, QTimer
from spritopia.common.logger import log


# Lazy import: tracker auto-starts on import, so we defer until first use.
_tracker = None
_data_storage = None

def _get_tracker():
    global _tracker
    if _tracker is None:
        from spritopia.interface.tracker import t
        _tracker = t
    return _tracker

def _get_ds():
    global _data_storage
    if _data_storage is None:
        from spritopia.data_storage.data_storage import d
        _data_storage = d
    return _data_storage


class TrackerBridge(QObject):

    # Signals
    connection_changed   = Signal(bool)    # True = connected to nba2k13.exe
    location_changed     = Signal(str)     # "Home", "PickUp", "InGame", "Disconnected", etc.
    game_status_changed  = Signal(str)     # "OutOfGame", "Running", "Paused", "Won"
    active_roster_changed = Signal(object) # roster name (str without .ROS suffix) or None
    roster_loaded_in_2k  = Signal(object)  # fires on LoadRoster screen exit — payload is the
                                           # roster name (str) that's now active, or None.
    live_stats           = Signal(dict)    # periodic stat snapshot during live game (deep-copied)
    game_won             = Signal(dict)    # final ripped stats dict (deep-copied)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Previous state for diff detection
        self._prev_connected = False
        self._prev_location = "Disconnected"
        self._prev_game_status = "OutOfGame"
        self._prev_active_roster = None
        self._prev_game_count = 0
        self._won_emitted_for_game = -1
        self._last_rip_tick = -1   # tracker tick of last emitted live stats

        # Poll timer
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(300)
        self._poll_timer.timeout.connect(self._poll)
        self._poll_timer.start()

        log.info("TrackerBridge initialized (300ms poll)")

    def _poll(self):
        """Read tracker state and emit signals on changes."""
        try:
            tracker = _get_tracker()
        except Exception:
            # Tracker not available (pymem not installed, etc.)
            if self._prev_connected:
                self._prev_connected = False
                self.connection_changed.emit(False)
            if self._prev_active_roster is not None:
                self._prev_active_roster = None
                self.active_roster_changed.emit(None)
            return

        # Snapshot under lock
        with tracker.lock:
            connected = tracker.mem is not None
            location = tracker.location
            game_status = tracker.gameStatus
            game_count = tracker.gameCount
            have_final = tracker.haveFinalStatsBeenRipped
            ripped = tracker.rippedGames.get(game_count)
            tick = tracker.tick

        # Did the user just exit the LoadRoster screen? This is our cue that 2K
        # finished (re)loading a roster from disk — used to clear staleness flags.
        load_roster_exit = (
            connected
            and self._prev_location == "LoadRoster"
            and location != "LoadRoster"
        )

        # Emit on changes
        if connected != self._prev_connected:
            self._prev_connected = connected
            self.connection_changed.emit(connected)

        if location != self._prev_location:
            self._prev_location = location
            self.location_changed.emit(location)

        if game_status != self._prev_game_status:
            self._prev_game_status = game_status
            self.game_status_changed.emit(game_status)

        # Active roster — read outside the lock since it does a memory access. The
        # public wrapper handles ERROR/UNOPENED/NONE → None for us.
        roster_name = self.get_active_roster() if connected else None
        if roster_name != self._prev_active_roster:
            self._prev_active_roster = roster_name
            self.active_roster_changed.emit(roster_name)

        # Emit AFTER roster_name has been settled — when the user reloads the
        # SAME roster, active_roster_changed won't fire (no diff), but we still
        # need to clear the staleness flag on the registry side. This signal
        # always fires on LoadRoster exit regardless of name change.
        if load_roster_exit:
            self.roster_loaded_in_2k.emit(roster_name)

        # Live stats: emit periodic snapshots during active games
        if (ripped is not None
                and not ripped.get("Final")
                and game_status in ("Running", "Paused")
                and tick != self._last_rip_tick):
            self._last_rip_tick = tick
            self.live_stats.emit(copy.deepcopy(ripped))

        # Game won: emit once per game when final stats are ready
        if (game_status == "Won"
                and have_final
                and ripped is not None
                and ripped.get("Final") is True
                and self._won_emitted_for_game != game_count):
            self._won_emitted_for_game = game_count
            stats_copy = copy.deepcopy(ripped)
            self.game_won.emit(stats_copy)

    # ── Public API ────────────────────────────────────────────────────────────

    def load_players(self, team1, team2):
        """
        Load picked players into 2K13's blacktop picker.

        Args:
            team1: list of player dicts (Ballerz, slots 0..N-1)
            team2: list of player dicts (Ringers, slots 5..5+N-1)

        Returns:
            dict with keys: success (bool), error (str|None),
                            loaded_count (int), warnings (list[str])
        """
        result = {"success": False, "error": None, "loaded_count": 0, "warnings": []}

        try:
            tracker = _get_tracker()
        except Exception as e:
            result["error"] = f"Tracker not available: {e}"
            return result

        # Check connection
        if tracker.mem is None:
            result["error"] = "NBA 2K13 is not running or not connected."
            return result

        # Check screen
        if tracker.location != "PickUp":
            result["error"] = (
                f"2K13 must be on the Pick Up screen to load players. "
                f"Current screen: {tracker.location}"
            )
            return result

        # Get active roster
        active_roster = tracker.getActiveRoster()
        if active_roster is None:
            result["error"] = "No roster is currently loaded in 2K13."
            return result
        roster_name = active_roster.split(".ROS")[0]

        d = _get_ds()

        # Check roster is imported
        if roster_name not in d.rosters:
            result["error"] = f"Roster '{roster_name}' is not imported in data storage."
            return result

        # Working-roster + freshness gates — refuse if app's working roster
        # doesn't match 2K's loaded roster, or if 2K's copy is stale relative
        # to disk. Either case would silently write the wrong RosterIDs to
        # 2K's slot memory, corrupting the in-game picker.
        try:
            from spritopia.gui.app_state import get_app_state
            registry = get_app_state().roster_registry
            working = registry.working_roster

            if working is not None and working != roster_name:
                result["error"] = (
                    f"App is operating on '{working}' but 2K has '{roster_name}' "
                    f"loaded. Load '{working}' in 2K (Esc → Load Roster) and try again."
                )
                return result

            if registry.is_stale(roster_name):
                result["error"] = (
                    f"'{roster_name}' was modified since 2K last loaded it. "
                    f"2K's in-memory copy is stale — RosterIDs would be wrong. "
                    f"Reload '{roster_name}' in 2K (Esc → Load Roster) and try again."
                )
                return result
        except Exception as e:
            # Registry not available — fall back to existing behavior rather
            # than block on a probe failure.
            log.warning(f"Working-roster validation skipped: {e}")

        # Build slot dict: Ballerz = 0..N-1, Ringers = 5..5+N-1
        slot_dict = {}

        for i, player in enumerate(team1):
            sprite_id = player["SpriteID"]
            roster_id = d.csv_GetRosterIDFromSpriteID(roster_name, sprite_id)
            if roster_id is None:
                name = f"{player.get('First_Name', '?')} {player.get('Last_Name', '?')}"
                result["warnings"].append(
                    f"{name} (SpriteID={sprite_id}) not found on roster '{roster_name}'"
                )
            else:
                slot_dict[i] = roster_id

        for i, player in enumerate(team2):
            sprite_id = player["SpriteID"]
            roster_id = d.csv_GetRosterIDFromSpriteID(roster_name, sprite_id)
            if roster_id is None:
                name = f"{player.get('First_Name', '?')} {player.get('Last_Name', '?')}"
                result["warnings"].append(
                    f"{name} (SpriteID={sprite_id}) not found on roster '{roster_name}'"
                )
            else:
                slot_dict[5 + i] = roster_id

        if not slot_dict:
            result["error"] = "No players could be mapped to roster IDs."
            return result

        # Write to 2K13 memory
        try:
            tracker.loadBlacktopPlayers(slot_dict)
            result["success"] = True
            result["loaded_count"] = len(slot_dict)
            log.info(f"Loaded {len(slot_dict)} players into 2K13 blacktop: {slot_dict}")
        except Exception as e:
            result["error"] = f"Failed to write players to 2K13 memory: {e}"
            log.exception(result["error"])

        return result

    def is_connected(self):
        try:
            return _get_tracker().mem is not None
        except Exception:
            return False

    def get_location(self):
        try:
            return _get_tracker().location
        except Exception:
            return "Disconnected"

    def get_game_status(self):
        try:
            return _get_tracker().gameStatus
        except Exception:
            return "OutOfGame"

    def get_active_roster(self):
        """Return the active roster name (without .ROS suffix) or None if unknown."""
        try:
            raw = _get_tracker().getActiveRoster()
        except Exception:
            return None
        if not raw or raw in ("UNOPENED", "NONE", "ERROR", "None"):
            return None
        return raw.split(".ROS")[0]


# ── Singleton ─────────────────────────────────────────────────────────────────

_bridge_instance = None

def get_tracker_bridge():
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = TrackerBridge()
    return _bridge_instance
