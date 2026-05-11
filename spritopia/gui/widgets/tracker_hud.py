"""
Header HUD showing the live state of the app's working roster + 2K13's
in-memory roster, with a clear match indicator.

Two rows:
  APP  ●  Premier
  2K   ●  Pick Up · Premier  ✓

The match indicator collapses one of five states:
  matched      — both connected, names agree, not stale  →  green ✓
  mismatched   — both connected, names differ            →  yellow ⚠
  stale        — same name but app rewrote .ROS since 2K loaded   →  orange (stale)
  disconnected — 2K not running (no comparison possible) →  gray ○
  app_no_roster — working_roster is None (e.g. user on Radio at boot)  →  gray —

Subscribes to: connection_changed, location_changed, active_roster_changed
(2K-side state) and working_roster_changed, entry_changed (app-side state
from RosterRegistry).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel

from spritopia.gui.theme import COLORS
from spritopia.gui.tracker_bridge import get_tracker_bridge
from spritopia.gui.app_state import get_app_state


# Pretty-name + color mapping per location string returned by tracker.testCurrentScreen.
_LOCATION_LABELS = {
    "Home":            ("Home",            COLORS["text_primary"]),
    "PickUp":          ("Pick Up",         COLORS["accent_primary"]),
    "TeamRoster":      ("Team Roster",     COLORS["text_primary"]),
    "CreatePlayer":    ("Create A Player", COLORS["accent_warning"]),
    "LoadRoster":      ("Load Roster",     COLORS["text_primary"]),
    "SaveRoster":      ("Save Roster",     COLORS["accent_success"]),
    "MyPlayerAccount": ("My Player",       COLORS["text_primary"]),
    "InGame":          ("In Game",         COLORS["accent_success"]),
    "Unknown":         ("Unknown",         COLORS["text_muted"]),
    "Disconnected":    ("Disconnected",    COLORS["accent_danger"]),
}


class TrackerHUDWidget(QFrame):
    """Compact two-row HUD: APP row (working roster), 2K row (screen · roster · match)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(42)
        self.setMinimumWidth(240)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)

        # Two-row grid: [label] [dot] [text]
        grid = QGridLayout(self)
        grid.setContentsMargins(10, 3, 12, 3)
        grid.setHorizontalSpacing(6)
        grid.setVerticalSpacing(0)

        # Row labels
        self._app_label = QLabel("APP")
        self._app_label.setStyleSheet(self._row_label_style())
        grid.addWidget(self._app_label, 0, 0)

        self._twok_label = QLabel("2K")
        self._twok_label.setStyleSheet(self._row_label_style())
        grid.addWidget(self._twok_label, 1, 0)

        # Status dots
        self._app_dot = QLabel("●")
        self._app_dot.setFixedWidth(10)
        self._app_dot.setAlignment(Qt.AlignCenter)
        grid.addWidget(self._app_dot, 0, 1)

        self._twok_dot = QLabel("●")
        self._twok_dot.setFixedWidth(10)
        self._twok_dot.setAlignment(Qt.AlignCenter)
        grid.addWidget(self._twok_dot, 1, 1)

        # Text content
        self._app_text = QLabel("—")
        grid.addWidget(self._app_text, 0, 2)

        self._twok_text = QLabel("disconnected")
        grid.addWidget(self._twok_text, 1, 2)

        grid.setColumnStretch(2, 1)

        # State (mirrors of what bridge + registry tell us)
        self._connected: bool = False
        self._location: str = "Disconnected"
        self._twok_roster: object = None     # str or None
        self._working_roster: object = None  # str or None

        # Bridge signals (2K-side)
        bridge = get_tracker_bridge()
        bridge.connection_changed.connect(self._on_connection_changed)
        bridge.location_changed.connect(self._on_location_changed)
        bridge.active_roster_changed.connect(self._on_2k_roster_changed)

        # Registry signals (app-side)
        registry = get_app_state().roster_registry
        registry.working_roster_changed.connect(self._on_working_roster_changed)
        registry.entry_changed.connect(self._on_entry_changed)

        # Seed from current state
        self._connected = bridge.is_connected()
        self._location = bridge.get_location() if self._connected else "Disconnected"
        self._twok_roster = bridge.get_active_roster() if self._connected else None
        self._working_roster = registry.working_roster
        self._render()

    # ── Slots ─────────────────────────────────────────────────────────────────

    def _on_connection_changed(self, connected: bool):
        self._connected = connected
        if not connected:
            self._location = "Disconnected"
            self._twok_roster = None
        self._render()

    def _on_location_changed(self, location: str):
        self._location = location
        self._render()

    def _on_2k_roster_changed(self, roster_name):
        self._twok_roster = roster_name
        self._render()

    def _on_working_roster_changed(self, roster_name):
        self._working_roster = roster_name
        self._render()

    def _on_entry_changed(self, roster_name: str):
        # Staleness flag may have flipped — re-render even though our text
        # state didn't directly change. Cheap: just recompute match state.
        self._render()

    # ── Render ────────────────────────────────────────────────────────────────

    def _render(self):
        # APP row
        if self._working_roster:
            app_text = self._working_roster
            app_text_color = COLORS["text_secondary"]
            app_dot_color = COLORS["accent_success"]
            app_glyph = "●"
        else:
            app_text = "no working roster"
            app_text_color = COLORS["text_muted"]
            app_dot_color = COLORS["text_muted"]
            app_glyph = "○"

        self._app_text.setText(app_text)
        self._app_text.setStyleSheet(self._row_text_style(app_text_color))
        self._app_dot.setText(app_glyph)
        self._app_dot.setStyleSheet(self._dot_style(app_dot_color))

        # 2K row — screen + roster + match-state suffix
        if not self._connected:
            twok_text = "not running"
            twok_color = COLORS["text_muted"]
            twok_dot_color = COLORS["text_muted"]
            twok_glyph = "○"
            match_suffix = ""
        else:
            loc_pretty, _ = _LOCATION_LABELS.get(
                self._location, (self._location or "Unknown", COLORS["text_muted"])
            )
            if self._twok_roster:
                twok_text = f"{loc_pretty} · {self._twok_roster}"
            else:
                twok_text = f"{loc_pretty} · no roster"
            twok_color = COLORS["text_secondary"]

            match = self._compute_match_state()
            if match == "matched":
                match_suffix = " ✓"
                twok_dot_color = COLORS["accent_success"]
                twok_glyph = "●"
            elif match == "mismatched":
                match_suffix = " ⚠ mismatch"
                twok_dot_color = COLORS["accent_warning"]
                twok_glyph = "●"
                twok_color = COLORS["accent_warning"]
            elif match == "stale":
                match_suffix = " ⚠ stale"
                twok_dot_color = COLORS["accent_warning"]
                twok_glyph = "◐"
                twok_color = COLORS["accent_warning"]
            else:  # "2k_no_roster" or "app_no_roster"
                match_suffix = ""
                twok_dot_color = COLORS["text_muted"]
                twok_glyph = "●"

        self._twok_text.setText(twok_text + match_suffix)
        self._twok_text.setStyleSheet(self._row_text_style(twok_color))
        self._twok_dot.setText(twok_glyph)
        self._twok_dot.setStyleSheet(self._dot_style(twok_dot_color))

        # Tooltip with full debug info
        try:
            registry = get_app_state().roster_registry
            stale_info = "—"
            if self._twok_roster:
                stale_info = "yes" if registry.is_stale(self._twok_roster) else "no"
        except Exception:
            stale_info = "?"

        self.setToolTip(
            f"App working roster:  {self._working_roster or '—'}\n"
            f"2K connected:        {self._connected}\n"
            f"2K screen:           {self._location}\n"
            f"2K loaded roster:    {self._twok_roster or '—'}\n"
            f"Stale (vs disk):     {stale_info}"
        )

    def _compute_match_state(self) -> str:
        """Reduce the (working_roster, twok_roster, stale) tuple to a state name."""
        if self._working_roster is None:
            return "app_no_roster"
        if not self._twok_roster:
            return "2k_no_roster"
        if self._working_roster != self._twok_roster:
            return "mismatched"
        try:
            if get_app_state().roster_registry.is_stale(self._twok_roster):
                return "stale"
        except Exception:
            pass
        return "matched"

    # ── Styles ────────────────────────────────────────────────────────────────

    @staticmethod
    def _row_label_style() -> str:
        return (
            f"font-size: 9px; font-weight: bold; color: {COLORS['text_muted']}; "
            f"letter-spacing: 1px; background: transparent; border: none;"
        )

    @staticmethod
    def _row_text_style(color: str) -> str:
        return (
            f"font-size: 11px; color: {color}; "
            f"background: transparent; border: none;"
        )

    @staticmethod
    def _dot_style(color: str) -> str:
        return (
            f"color: {color}; font-size: 12px; "
            f"background: transparent; border: none;"
        )
