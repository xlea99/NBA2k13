"""
Self-managing banner that surfaces working-roster vs 2K-loaded-roster issues.

Embeds at the top of any screen where roster state matters (Premier home,
the Play flow, etc.). Subscribes to RosterRegistry + tracker bridge signals,
auto-shows when there's a problem, auto-hides when state is healthy.

Banner states it can surface:
    mismatch — 2K has a different roster loaded than the app is operating on
    stale    — same roster name but the app wrote .ROS after 2K last loaded it
    (everything else: hidden)
"""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from spritopia.gui.theme import COLORS
from spritopia.gui.tracker_bridge import get_tracker_bridge
from spritopia.gui.app_state import get_app_state


class RosterStateBanner(QFrame):
    """Thin, colored banner that auto-toggles based on registry + bridge state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._wire_signals()
        self._refresh()

    def _setup_ui(self):
        lo = QHBoxLayout(self)
        lo.setContentsMargins(16, 10, 16, 10)
        lo.setSpacing(12)

        self._icon_lbl = QLabel("⚠")
        self._icon_lbl.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLORS['accent_warning']};"
            f"background: transparent;"
        )
        lo.addWidget(self._icon_lbl)

        self._text_lbl = QLabel("")
        self._text_lbl.setWordWrap(True)
        self._text_lbl.setStyleSheet(
            f"font-size: 12px; color: {COLORS['text_primary']}; "
            f"background: transparent;"
        )
        lo.addWidget(self._text_lbl, stretch=1)

    def _wire_signals(self):
        bridge = get_tracker_bridge()
        bridge.connection_changed.connect(self._refresh)
        bridge.active_roster_changed.connect(self._refresh)

        registry = get_app_state().roster_registry
        registry.working_roster_changed.connect(self._refresh)
        registry.entry_changed.connect(self._refresh)

    # ── State computation ────────────────────────────────────────────────────

    def _refresh(self, *_):
        registry = get_app_state().roster_registry
        bridge = get_tracker_bridge()

        working = registry.working_roster
        if working is None:
            # No working roster (rosterless mode, or initial-import failed).
            # HUD + startup dialog already inform; nothing to nag about here.
            self.hide()
            return

        if not bridge.is_connected():
            # 2K isn't running — no comparison possible, HUD shows the state.
            self.hide()
            return

        twok_roster = bridge.get_active_roster()
        if twok_roster is None:
            # 2K is up but no .ROS loaded — user is mid-load, no warning yet.
            self.hide()
            return

        if working != twok_roster:
            self._show_mismatch(working, twok_roster)
            return

        if registry.is_stale(working):
            self._show_stale(working)
            return

        # Everything in agreement.
        self.hide()

    def _show_mismatch(self, working: str, twok_roster: str):
        self._apply_style(
            border_color=COLORS["accent_warning"],
            bg_color="#3a2810",
        )
        self._text_lbl.setText(
            f"<b>2K has '{twok_roster}' loaded</b>, but the app is operating on "
            f"<b>'{working}'</b>. Reload <b>'{working}'</b> in 2K to use this screen "
            f"(loading players, ripping stats, and CAP sync will all refuse "
            f"until 2K matches)."
        )
        self.show()

    def _show_stale(self, working: str):
        self._apply_style(
            border_color=COLORS["accent_warning"],
            bg_color="#3a2810",
        )
        self._text_lbl.setText(
            f"<b>'{working}' was modified after 2K last loaded it.</b> "
            f"Reload <b>'{working}'</b> in 2K (Esc → Load Roster) to pick up your "
            f"changes — until then, loading players is refused because the in-game "
            f"RosterIDs no longer match what we wrote."
        )
        self.show()

    def _apply_style(self, border_color: str, bg_color: str):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-left: 4px solid {border_color};
                border-radius: 4px;
            }}
        """)
