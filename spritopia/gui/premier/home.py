"""
Premier Mode Home/Dashboard Widget.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from spritopia.gui.theme import COLORS


class QuickActionCard(QFrame):
    """A clickable card for quick actions."""

    clicked = Signal()

    def __init__(self, title: str, description: str, icon: str = "", parent=None):
        super().__init__(parent)
        self._setup_ui(title, description, icon)

    def _setup_ui(self, title: str, description: str, icon: str):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
            QFrame:hover {{
                background-color: {COLORS['bg_light']};
                border-color: {COLORS['accent_primary']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class PremierHomeWidget(QWidget):
    """
    Premier mode home/dashboard.

    Shows quick actions and recent activity.
    """

    open_picker = Signal()
    open_create_player = Signal()
    open_stats = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Header
        header = QLabel("Premier Mode")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        subtitle = QLabel("Play blacktop games, track stats, and build your roster")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        # Quick actions grid
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 16px;")
        layout.addWidget(actions_label)

        actions_grid = QGridLayout()
        actions_grid.setSpacing(16)

        # Picker card
        picker_card = QuickActionCard(
            "Game Picker",
            "Select players and load a blacktop game into NBA 2K13"
        )
        picker_card.clicked.connect(self.open_picker.emit)
        actions_grid.addWidget(picker_card, 0, 0)

        # Create player card
        create_card = QuickActionCard(
            "Create Players",
            "Queue new players for generation and open them like packs"
        )
        create_card.clicked.connect(self.open_create_player.emit)
        actions_grid.addWidget(create_card, 0, 1)

        # Stats card
        stats_card = QuickActionCard(
            "Stats Center",
            "View player stats, game history, and leaderboards"
        )
        stats_card.clicked.connect(self.open_stats.emit)
        actions_grid.addWidget(stats_card, 1, 0)

        # Roster card
        roster_card = QuickActionCard(
            "Roster Manager",
            "Manage saved rosters and player data"
        )
        # TODO: Connect to roster manager
        actions_grid.addWidget(roster_card, 1, 1)

        layout.addLayout(actions_grid)

        # Recent activity section (placeholder)
        recent_label = QLabel("Recent Games")
        recent_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 16px;")
        layout.addWidget(recent_label)

        recent_placeholder = QFrame()
        recent_placeholder.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
                min-height: 100px;
            }}
        """)
        recent_layout = QVBoxLayout(recent_placeholder)
        recent_layout.setAlignment(Qt.AlignCenter)

        no_games = QLabel("No recent games")
        no_games.setStyleSheet(f"color: {COLORS['text_muted']};")
        recent_layout.addWidget(no_games)

        layout.addWidget(recent_placeholder)

        layout.addStretch()
