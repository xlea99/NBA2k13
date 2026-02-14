"""
Pack Reveal Widget.

Animated reveal of newly created players, similar to card pack openings.
Shows rarity with dramatic sound effects and visual flair.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsOpacityEffect, QSizePolicy, QStackedWidget,
    QScrollArea, QGridLayout, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QTimer, QSize
from PySide6.QtGui import QPixmap, QFont

from spritopia.players.players import Player
from spritopia.players import archetypes
from spritopia.gui.theme import COLORS, get_rarity_color, get_rarity_style, get_archetype_color, get_archetype_style
from spritopia.gui.audio import get_audio_player
from spritopia.common.paths import paths


class IconWithTooltip(QLabel):
    """A label that displays an image with a rich tooltip."""

    def __init__(self, size: int = 48, parent=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        self._tooltip_title = ""
        self._tooltip_desc = ""

    def set_image(self, image_path: str):
        """Set the image from a file path."""
        if image_path:
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self._size, self._size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.setPixmap(scaled)
            else:
                self.setText("?")
                self.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 20px; font-weight: bold;")
        else:
            self.setText("?")
            self.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 20px; font-weight: bold;")

    def set_tooltip_content(self, title: str, description: str):
        """Set the tooltip title and description."""
        self._tooltip_title = title
        self._tooltip_desc = description
        # Build rich tooltip
        tooltip = f"<b>{title}</b>"
        if description:
            # Wrap long descriptions
            wrapped = description[:300] + "..." if len(description) > 300 else description
            tooltip += f"<br/><br/>{wrapped}"
        self.setToolTip(tooltip)


class StatMiniBar(QWidget):
    """A compact stat bar for the card."""

    def __init__(self, label: str, value: int = 0, parent=None):
        super().__init__(parent)
        self._setup_ui(label, value)

    def _setup_ui(self, label: str, value: int):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 1, 0, 1)
        layout.setSpacing(4)

        # Stat name (abbreviated)
        name_label = QLabel(label[:8])
        name_label.setFixedWidth(55)
        name_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        layout.addWidget(name_label)

        # Progress bar
        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(6)
        self.bar.setMaximum(99)
        self.bar.setValue(value)
        layout.addWidget(self.bar, stretch=1)

        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setFixedWidth(22)
        self.value_label.setAlignment(Qt.AlignRight)
        self.value_label.setStyleSheet(f"font-weight: bold; font-size: 10px;")
        layout.addWidget(self.value_label)

        self._update_color(value)

    def _update_color(self, value: int):
        if value >= 85:
            color = COLORS['accent_success']
        elif value >= 70:
            color = COLORS['accent_primary']
        elif value >= 50:
            color = COLORS['accent_warning']
        else:
            color = COLORS['accent_danger']

        self.bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['bg_dark']};
                border-radius: 3px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        self.value_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 10px;")


class RevealCard(QFrame):
    """
    A single card that reveals a player with animation.
    Shows faction/artifact icons and top stats.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player = None
        self._revealed = False
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedSize(300, 420)
        self.setStyleSheet(f"""
            RevealCard {{
                background-color: {COLORS['bg_card']};
                border: 3px solid {COLORS['border_dark']};
                border-radius: 16px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        # Unrevealed state - question mark
        self.unrevealed_container = QWidget()
        unrevealed_layout = QVBoxLayout(self.unrevealed_container)
        unrevealed_layout.setAlignment(Qt.AlignCenter)

        question_mark = QLabel("?")
        question_mark.setStyleSheet(f"font-size: 120px; font-weight: bold; color: {COLORS['text_muted']};")
        question_mark.setAlignment(Qt.AlignCenter)
        unrevealed_layout.addWidget(question_mark)

        click_hint = QLabel("Click to reveal")
        click_hint.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
        click_hint.setAlignment(Qt.AlignCenter)
        unrevealed_layout.addWidget(click_hint)

        layout.addWidget(self.unrevealed_container)

        # Revealed state
        self.revealed_container = QWidget()
        self.revealed_container.hide()
        revealed_layout = QVBoxLayout(self.revealed_container)
        revealed_layout.setContentsMargins(0, 0, 0, 0)
        revealed_layout.setSpacing(6)

        # Rarity banner at top
        self.rarity_banner = QLabel("COMMON")
        self.rarity_banner.setAlignment(Qt.AlignCenter)
        self.rarity_banner.setFixedHeight(28)
        self.rarity_banner.setStyleSheet(f"""
            background-color: {COLORS['rarity_common']};
            color: white;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            border-radius: 4px;
        """)
        revealed_layout.addWidget(self.rarity_banner)

        # Archetype indicator
        self.archetype_label = QLabel("Slayer")
        self.archetype_label.setAlignment(Qt.AlignCenter)
        self.archetype_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['arch_slayer']};")
        revealed_layout.addWidget(self.archetype_label)

        # Player name
        self.name_label = QLabel("Player Name")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {COLORS['text_primary']};")
        revealed_layout.addWidget(self.name_label)

        # Position
        self.position_label = QLabel("SG/PG")
        self.position_label.setAlignment(Qt.AlignCenter)
        self.position_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        revealed_layout.addWidget(self.position_label)

        # Faction and Artifact row with icons
        icons_row = QHBoxLayout()
        icons_row.setSpacing(8)

        # Faction section (left)
        faction_section = QVBoxLayout()
        faction_section.setSpacing(2)
        faction_section.setAlignment(Qt.AlignCenter)

        self.faction_name_label = QLabel("Faction")
        self.faction_name_label.setAlignment(Qt.AlignCenter)
        self.faction_name_label.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']}; font-weight: bold;")
        faction_section.addWidget(self.faction_name_label)

        self.faction_icon = IconWithTooltip(size=52)
        self.faction_icon.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 6px;")
        faction_section.addWidget(self.faction_icon, alignment=Qt.AlignCenter)

        icons_row.addLayout(faction_section)

        # Stats section (middle) - important attributes
        stats_section = QVBoxLayout()
        stats_section.setSpacing(2)
        self.stat_bars = []
        for i in range(5):
            bar = StatMiniBar("---", 0)
            bar.hide()
            self.stat_bars.append(bar)
            stats_section.addWidget(bar)
        icons_row.addLayout(stats_section, stretch=1)

        # Artifact section (right)
        artifact_section = QVBoxLayout()
        artifact_section.setSpacing(2)
        artifact_section.setAlignment(Qt.AlignCenter)

        self.artifact_name_label = QLabel("Artifact")
        self.artifact_name_label.setAlignment(Qt.AlignCenter)
        self.artifact_name_label.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']}; font-weight: bold;")
        artifact_section.addWidget(self.artifact_name_label)

        self.artifact_icon = IconWithTooltip(size=52)
        self.artifact_icon.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 6px;")
        artifact_section.addWidget(self.artifact_icon, alignment=Qt.AlignCenter)

        icons_row.addLayout(artifact_section)

        revealed_layout.addLayout(icons_row)
        revealed_layout.addStretch()

        layout.addWidget(self.revealed_container)

        # Setup opacity effect for animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)

    def set_player(self, player: Player):
        """Set the player to reveal."""
        self._player = player
        self._revealed = False
        self.unrevealed_container.show()
        self.revealed_container.hide()
        self.setCursor(Qt.PointingHandCursor)

        # Reset border
        self.setStyleSheet(f"""
            RevealCard {{
                background-color: {COLORS['bg_card']};
                border: 3px solid {COLORS['border_dark']};
                border-radius: 16px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

    def reveal(self):
        """Reveal the player with animation."""
        if self._revealed or self._player is None:
            return

        self._revealed = True
        self.setCursor(Qt.ArrowCursor)

        # Get player info
        rarity = self._player["Rarity"] or "Common"
        rarity_style = get_rarity_style(rarity)
        rarity_color = rarity_style['color']

        archetype = self._player["Archetype"]
        archetype_name = str(archetype) if archetype else "Unknown"
        archetype_style = get_archetype_style(archetype_name)

        first = self._player["First_Name"] or ""
        last = self._player["Last_Name"] or ""
        name = f"{first} {last}".strip() or "Unknown"

        faction = self._player["Faction"] or "No Faction"

        # Position
        if archetype:
            pos = getattr(archetype, 'inGamePositionString', 'N/A')
            pos2 = getattr(archetype, 'inGameSecondaryPositionString', '')
            position = f"{pos}/{pos2}" if pos2 and pos2 != "None" else pos
        else:
            position = "N/A"

        # Play sound
        get_audio_player().play_rarity_reveal(rarity)

        # Update UI - rarity banner with new styling
        self.rarity_banner.setText(rarity.upper())
        if rarity.lower() == "godlike":
            # Special godlike styling with glow
            self.rarity_banner.setStyleSheet(f"""
                background-color: {rarity_style['bg']};
                color: {rarity_style['text']};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                border-radius: 4px;
                border: 1px solid {rarity_style['glow']};
            """)
        else:
            self.rarity_banner.setStyleSheet(f"""
                background-color: {rarity_style['bg']};
                color: {rarity_color};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                border-radius: 4px;
            """)

        self.archetype_label.setText(archetype_name)
        self.archetype_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {archetype_style['color']};")

        self.name_label.setText(name)
        self.position_label.setText(position)

        # Faction icon and tooltip
        self.faction_name_label.setText(faction[:12] + "..." if len(faction) > 12 else faction)
        faction_icon_path = paths["graphics"] / "FactionIcons" / f"{faction}.png"
        self.faction_icon.set_image(str(faction_icon_path))

        # Get faction description for tooltip
        try:
            from spritopia.players import factions
            faction_info = factions.dbDict["Factions"].get(faction, {})
            faction_desc = faction_info.get("Description", "")
            self.faction_icon.set_tooltip_content(faction, faction_desc)
        except Exception:
            self.faction_icon.set_tooltip_content(faction, "")

        # Artifact icon and tooltip
        pmods = self._player.pmods if hasattr(self._player, 'pmods') else []
        if pmods:
            pmod = pmods[0]
            artifact_name = pmod.get("Name", "Unknown")
            artifact_desc = pmod.get("Description", "")
            artifact_image = pmod.get("Image", "")

            # Truncate name for display
            display_name = artifact_name[:10] + "..." if len(artifact_name) > 10 else artifact_name
            self.artifact_name_label.setText(display_name)
            self.artifact_name_label.show()
            self.artifact_icon.show()

            # Load artifact image
            if artifact_image:
                artifact_icon_path = paths["graphics"] / artifact_image
                self.artifact_icon.set_image(str(artifact_icon_path))
            else:
                self.artifact_icon.setText("?")

            self.artifact_icon.set_tooltip_content(artifact_name, artifact_desc)
        else:
            self.artifact_name_label.setText("None")
            self.artifact_icon.setText("-")
            self.artifact_icon.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px; background-color: {COLORS['bg_light']}; border-radius: 6px;")
            self.artifact_icon.setToolTip("No artifact")

        # Important attributes
        if archetype and hasattr(archetype, 'attributeImportance'):
            important_attrs = archetype.attributeImportance[:5]
            for i, attr in enumerate(important_attrs):
                value = self._player[attr] or 0
                attr_name = archetypes.MAPPED_ATTRIBUTES.get(attr, attr)
                self.stat_bars[i].findChild(QLabel).setText(attr_name[:8])
                self.stat_bars[i].bar.setValue(value)
                self.stat_bars[i].value_label.setText(str(value))
                self.stat_bars[i]._update_color(value)
                self.stat_bars[i].show()
        else:
            for bar in self.stat_bars:
                bar.hide()

        # Update border color based on rarity
        if rarity.lower() == "godlike":
            # Godlike gets special glow border
            self.setStyleSheet(f"""
                RevealCard {{
                    background-color: {rarity_style['bg']};
                    border: 3px solid {rarity_style['glow']};
                    border-radius: 16px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                RevealCard {{
                    background-color: {COLORS['bg_card']};
                    border: 3px solid {rarity_color};
                    border-radius: 16px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)

        # Switch containers
        self.unrevealed_container.hide()
        self.revealed_container.show()

    def mousePressEvent(self, event):
        """Handle click to reveal."""
        if event.button() == Qt.LeftButton and not self._revealed:
            self.reveal()
        super().mousePressEvent(event)

    def is_revealed(self) -> bool:
        return self._revealed

    def get_player(self) -> Player:
        return self._player


class PackRevealWidget(QWidget):
    """
    Pack reveal experience for newly created players.

    Shows cards that can be clicked to reveal, with dramatic effects.
    """

    finished = Signal()  # Emitted when all reveals are done and user clicks continue
    reveal_all_clicked = Signal()  # Emitted when reveal all is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self._players = []
        self._cards = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        self.title = QLabel("Reveal Your Players!")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(self.title)

        header_layout.addStretch()

        self.reveal_all_btn = QPushButton("Reveal All")
        self.reveal_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_secondary']};
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #6d28d9;
            }}
        """)
        self.reveal_all_btn.clicked.connect(self._reveal_all)
        header_layout.addWidget(self.reveal_all_btn)

        layout.addLayout(header_layout)

        # Subtitle
        self.subtitle = QLabel("Click each card to reveal your new player")
        self.subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(self.subtitle)

        # Cards container (scrollable for many cards)
        self.cards_scroll_area = QScrollArea()
        self.cards_scroll_area.setWidgetResizable(True)
        self.cards_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cards_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cards_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setAlignment(Qt.AlignCenter)

        self.cards_scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.cards_scroll_area, stretch=1)

        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white;
                border: none;
                padding: 14px 32px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #0ea572;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_muted']};
            }}
        """)
        self.continue_btn.clicked.connect(self._on_continue)
        bottom_layout.addWidget(self.continue_btn)

        bottom_layout.addStretch()
        layout.addLayout(bottom_layout)

    def set_players(self, players: list):
        """Set the players to reveal."""
        self._players = players

        # Clear existing cards
        self._cards.clear()
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Determine grid dimensions (max 4 cards per row for larger cards)
        cards_per_row = min(4, max(1, len(players)))

        # Create cards and arrange in grid
        for i, player in enumerate(players):
            card = RevealCard()
            card.set_player(player)
            self._cards.append(card)
            row = i // cards_per_row
            col = i % cards_per_row
            self.cards_layout.addWidget(card, row, col)

        # Update title
        count = len(players)
        self.title.setText(f"Reveal Your Player{'s' if count != 1 else ''}!")
        self.subtitle.setText(f"Click each card to reveal ({count} player{'s' if count != 1 else ''})")

        # Reset buttons
        self.reveal_all_btn.setEnabled(True)
        self.continue_btn.setEnabled(False)

    def _reveal_all(self):
        """Reveal all cards with staggered timing."""
        self.reveal_all_btn.setEnabled(False)

        # Reveal cards with delay
        for i, card in enumerate(self._cards):
            if not card.is_revealed():
                QTimer.singleShot(i * 400, card.reveal)

        # Enable continue after all reveals
        QTimer.singleShot(len(self._cards) * 400 + 500, self._check_all_revealed)

    def _check_all_revealed(self):
        """Check if all cards are revealed and enable continue."""
        all_revealed = all(card.is_revealed() for card in self._cards)
        if all_revealed:
            self.continue_btn.setEnabled(True)
            self.subtitle.setText("All players revealed! Click Continue to proceed.")

    def _on_continue(self):
        """Handle continue button."""
        self.finished.emit()

    def get_revealed_players(self) -> list:
        """Get all revealed players."""
        return [card.get_player() for card in self._cards if card.is_revealed()]

    def mousePressEvent(self, event):
        """Check reveals after any click."""
        super().mousePressEvent(event)
        QTimer.singleShot(100, self._check_all_revealed)
