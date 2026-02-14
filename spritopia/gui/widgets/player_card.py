"""
Compact player card widget for lists and grids.
"""

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

from spritopia.players.players import Player
from spritopia.gui.theme import COLORS, get_rarity_color, get_rarity_style, get_archetype_color, get_archetype_style


class PlayerCard(QFrame):
    """
    A compact card displaying basic player info.
    Used in search results, picker slots, etc.
    """

    clicked = Signal(object)  # Emits the Player when clicked

    def __init__(self, player: Player = None, parent=None):
        super().__init__(parent)
        self._player = player
        self._setup_ui()
        if player:
            self.set_player(player)

    def _setup_ui(self):
        self.setProperty("class", "card")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Left section: Archetype indicator bar
        self.archetype_bar = QFrame()
        self.archetype_bar.setFixedWidth(4)
        self.archetype_bar.setStyleSheet(f"background-color: {COLORS['text_muted']};")
        layout.addWidget(self.archetype_bar)

        # Center section: Name and info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        self.name_label = QLabel("--")
        self.name_label.setStyleSheet(f"font-weight: bold; font-size: 14px;")
        info_layout.addWidget(self.name_label)

        self.subtitle_label = QLabel("--")
        self.subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        info_layout.addWidget(self.subtitle_label)

        layout.addLayout(info_layout, stretch=1)

        # Right section: Rarity badge
        self.rarity_badge = QLabel("--")
        self.rarity_badge.setFixedWidth(70)
        self.rarity_badge.setAlignment(Qt.AlignCenter)
        self.rarity_badge.setStyleSheet(f"""
            font-size: 10px;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            background-color: {COLORS['bg_light']};
        """)
        layout.addWidget(self.rarity_badge)

    def set_player(self, player: Player):
        """Update the card with player data."""
        self._player = player

        if player is None:
            self.name_label.setText("--")
            self.subtitle_label.setText("--")
            self.rarity_badge.setText("--")
            self.archetype_bar.setStyleSheet(f"background-color: {COLORS['text_muted']};")
            return

        # Name
        first = player["First_Name"] or ""
        last = player["Last_Name"] or ""
        self.name_label.setText(f"{first} {last}".strip() or "Unknown")

        # Subtitle: Archetype and Faction
        archetype = str(player["Archetype"]) if player["Archetype"] else "None"
        faction = player["Faction"] or ""
        subtitle_parts = [archetype]
        if faction:
            subtitle_parts.append(faction)
        self.subtitle_label.setText(" · ".join(subtitle_parts))

        # Archetype color bar with new styling
        arch_style = get_archetype_style(archetype)
        self.archetype_bar.setStyleSheet(f"background-color: {arch_style['color']};")

        # Rarity badge with new styling
        rarity = player["Rarity"] or "Common"
        rarity_style = get_rarity_style(rarity)
        self.rarity_badge.setText(rarity.upper())

        if rarity.lower() == "godlike":
            # Special godlike styling
            self.rarity_badge.setStyleSheet(f"""
                font-size: 10px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                background-color: {rarity_style['bg']};
                color: {rarity_style['text']};
                border: 1px solid {rarity_style['glow']};
            """)
        else:
            self.rarity_badge.setStyleSheet(f"""
                font-size: 10px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                background-color: {rarity_style['bg']};
                color: {rarity_style['color']};
            """)

    def get_player(self) -> Player:
        """Get the current player."""
        return self._player

    def mousePressEvent(self, event):
        """Handle click events."""
        if event.button() == Qt.LeftButton and self._player:
            self.clicked.emit(self._player)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Hover effect."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['accent_primary']};
                border-radius: 8px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Remove hover effect."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        super().leaveEvent(event)


class EmptyPlayerSlot(QFrame):
    """
    An empty slot placeholder for the picker.
    """

    clicked = Signal(int)  # Emits slot index when clicked

    def __init__(self, slot_index: int, parent=None):
        super().__init__(parent)
        self._slot_index = slot_index
        self._setup_ui()

    def _setup_ui(self):
        self.setProperty("class", "card")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 2px dashed {COLORS['border_light']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(f"+ Slot {self._slot_index + 1}")
        label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self._slot_index)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 2px dashed {COLORS['accent_primary']};
                border-radius: 8px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 2px dashed {COLORS['border_light']};
                border-radius: 8px;
            }}
        """)
        super().leaveEvent(event)
