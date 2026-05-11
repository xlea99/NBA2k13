"""
CAP Sync Coordinator — incoming face/CAP data sync from 2K13 .ROS into Players.db.

The "incoming" half of the two-direction sync problem (the "outgoing" half — pushing
new players from Players.db to a .ROS — lives in create_player_page.py).

Workflow this implements ("Option A — brutal but bulletproof"):
  1. Tracker watches 2K13's current screen.
  2. Whenever the user enters the CreatePlayer screen, mark the active roster as
     "dirty" — i.e. the .ROS may now contain face data that's newer than Players.db.
     We queue an IMPORT_CAP_INFO_FROM_ROSTER change to the save_manager so the
     glowing Save button reminds the user.
  3. The user must press "Save Roster" inside 2K (we detect that screen too) to
     confirm the .ROS on disk is fresh. Without that, an import would happily wipe
     the in-game edits by re-extracting a stale .ROS.
  4. When the user clicks Save in the GUI, the queued change runs:
        backup Players.db → RedMC import (.ROS → CSVs → memory) →
        copy CAP/headshape fields per-player → upload Players.db → clear dirty state.
     If the user never pressed Save Roster in 2K, the change refuses and a
     dialog tells them why. The save_manager's existing error-surfacing wires
     this into a QMessageBox automatically.
"""

import shutil
import datetime
from pathlib import Path

from PySide6.QtCore import QObject

from spritopia.gui.app_state import get_app_state
from spritopia.gui.save_manager import (
    get_save_manager, ChangeType, PendingChange,
)
from spritopia.gui.tracker_bridge import get_tracker_bridge
from spritopia.data_storage.data_storage import d
from spritopia.data_storage.roster_io import importRosterData
from spritopia.common.logger import log
from spritopia.common.paths import paths


def _import_group_id(roster_name: str) -> str:
    """Stable group_id so we don't double-queue the same import."""
    return f"import_cap:{roster_name}"


def _backup_players_db():
    """Copy Players.db to save/backups/PlayerData/ with a timestamp suffix.

    The shared utilities/backup.py helper is currently broken (calls a nonexistent
    `Paths.validatePath` method), so we inline a minimal version here. Keeps a
    rolling 20 backups, oldest pruned automatically.
    """
    src = paths["saveDBs"] / "Players.db"
    if not src.exists():
        log.warning("Players.db not found at expected path; skipping backup.")
        return
    backup_dir: Path = paths["backups"] / "PlayerData"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
    dest = backup_dir / f"Players_{timestamp}.db"
    shutil.copy(src, dest)

    # Prune to 20 most recent
    existing = sorted(
        [f for f in backup_dir.iterdir() if f.name.startswith("Players_") and f.suffix == ".db"],
        key=lambda f: f.stat().st_mtime,
    )
    while len(existing) > 20:
        existing.pop(0).unlink()


class CAPSyncCoordinator(QObject):
    """
    Watches tracker location signals and translates them into app_state mutations
    + save_manager queue updates for incoming CAP imports.

    Owned by MainWindow; created after the tracker bridge initializes successfully.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bridge = get_tracker_bridge()
        self._app_state = get_app_state()
        self._save_manager = get_save_manager()

        self._bridge.location_changed.connect(self._on_location_changed)
        log.info("CAPSyncCoordinator listening for tracker location changes")

    # ── Tracker → state machine ───────────────────────────────────────────────

    def _on_location_changed(self, location: str):
        roster_name = self._bridge.get_active_roster()
        if not roster_name:
            return

        if location == "CreatePlayer":
            self._on_create_player_visited(roster_name)
        elif location == "SaveRoster":
            self._on_save_roster_visited(roster_name)

    def _on_create_player_visited(self, roster_name: str):
        # Mark dirty (idempotent in app_state). Visiting again after a 2K save also
        # invalidates the saved-since-dirty flag, since the user is presumed to be
        # editing again.
        self._app_state.mark_roster_dirty(roster_name)

        # Queue exactly one import change per roster, no matter how many times the
        # user pops in/out of CreatePlayer.
        gid = _import_group_id(roster_name)
        if not self._save_manager.has_change_with_group_id(gid):
            change = PendingChange(
                change_type=ChangeType.IMPORT_CAP_INFO_FROM_ROSTER,
                description=f"Import CAP/face edits from {roster_name}.ROS into Players.db",
                data={"roster_name": roster_name},
                execute_fn=self._execute_import_cap_info,
                group_id=gid,
            )
            self._save_manager.add_change(change)
            log.info(f"Queued CAP import for roster '{roster_name}' (CreatePlayer screen detected)")

    def _on_save_roster_visited(self, roster_name: str):
        self._app_state.mark_roster_saved_in_2k(roster_name)

    # ── Save-manager execute_fn ───────────────────────────────────────────────

    def _execute_import_cap_info(self, data: dict):
        """Run the actual incoming sync. Raises on guard failure or RedMC error
        — the save_manager catches and surfaces via SaveButton's QMessageBox."""
        roster_name = data["roster_name"]

        # Hard guard — the .ROS on disk MUST be the post-edit version, otherwise
        # we'll re-extract stale data and overwrite Players.db with the OLD faces.
        if not self._app_state.is_roster_safe_to_import(roster_name):
            raise RuntimeError(
                f"Cannot import CAP info from '{roster_name}.ROS' — you have not "
                f"saved the roster inside 2K13 since visiting Create-A-Player. "
                f"Open 2K13's 'Save Roster' menu to confirm your face edits are "
                f"on disk, then click Save again."
            )

        log.info(f"Beginning CAP info import for roster '{roster_name}'")

        # 1. Snapshot Players.db before we touch it.
        _backup_players_db()

        # 2. RedMC pull: .ROS → CSVs → memory.
        importRosterData(roster_name, d)

        # 3. Copy CAP+headshape columns per active SpriteID. commit=False so we
        # don't run a full DB upload after every player; we batch one upload after.
        sprite_ids = d.rosters[roster_name].get("SpriteIDs", {}).values()
        synced = 0
        for sprite_id in sprite_ids:
            if sprite_id is None or sprite_id < 0:
                continue
            if sprite_id not in d.players:
                # Roster references a SpriteID that's not in Players.db — skip
                # rather than crash. Logged for visibility.
                log.warning(
                    f"Roster '{roster_name}' references SpriteID {sprite_id} "
                    f"which is not in Players.db; skipping CAP sync for it."
                )
                continue
            d.updatePlayerCAPInfoFromRoster(roster_name, sprite_id, commit=False)
            synced += 1

        # 4. One upload to flush all dirty Player rows.
        d.playersDB_UploadPlayers()

        # 5. Clear dirty state so Save Button stops glowing for this roster.
        self._app_state.clear_roster_dirty(roster_name)

        # 6. We just re-extracted CSVs from the .ROS that 2K currently has
        # loaded — so our in-memory state matches 2K's. Mark the roster as
        # "loaded in 2K" to clear any prior staleness on the registry side.
        self._app_state.roster_registry.mark_loaded_in_2k(roster_name)

        log.info(f"CAP info import complete for '{roster_name}' — synced {synced} players.")
