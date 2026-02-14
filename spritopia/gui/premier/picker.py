"""
Premier Mode Picker Widget.

The 8-slot player picker for loading games into NBA 2K13.
Two teams of 4 players each.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from spritopia.players.players import Player
from spritopia.gui.theme import COLORS, get_archetype_color
from spritopia.gui.widgets.player_card import PlayerCard, EmptyPlayerSlot
from spritopia.gui.app_state import get_app_state
from spritopia.gui.audio import get_audio_player


class PickerSlot(QFrame):
    """
    A single slot in the picker that can hold a player or be empty.
    """

    add_clicked = Signal(int)  # Slot index
    remove_clicked = Signal(int)  # Slot index

    def __init__(self, slot_index: int, parent=None):
        super().__init__(parent)
        self._slot_index = slot_index
        self._player = None
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        self.setFixedHeight(90)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self._show_empty()

    def _show_empty(self):
        """Show the empty state."""
        self._clear_layout()

        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)

        slot_label = QLabel(f"Slot {self._slot_index + 1}")
        slot_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        slot_label.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(slot_label)

        add_btn = QPushButton("+ Add Player")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_primary']};
                border: 1px dashed {COLORS['accent_primary']};
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_primary']}22;
            }}
        """)
        add_btn.clicked.connect(lambda: self.add_clicked.emit(self._slot_index))
        empty_layout.addWidget(add_btn)

        self.layout.addWidget(empty_widget)

    def _show_player(self, player: Player):
        """Show a player in the slot."""
        self._clear_layout()

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        container_layout.setSpacing(8)

        # Archetype bar
        archetype = str(player["Archetype"]) if player["Archetype"] else "None"
        arch_color = get_archetype_color(archetype)

        arch_bar = QFrame()
        arch_bar.setFixedWidth(4)
        arch_bar.setStyleSheet(f"background-color: {arch_color};")
        container_layout.addWidget(arch_bar)

        # Player info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        first = player["First_Name"] or ""
        last = player["Last_Name"] or ""
        name_label = QLabel(f"{first} {last}".strip() or "Unknown")
        name_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        info_layout.addWidget(name_label)

        rarity = player["Rarity"] or "Common"
        sub_label = QLabel(f"{archetype} · {rarity}")
        sub_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        info_layout.addWidget(sub_label)

        container_layout.addLayout(info_layout, stretch=1)

        # Remove button
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(24, 24)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_danger']}33;
                color: {COLORS['accent_danger']};
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_danger']};
                color: white;
            }}
        """)
        remove_btn.clicked.connect(lambda: self.remove_clicked.emit(self._slot_index))
        container_layout.addWidget(remove_btn)

        self.layout.addWidget(container)

    def _clear_layout(self):
        """Clear all widgets from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def set_player(self, player: Player):
        """Set the player for this slot."""
        self._player = player
        if player:
            self._show_player(player)
        else:
            self._show_empty()

    def get_player(self) -> Player:
        return self._player

    @property
    def slot_index(self) -> int:
        return self._slot_index


class TeamPanel(QFrame):
    """
    Panel for one team (4 player slots).
    """

    def __init__(self, team_num: int, parent=None):
        super().__init__(parent)
        self._team_num = team_num
        self._slots = []
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Team header
        team_color = COLORS['accent_primary'] if self._team_num == 1 else COLORS['accent_secondary']
        header = QLabel(f"Team {self._team_num}")
        header.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {team_color};")
        layout.addWidget(header)

        # Player slots (4 per team)
        start_idx = 0 if self._team_num == 1 else 4
        for i in range(4):
            slot = PickerSlot(start_idx + i)
            self._slots.append(slot)
            layout.addWidget(slot)

        layout.addStretch()

    @property
    def slots(self) -> list:
        return self._slots


class PremierPickerWidget(QWidget):
    """
    Main Premier mode picker widget.

    Contains two team panels with 4 slots each.
    Allows adding players from the sidebar and loading them into the game.
    """

    load_requested = Signal()  # Emitted when user wants to load into game

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Premier Picker")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Action buttons
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_danger']}22;
                color: {COLORS['accent_danger']};
                border: 1px solid {COLORS['accent_danger']}44;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_danger']};
                color: white;
            }}
        """)
        self.clear_btn.clicked.connect(self._on_clear_all)
        header_layout.addWidget(self.clear_btn)

        self.load_btn = QPushButton("Load Game")
        self.load_btn.setProperty("class", "primary")
        self.load_btn.clicked.connect(self._on_load_game)
        header_layout.addWidget(self.load_btn)

        layout.addLayout(header_layout)

        # Subtitle
        subtitle = QLabel("Select a player in the sidebar, then click 'Add Player' on a slot")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Teams container
        teams_layout = QHBoxLayout()
        teams_layout.setSpacing(24)

        self.team1_panel = TeamPanel(1)
        teams_layout.addWidget(self.team1_panel)

        self.team2_panel = TeamPanel(2)
        teams_layout.addWidget(self.team2_panel)

        layout.addLayout(teams_layout, stretch=1)

    def _connect_signals(self):
        """Connect slot signals."""
        for slot in self.team1_panel.slots + self.team2_panel.slots:
            slot.add_clicked.connect(self._on_add_to_slot)
            slot.remove_clicked.connect(self._on_remove_from_slot)

        # Listen to app state
        app_state = get_app_state()
        app_state.picker_updated.connect(self._sync_from_state)

    def _on_add_to_slot(self, slot_index: int):
        """Handle adding a player to a slot."""
        app_state = get_app_state()
        player = app_state.selected_player

        if player is None:
            QMessageBox.warning(
                self,
                "No Player Selected",
                "Select a player in the sidebar first."
            )
            return

        # Check if player is already in picker
        if player in app_state.picker_slots:
            QMessageBox.warning(
                self,
                "Already Added",
                f"{player['First_Name']} {player['Last_Name']} is already in the picker."
            )
            return

        app_state.set_picker_slot(slot_index, player)
        get_audio_player().play_click()

    def _on_remove_from_slot(self, slot_index: int):
        """Handle removing a player from a slot."""
        app_state = get_app_state()
        app_state.clear_picker_slot(slot_index)
        get_audio_player().play_click()

    def _sync_from_state(self):
        """Sync UI with app state."""
        app_state = get_app_state()
        all_slots = self.team1_panel.slots + self.team2_panel.slots

        for i, slot in enumerate(all_slots):
            if i < len(app_state.picker_slots):
                slot.set_player(app_state.picker_slots[i])

    def _on_clear_all(self):
        """Clear all picker slots."""
        app_state = get_app_state()
        app_state.clear_all_picker_slots()

    def _on_load_game(self):
        """Handle load game button."""
        app_state = get_app_state()

        # Check if we have enough players
        team1 = [p for p in app_state.picker_slots[:4] if p is not None]
        team2 = [p for p in app_state.picker_slots[4:] if p is not None]

        if len(team1) == 0 or len(team2) == 0:
            QMessageBox.warning(
                self,
                "Incomplete Teams",
                "Both teams need at least one player."
            )
            return

        # Emit signal for parent to handle
        self.load_requested.emit()

    def get_teams(self) -> tuple:
        """Get the two teams as lists of players."""
        app_state = get_app_state()
        team1 = [p for p in app_state.picker_slots[:4] if p is not None]
        team2 = [p for p in app_state.picker_slots[4:] if p is not None]
        return team1, team2
