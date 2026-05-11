"""
Roster Manager — view/manage rosters and the Players.db catalog.

Phase 1 scope:
  • Roster selector (drop-down of all rosters in save/roster_csvs/) + reload
  • Two-pane layout: Players.db (left, read-only) | Active Roster (right)
  • Add player → roster (queues ADD_PLAYER_TO_ROSTER + SYNC_ROSTER_TO_ROS via save_manager)
  • Remove player from roster (queues REMOVE_PLAYER_FROM_ROSTER + SYNC_ROSTER_TO_ROS)
  • Import an existing .ROS that hasn't been imported yet (RedMC pull → CSVs)
  • Create a brand new roster from data/templates/BlankRosterTemplate.ROS

Out of scope (Phase 2+): Players.db edit mode, delete player from DB.
"""

import shutil
from pathlib import Path
from typing import Optional, List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QFrame, QMessageBox, QInputDialog,
)

from spritopia.gui.theme import COLORS
from spritopia.gui.widgets.player_list_view import PlayerListView, PlayerListEntry
from spritopia.gui.save_manager import (
    get_save_manager, ChangeType, PendingChange,
)
from spritopia.gui.app_state import get_app_state
from spritopia.data_storage.data_storage import d
from spritopia.data_storage.roster_io import importRosterData, exportRosterData
from spritopia.common.logger import log
from spritopia.common.paths import paths


_BLANK_ROSTER_TEMPLATE = "BlankRosterTemplate.ROS"


class RosterManagerWidget(QWidget):
    """Top-level roster + Players.db management screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._app_state = get_app_state()
        self._save_manager = get_save_manager()
        self._active_roster: Optional[str] = None
        self._setup_ui()
        # Populate the left pane once — it doesn't depend on the selected
        # roster, so subsequent roster-swap calls skip this expensive rebuild.
        self._refresh_players_view()
        self._refresh_roster_list()

        # Refresh the right pane when save state changes (e.g. user clicked Save
        # and the in-memory rosters got mutated by execute_fns).
        self._save_manager.save_completed.connect(self._refresh_roster_view)
        # Also refresh on every queue mutation — that's how the pending-add /
        # pending-remove visual overlay stays in sync with the save_manager.
        self._save_manager.changes_updated.connect(self._refresh_roster_view)
        # Refresh both panes when the global player list updates (e.g. new player
        # generated via Create-A-Player).
        self._app_state.player_list_changed.connect(self._refresh_players_view)
        # When the app's working roster changes (mode switch), auto-follow it
        # in the target dropdown so the manager's default view matches the
        # mode the user is in. User can still manually pick a different target
        # afterward — the divergence notice then explains the disconnect.
        self._app_state.roster_registry.working_roster_changed.connect(
            self._on_working_roster_changed
        )

    # ── UI setup ──────────────────────────────────────────────────────────────

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(12)

        # Body — three columns. Each column owns its own header(s) so the lists
        # can fill all the height not used by their column-local headers.
        body = QHBoxLayout()
        body.setSpacing(14)

        # ── Left column: Players DB Manager ───────────────────────────────────
        left_col = QVBoxLayout()
        left_col.setSpacing(6)

        left_title = QLabel("Players DB Manager")
        left_title.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLORS['text_primary']};"
        )
        left_col.addWidget(left_title)

        left_sub = QLabel("Read-only catalog of every Player.")
        left_sub.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        left_sub.setWordWrap(True)
        left_col.addWidget(left_sub)

        self._players_view = PlayerListView(
            show_id_column=True,
            id_header="SID",
            placeholder="Search players…",
        )
        self._players_view.entry_double_clicked.connect(self._on_add_clicked)
        left_col.addWidget(self._players_view, stretch=1)

        body.addLayout(left_col, stretch=1)

        # ── Center action column ──────────────────────────────────────────────
        center_col = QVBoxLayout()
        center_col.setSpacing(8)
        center_col.addStretch()
        self._add_btn = self._make_button("Add  →", primary=True)
        self._add_btn.clicked.connect(self._on_add_clicked)
        center_col.addWidget(self._add_btn)
        self._remove_btn = self._make_button("←  Remove", primary=False)
        self._remove_btn.clicked.connect(self._on_remove_clicked)
        center_col.addWidget(self._remove_btn)
        center_col.addStretch()
        body.addLayout(center_col)

        # ── Right column: Roster Manager (title + toolbar + list) ─────────────
        right_col = QVBoxLayout()
        right_col.setSpacing(6)

        right_title = QLabel("Roster Manager")
        right_title.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLORS['text_primary']};"
        )
        right_col.addWidget(right_title)

        right_sub = QLabel(
            "Edit the active roster's player list. "
            "Changes queue to the Save button — nothing is written to disk until you click Save."
        )
        right_sub.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        right_sub.setWordWrap(True)
        right_col.addWidget(right_sub)

        # Toolbar: roster dropdown + actions
        toolbar = QFrame()
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)
        tb_lo = QHBoxLayout(toolbar)
        tb_lo.setContentsMargins(14, 10, 14, 10)
        tb_lo.setSpacing(10)

        tb_lo.addWidget(self._field_label("Active Roster:"))

        self._roster_combo = QComboBox()
        self._roster_combo.setMinimumWidth(180)
        self._roster_combo.setStyleSheet(self._combo_style())
        self._roster_combo.currentTextChanged.connect(self._on_roster_selected)
        tb_lo.addWidget(self._roster_combo)

        self._reload_btn = self._make_button("Reload", primary=False)
        self._reload_btn.clicked.connect(self._on_reload_clicked)
        tb_lo.addWidget(self._reload_btn)

        tb_lo.addStretch()

        self._new_btn = self._make_button("New Roster", primary=True)
        self._new_btn.clicked.connect(self._on_new_clicked)
        tb_lo.addWidget(self._new_btn)

        right_col.addWidget(toolbar)

        # Divergence notice — appears when target roster ≠ app's working roster.
        # Editing a non-working roster is legitimate, but the user should know
        # the changes won't be playable until they switch modes.
        self._divergence_lbl = QLabel("")
        self._divergence_lbl.setStyleSheet(
            f"font-size: 11px; color: {COLORS['accent_warning']}; "
            f"padding: 4px 8px; background-color: {COLORS['bg_medium']}; "
            f"border-left: 3px solid {COLORS['accent_warning']}; border-radius: 2px;"
        )
        self._divergence_lbl.setWordWrap(True)
        self._divergence_lbl.setVisible(False)
        right_col.addWidget(self._divergence_lbl)

        # Roster list
        self._roster_pane_header = self._pane_header("ROSTER", "—")
        right_col.addWidget(self._roster_pane_header)
        self._roster_view = PlayerListView(
            show_id_column=True,
            id_header="RID",
            placeholder="Filter roster…",
        )
        self._roster_view.entry_double_clicked.connect(self._on_remove_clicked)
        right_col.addWidget(self._roster_view, stretch=1)

        body.addLayout(right_col, stretch=1)

        outer.addLayout(body, stretch=1)

        # Bottom status
        self._status_lbl = QLabel("")
        self._status_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        outer.addWidget(self._status_lbl)

    # ── Style helpers ─────────────────────────────────────────────────────────

    @staticmethod
    def _field_label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        return lbl

    @staticmethod
    def _pane_header(title: str, subtitle: str) -> QWidget:
        wrap = QWidget()
        lo = QVBoxLayout(wrap)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {COLORS['text_muted']}; "
            f"letter-spacing: 1px;"
        )
        lo.addWidget(title_lbl)
        sub_lbl = QLabel(subtitle)
        sub_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        sub_lbl.setObjectName("subtitle")
        lo.addWidget(sub_lbl)
        return wrap

    @staticmethod
    def _combo_style() -> str:
        return f"""
            QComboBox {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                color: {COLORS['text_primary']};
            }}
            QComboBox:hover {{ border-color: {COLORS['accent_primary']}; }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                selection-background-color: {COLORS['accent_primary']};
            }}
        """

    @staticmethod
    def _make_button(text: str, primary: bool) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        if primary:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_primary']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 16px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: #1d6fb8; }}
                QPushButton:disabled {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_muted']};
                }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['text_secondary']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 4px;
                    padding: 0 14px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    color: {COLORS['text_primary']};
                    border-color: {COLORS['text_muted']};
                }}
                QPushButton:disabled {{
                    color: {COLORS['text_muted']};
                    border-color: {COLORS['border_dark']};
                }}
            """)
        return btn

    # ── Roster lifecycle ──────────────────────────────────────────────────────

    def _refresh_roster_list(self):
        """Rebuild the roster dropdown from save/roster_csvs/ + currently-loaded rosters.

        On initial population (no prior selection), defaults to the app's working
        roster if available — so opening Manage Data while in Premier mode
        auto-targets Premier rather than whatever sorts alphabetically first.
        """
        on_disk = set(d.csv_GetSavedRosterList())
        in_memory = set(d.rosters.keys())
        all_rosters = sorted(on_disk | in_memory)

        # Preserve current selection if it still exists; otherwise prefer the
        # working roster.
        previous = self._roster_combo.currentText()
        if not previous:
            working = self._app_state.roster_registry.working_roster
            if working and working in all_rosters:
                previous = working

        self._roster_combo.blockSignals(True)
        self._roster_combo.clear()
        if not all_rosters:
            self._roster_combo.addItem("(no rosters available)")
            self._roster_combo.setEnabled(False)
        else:
            self._roster_combo.setEnabled(True)
            self._roster_combo.addItems(all_rosters)
            if previous in all_rosters:
                self._roster_combo.setCurrentText(previous)
        self._roster_combo.blockSignals(False)

        if all_rosters:
            self._on_roster_selected(self._roster_combo.currentText())

    def _on_roster_selected(self, name: str):
        if not name or name.startswith("("):
            self._active_roster = None
            self._roster_view.set_entries([])
            self._set_pane_subtitle("—")
            self._players_view.set_entries([])
            return

        self._active_roster = name

        # Lazily import the roster CSVs into memory if not already loaded.
        if name not in d.rosters:
            try:
                d.csv_ImportCSVs(name)
                self._set_status(f"Loaded roster '{name}' from disk.", muted=True)
            except Exception as e:
                log.exception(f"Failed to load roster '{name}': {e}")
                QMessageBox.warning(
                    self, "Roster Load Failed",
                    f"Couldn't load CSVs for roster '{name}':\n\n{e}"
                )
                return

        # NOTE: we do NOT refresh the players pane here. Players.db is independent
        # of which roster is selected — refreshing it on every combo swap is
        # wasteful (rebuilding ~200 rows in QTableWidget isn't free). Players
        # view only needs to refresh on init + player_list_changed.
        self._refresh_roster_view()
        self._refresh_divergence_notice()

    def _on_working_roster_changed(self, new_working):
        """Auto-switch the target dropdown to the new working roster.

        The combo selection change triggers _on_roster_selected, which in turn
        calls _refresh_divergence_notice. If the new working roster isn't in
        the dropdown (no CSVs on disk), leave the combo where it is and just
        refresh the notice — it'll show the divergence.
        """
        if new_working:
            idx = self._roster_combo.findText(new_working)
            if idx >= 0 and self._roster_combo.currentText() != new_working:
                self._roster_combo.setCurrentText(new_working)
                return  # _on_roster_selected fires and refreshes everything
        self._refresh_divergence_notice()

    def _refresh_divergence_notice(self, *_):
        """Show a notice when the target roster ≠ app's working roster.

        Editing a non-working roster is legitimate (e.g. preparing Gauntlet
        while playing Premier), but the user should know their changes won't
        be playable until they switch modes.
        """
        if self._active_roster is None:
            self._divergence_lbl.setVisible(False)
            return
        working = self._app_state.roster_registry.working_roster
        if working is None or working == self._active_roster:
            self._divergence_lbl.setVisible(False)
            return
        self._divergence_lbl.setText(
            f"Editing <b>{self._active_roster}</b>, but the app is operating on "
            f"<b>{working}</b>. Saves will update <b>{self._active_roster}.ROS</b> "
            f"on disk; switch modes to play with these changes."
        )
        self._divergence_lbl.setVisible(True)

    def _on_reload_clicked(self):
        if not self._active_roster:
            return
        try:
            d.csv_ImportCSVs(self._active_roster)
            self._refresh_roster_view()
            self._set_status(f"Reloaded '{self._active_roster}' from disk.", muted=True)
        except Exception as e:
            log.exception(f"Reload failed: {e}")
            QMessageBox.warning(self, "Reload Failed", f"Could not reload from disk:\n\n{e}")

    # ── Pane refresh ──────────────────────────────────────────────────────────

    def _refresh_players_view(self):
        """Render every Player in Players.db on the left pane."""
        entries: List[PlayerListEntry] = []
        for sprite_id, player in d.players.items():
            entries.append(PlayerListEntry(
                player=player,
                id_label=str(sprite_id),
            ))
        # Stable display order: by name.
        entries.sort(key=lambda e: (
            (e.player["Last_Name"] or "").lower(),
            (e.player["First_Name"] or "").lower(),
        ))
        self._players_view.set_entries(entries)

    def _refresh_roster_view(self):
        """Render the active roster's used slots, plus an overlay of any pending
        ADD/REMOVE changes from the save_manager queue.

        Saved-on-disk slots that have a queued REMOVE for them get marked
        pending_state="remove" (struck-through, red tint). Pending ADDs get
        their own entries with pending_state="add" (green tint). This way
        the user sees their queued changes before they save.
        """
        if not self._active_roster or self._active_roster not in d.rosters:
            self._roster_view.set_entries([])
            self._set_pane_subtitle("—")
            return

        # Collect pending changes for this roster, indexed by RosterID.
        pending_removes: set[int] = set()
        pending_adds: dict[int, object] = {}  # roster_id -> player dict
        for change in self._save_manager.get_pending_changes():
            if change.data is None:
                continue
            if change.data.get("roster_name") != self._active_roster:
                continue
            if change.change_type == ChangeType.REMOVE_PLAYER_FROM_ROSTER:
                try:
                    pending_removes.add(int(change.data["roster_id"]))
                except (KeyError, TypeError, ValueError):
                    continue
            elif change.change_type == ChangeType.ADD_PLAYER_TO_ROSTER:
                try:
                    rid = int(change.data["roster_id"])
                except (KeyError, TypeError, ValueError):
                    continue
                pending_adds[rid] = change.data.get("player")

        sprite_id_map = d.rosters[self._active_roster].get("SpriteIDs", {})
        entries: List[PlayerListEntry] = []
        unmapped = 0
        for roster_id, sprite_id in sprite_id_map.items():
            if sprite_id is None or sprite_id < 0:
                continue
            player = d.players.get(sprite_id)
            if player is None:
                unmapped += 1
                continue
            rid_int = int(roster_id)
            entries.append(PlayerListEntry(
                player=player,
                id_label=f"#{rid_int:03d}",
                extra_data=rid_int,
                pending_state="remove" if rid_int in pending_removes else None,
            ))

        # Append pending ADDs as new rows (their slot isn't in sprite_id_map yet).
        for rid_int, player in pending_adds.items():
            if player is None:
                continue
            entries.append(PlayerListEntry(
                player=player,
                id_label=f"#{rid_int:03d}",
                extra_data=rid_int,
                pending_state="add",
            ))

        entries.sort(key=lambda e: e.extra_data)
        self._roster_view.set_entries(entries)

        # Subtitle counts saved players + a tally of what's queued.
        used = sum(1 for e in entries if e.pending_state != "add")
        total = 999
        msg = f"{used} / {total} slots used"
        if pending_adds or pending_removes:
            queued_bits = []
            if pending_adds:
                queued_bits.append(f"+{len(pending_adds)}")
            if pending_removes:
                queued_bits.append(f"-{len(pending_removes)}")
            msg += f"  ({' '.join(queued_bits)} queued)"
        if unmapped:
            msg += f" · {unmapped} player(s) on roster but missing from Players.db"
        self._set_pane_subtitle(f"{self._active_roster}.ROS · {msg}")

    def _set_pane_subtitle(self, text: str):
        # The pane header has a child labeled 'subtitle' — find and update it.
        sub = self._roster_pane_header.findChild(QLabel, "subtitle")
        if sub:
            sub.setText(text)

    def _set_status(self, text: str, muted: bool = False):
        color = COLORS['text_muted'] if muted else COLORS['accent_success']
        self._status_lbl.setStyleSheet(f"color: {color}; font-size: 11px;")
        self._status_lbl.setText(text)

    # ── Add / Remove ──────────────────────────────────────────────────────────

    def _on_add_clicked(self, *_):
        if not self._active_roster:
            return
        entry = self._players_view.selected_entry()
        if entry is None:
            self._set_status("Select a player from Players.db first.", muted=True)
            return
        player = entry.player
        sprite_id = player["SpriteID"]

        # Don't double-add a player who's already on the roster
        sprite_id_map = d.rosters[self._active_roster].get("SpriteIDs", {})
        if sprite_id in sprite_id_map.values():
            QMessageBox.information(
                self, "Already on Roster",
                f"{player['First_Name']} {player['Last_Name']} is already on "
                f"'{self._active_roster}.ROS'."
            )
            return

        roster_id = self._find_next_free_roster_id()
        if roster_id is None:
            QMessageBox.warning(
                self, "Roster Full",
                f"No unused RosterIDs left on '{self._active_roster}' "
                f"(accounting for {len([c for c in self._save_manager.get_pending_changes() if c.change_type == ChangeType.ADD_PLAYER_TO_ROSTER])} pending adds)."
            )
            return

        name = f"{player['First_Name'] or '???'} {player['Last_Name'] or '???'}"
        self._save_manager.add_change(PendingChange(
            change_type=ChangeType.ADD_PLAYER_TO_ROSTER,
            description=f"Add {name} -> {self._active_roster}.ROS (slot {roster_id:03d})",
            data={"player": player, "roster_name": self._active_roster, "roster_id": roster_id},
            execute_fn=self._execute_add_player_to_roster,
        ))
        self._queue_roster_sync()
        self._set_status(
            f"Queued: add {name} to {self._active_roster}.ROS at slot #{roster_id:03d}.",
            muted=False,
        )

    def _on_remove_clicked(self, *_):
        if not self._active_roster:
            return
        entry = self._roster_view.selected_entry()
        if entry is None:
            self._set_status("Select a player on the roster first.", muted=True)
            return
        player = entry.player
        roster_id = int(entry.extra_data)
        name = f"{player['First_Name'] or '???'} {player['Last_Name'] or '???'}"

        # Toggle behavior: clicking Remove on a pending change should *cancel*
        # that change rather than queue another one on top of it.
        if entry.pending_state == "add":
            removed = self._save_manager.remove_changes_where(
                lambda c, rn=self._active_roster, rid=roster_id: (
                    c.change_type == ChangeType.ADD_PLAYER_TO_ROSTER
                    and (c.data or {}).get("roster_name") == rn
                    and (c.data or {}).get("roster_id") == rid
                )
            )
            if removed:
                self._maybe_drop_orphaned_sync()
                self._set_status(
                    f"Cancelled queued add of {name} (slot #{roster_id:03d}).",
                    muted=False,
                )
            return

        if entry.pending_state == "remove":
            removed = self._save_manager.remove_changes_where(
                lambda c, rn=self._active_roster, rid=roster_id: (
                    c.change_type == ChangeType.REMOVE_PLAYER_FROM_ROSTER
                    and (c.data or {}).get("roster_name") == rn
                    and (c.data or {}).get("roster_id") == rid
                )
            )
            if removed:
                self._maybe_drop_orphaned_sync()
                self._set_status(
                    f"Cancelled queued remove of {name} (slot #{roster_id:03d}).",
                    muted=False,
                )
            return

        # No prior pending change for this slot — queue a fresh REMOVE.
        self._save_manager.add_change(PendingChange(
            change_type=ChangeType.REMOVE_PLAYER_FROM_ROSTER,
            description=f"Remove {name} from {self._active_roster}.ROS (slot {roster_id:03d})",
            data={"roster_name": self._active_roster, "roster_id": roster_id},
            execute_fn=self._execute_remove_player_from_roster,
        ))
        self._queue_roster_sync()
        self._set_status(
            f"Queued: remove {name} from {self._active_roster}.ROS.",
            muted=False,
        )

    def _maybe_drop_orphaned_sync(self):
        """If no ADD/REMOVE changes remain for the active roster, drop its
        SYNC change too — otherwise we'd run RedMC for nothing on save."""
        if not self._active_roster:
            return
        has_mutations = any(
            c.change_type in (
                ChangeType.ADD_PLAYER_TO_ROSTER,
                ChangeType.REMOVE_PLAYER_FROM_ROSTER,
            )
            and (c.data or {}).get("roster_name") == self._active_roster
            for c in self._save_manager.get_pending_changes()
        )
        if not has_mutations:
            gid = f"sync_roster:{self._active_roster}"
            self._save_manager.remove_changes_where(
                lambda c, target=gid: c.group_id == target
            )

    def _queue_roster_sync(self):
        """Ensure exactly one SYNC_ROSTER_TO_ROS change is queued for the active
        roster — and that it sits at the END of the queue.

        The bump-to-end is critical: every ADD/REMOVE for this roster needs to
        run BEFORE the SYNC. Otherwise the RedMC write fires mid-batch and
        persists a partial state to .ROS while subsequent in-memory mutations
        only land in CSVs.
        """
        if not self._active_roster:
            return
        gid = f"sync_roster:{self._active_roster}"
        if self._save_manager.has_change_with_group_id(gid):
            self._save_manager.bump_to_end(gid)
            return
        self._save_manager.add_change(PendingChange(
            change_type=ChangeType.SYNC_ROSTER_TO_ROS,
            description=f"Sync {self._active_roster}.ROS via RedMC",
            data={"roster_name": self._active_roster},
            execute_fn=self._execute_sync_roster,
            group_id=gid,
        ))

    def _find_next_free_roster_id(self) -> Optional[int]:
        """Find the lowest unused RosterID for the active roster, accounting for
        slots already claimed by queued (but not yet executed) ADDs.

        Returns None if the roster is full when pending claims are considered.
        """
        if not self._active_roster:
            return None
        roster_players = d.rosters[self._active_roster]["Players"][1:]
        # Slots claimed by pending adds we haven't yet executed
        claimed_by_pending = {
            int(c.data["roster_id"])
            for c in self._save_manager.get_pending_changes()
            if c.change_type == ChangeType.ADD_PLAYER_TO_ROSTER
            and c.data.get("roster_name") == self._active_roster
        }
        for entry in roster_players:
            try:
                rid = int(entry["ID"])
            except (KeyError, ValueError, TypeError):
                continue
            if entry.get("IsRegNBA") == "1":
                continue
            if rid in claimed_by_pending:
                continue
            return rid
        return None

    # ── execute_fns (run when user clicks Save) ───────────────────────────────

    def _execute_add_player_to_roster(self, data: dict):
        roster_name = data["roster_name"]
        player = data["player"]
        roster_id = data["roster_id"]

        if roster_name not in d.rosters:
            d.csv_ImportCSVs(roster_name)

        d.csv_UpdatePlayer(roster_name, roster_id, player)
        d.csv_ExportCSVs(roster_name)
        log.info(
            f"Added {player['First_Name']} {player['Last_Name']} "
            f"→ {roster_name}.ROS slot {roster_id}"
        )

    def _execute_remove_player_from_roster(self, data: dict):
        roster_name = data["roster_name"]
        roster_id = data["roster_id"]

        if roster_name not in d.rosters:
            d.csv_ImportCSVs(roster_name)

        # csv_UpdatePlayer with player=None blanks the slot (IsRegNBA=0, names = sentinels).
        d.csv_UpdatePlayer(roster_name, roster_id, None)
        d.csv_ExportCSVs(roster_name)
        log.info(f"Removed slot {roster_id} from {roster_name}.ROS")

    def _execute_sync_roster(self, data: dict):
        roster_name = data["roster_name"]
        log.info(f"Beginning RedMC sync for roster '{roster_name}'")
        exportRosterData(roster_name, d)
        # Notify the registry that this roster's .ROS was rewritten — Phase 2
        # will use the resulting `marked_stale` flag to drive HUD warnings and
        # refuse `loadBlacktopPlayers` until 2K reloads it.
        self._app_state.roster_registry.mark_synced(roster_name)
        log.info(f"RedMC sync complete for '{roster_name}'")

    # ── Create-new ────────────────────────────────────────────────────────────

    def _on_new_clicked(self):
        """Create a brand-new roster from the blank template."""
        name, ok = QInputDialog.getText(
            self, "New Roster",
            "Name for the new roster (no .ROS suffix, no spaces or weird chars):",
        )
        if not ok:
            return
        name = (name or "").strip()
        if not name or not name.replace("_", "").replace("-", "").isalnum():
            QMessageBox.warning(
                self, "Invalid Name",
                "Roster name must be alphanumeric (underscores and hyphens OK)."
            )
            return

        # Refuse collisions
        existing = set(d.csv_GetSavedRosterList())
        saves_dir: Path = paths["gameRosters"]
        existing_ros = {f.stem for f in saves_dir.glob("*.ROS")} if saves_dir.exists() else set()
        if name in existing or name in existing_ros:
            QMessageBox.warning(
                self, "Name Already In Use",
                f"A roster named '{name}' already exists "
                f"(in our app or in {saves_dir}). Pick a different name."
            )
            return

        template_src = paths["templates"] / _BLANK_ROSTER_TEMPLATE
        if not template_src.exists():
            QMessageBox.critical(
                self, "Template Missing",
                f"Blank roster template not found at:\n{template_src}"
            )
            return
        if not saves_dir.exists():
            QMessageBox.critical(
                self, "2K Saves Folder Missing",
                f"Cannot create new roster — 2K saves dir not found:\n{saves_dir}"
            )
            return

        confirm = QMessageBox.question(
            self, "Create New Roster",
            f"This will:\n"
            f"  1. Copy the blank template to '{saves_dir / (name + '.ROS')}'.\n"
            f"  2. Run RedMC to import it (~30s, takes over your screen).\n"
            f"  3. Switch to it as the active roster.\n\n"
            f"Continue?",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel,
        )
        if confirm != QMessageBox.Yes:
            return

        target_ros = saves_dir / f"{name}.ROS"
        try:
            shutil.copy(template_src, target_ros)
            log.info(f"Copied blank roster template → {target_ros}")
        except Exception as e:
            log.exception(f"Failed to copy template: {e}")
            QMessageBox.critical(
                self, "Copy Failed",
                f"Couldn't copy the blank template to {target_ros}:\n\n{e}"
            )
            return

        try:
            importRosterData(name, d)
        except Exception as e:
            log.exception(f"RedMC import failed for new roster '{name}'")
            QMessageBox.critical(
                self, "Import Failed",
                f"The .ROS was copied, but RedMC import failed:\n\n{e}\n\n"
                f"You may need to run 'Import Existing .ROS' manually after fixing this."
            )
            return

        self._refresh_roster_list()
        self._roster_combo.setCurrentText(name)
        self._set_status(f"Created and imported new roster '{name}'.")
