"""
Roster Registry — single source of truth for the app's working roster
and per-roster lifecycle state.

Owned by AppState. Subscribed to by the picker, sidebar, save manager,
tracker bridge — every place that needs to ask "what roster is this app
operating on?" or "is roster X stale?" so the answer comes from one
place instead of being inferred per call site via string literals or
tracker memory reads.

Design rule: there is **no default working roster**. The working roster
is set only by entering a mode tab whose mode_key has an entry in
MODE_ROSTER_MAP. Modes without a mapping (Radio, Tournaments, Settings)
leave working_roster unchanged when entered. If the registry has never
seen a mapped mode, working_roster is None and consumers must handle
that case (typically: empty pool / disabled features / friendly notice).
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QObject, Signal

from spritopia.data_storage.data_storage import d
from spritopia.common.logger import log


# Mode tab key -> roster name. Modes not listed here intentionally don't
# trigger a working-roster change on entry.
MODE_ROSTER_MAP: dict[str, str] = {
    "premier":  "Premier",
    "gauntlet": "Gauntlet",
    "league":   "League",
}


@dataclass
class RosterEntry:
    name: str
    imported: bool = False
    marked_stale: bool = False              # True if .ROS was rewritten since 2K last loaded
    last_synced_at: Optional[datetime] = None
    last_loaded_in_2k_at: Optional[datetime] = None


class RosterRegistry(QObject):
    """
    Tracks the active working roster and per-roster lifecycle state.

    Signals:
        working_roster_changed(object) — fires when working roster is set/cleared.
            Argument is str (roster name) or None.
        entry_changed(str) — fires when a single entry's lifecycle state mutates.
            Argument is the roster name. Useful for HUD/banner refresh.
    """
    working_roster_changed = Signal(object)   # str | None
    entry_changed = Signal(str)               # roster name

    def __init__(self, parent=None):
        super().__init__(parent)
        self._working_roster: Optional[str] = None
        self._entries: dict[str, RosterEntry] = {}

    # ── Working roster ───────────────────────────────────────────────────────

    @property
    def working_roster(self) -> Optional[str]:
        return self._working_roster

    def set_working_roster(self, name: Optional[str]) -> None:
        """Set the working roster directly. Eagerly imports the roster's CSVs.

        Pass None to clear (no current mode). Raises ValueError if the named
        roster has no CSVs on disk — caller is expected to surface this
        appropriately (e.g. via a dialog or status message).
        """
        if name == self._working_roster:
            return
        if name is not None:
            self._ensure_imported(name)
        self._working_roster = name
        log.info(f"Working roster set to {name!r}")
        self.working_roster_changed.emit(name)

    def set_working_roster_for_mode(self, mode_key: str) -> None:
        """Translate a mode tab key to its roster mapping and apply it.

        Modes without a mapping (Radio, Tournaments, Settings) leave the
        working roster unchanged — they intentionally don't have one.
        """
        mapped = MODE_ROSTER_MAP.get(mode_key)
        if mapped is None:
            log.debug(
                f"Mode '{mode_key}' has no roster mapping; "
                f"working_roster left as {self._working_roster!r}."
            )
            return
        self.set_working_roster(mapped)

    # ── Per-roster lifecycle ─────────────────────────────────────────────────

    def get_entry(self, name: str) -> RosterEntry:
        if name not in self._entries:
            self._entries[name] = RosterEntry(name=name)
        return self._entries[name]

    def is_imported(self, name: str) -> bool:
        return name in self._entries and self._entries[name].imported

    def is_stale(self, name: str) -> bool:
        return name in self._entries and self._entries[name].marked_stale

    def mark_synced(self, name: str) -> None:
        """Record that we just rewrote roster `name`'s .ROS via RedMC. 2K's
        in-memory copy is now stale until the user reloads it."""
        entry = self.get_entry(name)
        entry.last_synced_at = datetime.now()
        entry.marked_stale = True
        log.info(f"Roster '{name}' marked stale (just synced to .ROS via RedMC)")
        self.entry_changed.emit(name)

    def mark_loaded_in_2k(self, name: str) -> None:
        """Record that 2K just (re)loaded the roster. Clears any stale flag."""
        entry = self.get_entry(name)
        entry.last_loaded_in_2k_at = datetime.now()
        if entry.marked_stale:
            entry.marked_stale = False
            log.info(f"Roster '{name}' freshness restored (2K reload observed)")
        self.entry_changed.emit(name)

    # ── Import lifecycle ─────────────────────────────────────────────────────

    def ensure_imported(self, name: str) -> None:
        """Idempotent CSV import. Raises ValueError if no CSVs on disk."""
        self._ensure_imported(name)

    def _ensure_imported(self, name: str) -> None:
        entry = self.get_entry(name)
        if entry.imported and name in d.rosters:
            return
        if name not in d.csv_GetSavedRosterList():
            raise ValueError(f"Roster '{name}' has no CSVs in save/roster_csvs/.")
        d.csv_ImportCSVs(name)
        entry.imported = True
        log.info(f"Eagerly imported roster '{name}' into d.rosters[]")
        self.entry_changed.emit(name)
