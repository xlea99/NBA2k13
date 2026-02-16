"""
Player Creation Form Widget.

Allows users to queue players for creation with optional archetype/faction selection.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFrame, QScrollArea, QCheckBox,
    QListWidget, QListWidgetItem, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from spritopia.gui.theme import COLORS, get_archetype_color, get_rarity_color
from spritopia.data_storage.data_storage import DataStorage


class QueuedPlayerItem(QFrame):
    """A single queued player in the creation queue."""

    remove_clicked = Signal(int)  # Index to remove

    def __init__(self, index: int, player_data: dict, parent=None):
        super().__init__(parent)
        self._index = index
        self._data = player_data
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Index number
        index_label = QLabel(f"#{self._index + 1}")
        index_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; font-weight: bold;")
        index_label.setFixedWidth(30)
        layout.addWidget(index_label)

        # Name
        first = self._data.get('first_name') or '???'
        last = self._data.get('last_name') or '???'
        name = f"{first} {last}"
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(name_label, stretch=1)

        # Archetype
        archetype = self._data.get('archetype', 'Random')
        if archetype and archetype != 'Random':
            arch_color = get_archetype_color(archetype)
            arch_label = QLabel(archetype)
            arch_label.setStyleSheet(f"color: {arch_color}; font-size: 12px;")
        else:
            arch_label = QLabel("Random")
            arch_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        arch_label.setFixedWidth(80)
        layout.addWidget(arch_label)

        # Faction
        faction = self._data.get('faction', 'Random')
        faction_label = QLabel(faction or "Random")
        faction_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        faction_label.setFixedWidth(100)
        layout.addWidget(faction_label)

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
        remove_btn.clicked.connect(lambda: self.remove_clicked.emit(self._index))
        layout.addWidget(remove_btn)


class CreationFormWidget(QWidget):
    """
    Form for queuing players to create.

    Users can:
    - Enter first/last name (or leave blank for random)
    - Select archetype (or random)
    - Select faction (or random)
    - Queue multiple players
    - Generate all queued players
    """

    generate_requested = Signal(list)  # Emits list of player data dicts

    def __init__(self, parent=None):
        super().__init__(parent)
        self._queue = []
        self._factions = []
        self._rosters = []
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top: Input form
        form_frame = QFrame()
        form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(16)

        # Title
        title = QLabel("Queue New Players")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        form_layout.addWidget(title)

        # Name row
        name_row = QHBoxLayout()
        name_row.setSpacing(12)

        first_name_container = QVBoxLayout()
        first_name_label = QLabel("First Name")
        first_name_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        first_name_container.addWidget(first_name_label)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Leave blank for random")
        first_name_container.addWidget(self.first_name_input)
        name_row.addLayout(first_name_container)

        last_name_container = QVBoxLayout()
        last_name_label = QLabel("Last Name")
        last_name_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        last_name_container.addWidget(last_name_label)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Leave blank for random")
        last_name_container.addWidget(self.last_name_input)
        name_row.addLayout(last_name_container)

        form_layout.addLayout(name_row)

        # Options row - use grid so labels align across columns
        options_grid = QGridLayout()
        options_grid.setHorizontalSpacing(12)
        options_grid.setVerticalSpacing(4)
        options_grid.setColumnStretch(0, 1)
        options_grid.setColumnStretch(1, 1)

        archetype_label = QLabel("Archetype")
        archetype_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        options_grid.addWidget(archetype_label, 0, 0)

        faction_label = QLabel("Faction")
        faction_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        options_grid.addWidget(faction_label, 0, 1)

        appearance_label = QLabel("Appearance")
        appearance_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        options_grid.addWidget(appearance_label, 0, 2)

        self.archetype_combo = QComboBox()
        self.archetype_combo.addItem("Random", None)
        self.archetype_combo.addItem("Slayer", "Slayer")
        self.archetype_combo.addItem("Vigilante", "Vigilante")
        self.archetype_combo.addItem("Medic", "Medic")
        self.archetype_combo.addItem("Guardian", "Guardian")
        self.archetype_combo.addItem("Engineer", "Engineer")
        self.archetype_combo.addItem("Director", "Director")
        options_grid.addWidget(self.archetype_combo, 1, 0)

        self.faction_combo = QComboBox()
        self.faction_combo.addItem("Random", None)
        # Factions will be populated from data
        options_grid.addWidget(self.faction_combo, 1, 1)

        self.random_appearance_check = QCheckBox("Random")
        self.random_appearance_check.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_primary']};
                font-size: 12px;
                spacing: 6px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
        """)
        options_grid.addWidget(self.random_appearance_check, 1, 2)

        form_layout.addLayout(options_grid)

        # Add to queue button
        add_btn = QPushButton("+ Add to Queue")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #3b8bdb;
            }}
        """)
        add_btn.clicked.connect(self._add_to_queue)
        form_layout.addWidget(add_btn)

        layout.addWidget(form_frame)

        # Middle: Queue list
        queue_container = QWidget()
        queue_layout = QVBoxLayout(queue_container)
        queue_layout.setContentsMargins(20, 16, 20, 16)
        queue_layout.setSpacing(12)

        queue_header = QHBoxLayout()
        queue_title = QLabel("Creation Queue")
        queue_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        queue_header.addWidget(queue_title)

        self.queue_count = QLabel("0 players")
        self.queue_count.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        queue_header.addWidget(self.queue_count)

        queue_header.addStretch()

        clear_queue_btn = QPushButton("Clear All")
        clear_queue_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_danger']};
                border: 1px solid {COLORS['accent_danger']}44;
                padding: 6px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_danger']}22;
            }}
        """)
        clear_queue_btn.clicked.connect(self._clear_queue)
        queue_header.addWidget(clear_queue_btn)

        queue_layout.addLayout(queue_header)

        # Scrollable queue list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.queue_widget = QWidget()
        self.queue_list_layout = QVBoxLayout(self.queue_widget)
        self.queue_list_layout.setContentsMargins(0, 0, 0, 0)
        self.queue_list_layout.setSpacing(8)
        self.queue_list_layout.addStretch()

        scroll.setWidget(self.queue_widget)
        queue_layout.addWidget(scroll, stretch=1)

        layout.addWidget(queue_container, stretch=1)

        # Bottom: Roster selection and generate button
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(20, 16, 20, 16)
        bottom_layout.setSpacing(12)

        # Roster options
        roster_row = QHBoxLayout()
        roster_row.setSpacing(12)

        self.add_to_roster_check = QCheckBox("Add to roster after creation")
        self.add_to_roster_check.setChecked(True)
        self.add_to_roster_check.setStyleSheet(f"color: {COLORS['text_primary']};")
        roster_row.addWidget(self.add_to_roster_check)

        self.roster_combo = QComboBox()
        self.roster_combo.setMinimumWidth(150)
        # Will be populated with available rosters
        roster_row.addWidget(self.roster_combo)

        roster_row.addStretch()
        bottom_layout.addLayout(roster_row)

        # Generate button
        self.generate_btn = QPushButton("Generate & Reveal Players")
        self.generate_btn.setEnabled(False)
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white;
                border: none;
                padding: 16px 32px;
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
        self.generate_btn.clicked.connect(self._on_generate)
        bottom_layout.addWidget(self.generate_btn)

        layout.addWidget(bottom_frame)

    def _load_data(self):
        """Load factions and rosters from data storage."""
        try:
            # Load factions
            from spritopia.players import factions
            self._factions = sorted(list(factions.dbDict["Factions"]))
            for faction in self._factions:
                self.faction_combo.addItem(faction, faction)
        except Exception as e:
            print(f"Failed to load factions: {e}")

        try:
            # Load available rosters
            self._rosters = DataStorage.csv_GetSavedRosterList()
            # Add Premier as default/first if it exists
            if "Premier" in self._rosters:
                self.roster_combo.addItem("Premier", "Premier")
                for roster in self._rosters:
                    if roster != "Premier":
                        self.roster_combo.addItem(roster, roster)
            else:
                for roster in self._rosters:
                    self.roster_combo.addItem(roster, roster)

            if len(self._rosters) == 0:
                self.roster_combo.addItem("No rosters available", None)
                self.add_to_roster_check.setEnabled(False)
                self.add_to_roster_check.setChecked(False)
        except Exception as e:
            print(f"Failed to load rosters: {e}")
            self.roster_combo.addItem("Premier", "Premier")

    def _add_to_queue(self):
        """Add current form values to the queue."""
        player_data = {
            'first_name': self.first_name_input.text().strip() or None,
            'last_name': self.last_name_input.text().strip() or None,
            'archetype': self.archetype_combo.currentData(),
            'faction': self.faction_combo.currentData(),
            'random_appearance': self.random_appearance_check.isChecked(),
        }

        self._queue.append(player_data)
        self._refresh_queue_display()

        # Clear form
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.archetype_combo.setCurrentIndex(0)
        self.faction_combo.setCurrentIndex(0)
        self.random_appearance_check.setChecked(False)

        # Focus first name for quick entry
        self.first_name_input.setFocus()

    def _remove_from_queue(self, index: int):
        """Remove a player from the queue."""
        if 0 <= index < len(self._queue):
            self._queue.pop(index)
            self._refresh_queue_display()

    def _clear_queue(self):
        """Clear all players from the queue."""
        self._queue.clear()
        self._refresh_queue_display()

    def _refresh_queue_display(self):
        """Refresh the queue list display."""
        # Clear existing items (except the stretch at the end)
        while self.queue_list_layout.count() > 1:
            item = self.queue_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add items
        for i, player_data in enumerate(self._queue):
            item_widget = QueuedPlayerItem(i, player_data)
            item_widget.remove_clicked.connect(self._remove_from_queue)
            self.queue_list_layout.insertWidget(i, item_widget)

        # Update count
        count = len(self._queue)
        self.queue_count.setText(f"{count} player{'s' if count != 1 else ''}")

        # Enable/disable generate button
        self.generate_btn.setEnabled(count > 0)

    def _on_generate(self):
        """Handle generate button click."""
        if len(self._queue) == 0:
            return

        # Get roster selection
        add_to_roster = self.add_to_roster_check.isChecked()
        roster_name = self.roster_combo.currentData() if add_to_roster else None

        # Emit signal with queue data
        queue_data = {
            'players': list(self._queue),
            'add_to_roster': add_to_roster,
            'roster_name': roster_name,
        }

        self.generate_requested.emit([queue_data])

    def clear_after_generation(self):
        """Clear the queue after successful generation."""
        self._queue.clear()
        self._refresh_queue_display()

    def get_queue(self) -> list:
        """Get the current queue."""
        return list(self._queue)
