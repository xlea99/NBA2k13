"""
Settings tab — top-level settings/admin area for Spritopia.

Houses sub-tabs for non-gameplay administrative work. Currently just one
sub-tab ("Manage Data") which contains the Roster Manager. As more admin
surfaces are added (preferences, backups, debug tools, etc.) they go here.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from spritopia.gui.theme import COLORS
from spritopia.gui.manage_data import RosterManagerWidget


class SettingsTab(QWidget):
    """Container widget for the Settings area's sub-tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        self._sub_tabs = QTabWidget()
        self._sub_tabs.setTabPosition(QTabWidget.North)
        self._sub_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 10px 22px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
        """)

        self._manage_data = RosterManagerWidget()
        self._sub_tabs.addTab(self._manage_data, "Manage Data")

        lo.addWidget(self._sub_tabs)
