"""
Player Finder sidebar widget.

This is the persistent left sidebar that allows searching, browsing,
and viewing players. The selected player can be used by other widgets
(e.g., adding to picker slots).
"""

import os
import random as _random
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QListWidget, QListWidgetItem, QLabel, QPushButton, QFrame,
    QSplitter, QSizePolicy, QDialog, QScrollArea, QGridLayout,
    QCheckBox, QSpinBox, QGroupBox, QStackedWidget, QStyledItemDelegate
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush

from spritopia.players.players import Player
from spritopia.players import archetypes
from spritopia.gui.theme import COLORS, get_archetype_style, get_rarity_style
from spritopia.gui.widgets.player_detail import PlayerDetailWidget
from spritopia.gui.app_state import get_app_state
from spritopia.data_storage.data_storage import d
from spritopia.data_storage import player_filter as pf
from spritopia.common.paths import paths
from spritopia.gui.stats.stats_engine import StatsEngine


def get_player_rosters(sprite_id: int) -> list:
    """Get list of roster names that a player is currently on."""
    rosters = []
    for roster_name, roster_data in d.rosters.items():
        if roster_data and "SpriteIDs" in roster_data:
            if sprite_id in roster_data["SpriteIDs"].values():
                rosters.append(roster_name)
    return rosters

# Value maps for contextual dropdowns
VALUE_COMBO_MAP = {
    "Archetype_Name": {
        "values": ["Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"],
        "sorted": False
    },
    "Rarity": {
        "values": ["Common", "Rare", "Epic", "Legendary", "Godlike"],
        "sorted": False
    },
    "IsOnRoster": {
        "values": lambda: list(d.rosters.keys()) if d.rosters else [],
        "sorted": True,
        "dynamic": True
    },
}

# Operator maps based on field type
OPERATOR_MAP = {
    "default": [
        ("equals", "equals"),
        ("does not equal", "does_not_equal"),
        ("greater than", "greater_than"),
        ("less than", "less_than"),
        ("contains", "contains"),
    ],
    "numeric": [
        ("equals", "equals"),
        ("does not equal", "does_not_equal"),
        ("greater than", "greater_than"),
        ("greater or equal", "greater_than_or_equal_to"),
        ("less than", "less_than"),
        ("less or equal", "less_than_or_equal_to"),
    ],
    "text": [
        ("equals", "equals"),
        ("does not equal", "does_not_equal"),
        ("contains", "contains"),
    ],
    "equality": [
        ("equals", "equals"),
        ("does not equal", "does_not_equal"),
    ],
}

# Field definitions with categories and types
FILTER_FIELDS = [
    # Special
    {"display": "On Roster", "value": "IsOnRoster", "category": "Special", "type": "special", "operators": "equality"},
    # Basic Info
    {"display": "Archetype", "value": "Archetype_Name", "category": "Basic Info", "type": "players", "operators": "equality"},
    {"display": "Rarity", "value": "Rarity", "category": "Basic Info", "type": "players", "operators": "equality"},
    {"display": "Faction", "value": "Faction", "category": "Basic Info", "type": "players", "operators": "text"},
    {"display": "First Name", "value": "First_Name", "category": "Basic Info", "type": "players", "operators": "text"},
    {"display": "Last Name", "value": "Last_Name", "category": "Basic Info", "type": "players", "operators": "text"},
    {"display": "Height", "value": "Height", "category": "Basic Info", "type": "players", "operators": "numeric"},
    {"display": "Weight", "value": "Weight", "category": "Basic Info", "type": "players", "operators": "numeric"},
    # Attributes - key names must match Player._DEFAULTS / CSV column names
    {"display": "Inside Shot", "value": "SShtIns", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Close Range Shot", "value": "SShtCls", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Mid Range Shot", "value": "SShtMed", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "3-Point Shot", "value": "SSht3PT", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Free Throw", "value": "SShtFT", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Layup", "value": "SLayUp", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Dunk", "value": "SDunk", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Standing Dunk", "value": "SStdDunk", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Shot In Traffic", "value": "SShtInT", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Post Fadeaway", "value": "SPstFdaway", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Post Hook", "value": "SPstHook", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Shot Off Dribble", "value": "SShtOfD", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Ball Handle", "value": "SBallHndl", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Off-Hand Dribble", "value": "SOffHDrib", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Ball Security", "value": "SBallSec", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Pass", "value": "SPass", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Block", "value": "SBlock", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Steal", "value": "SSteal", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Hands", "value": "SHands", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "On-Ball Defense", "value": "SOnBallD", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Off Rebound", "value": "SOReb", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Def Rebound", "value": "SDReb", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Off Low Post", "value": "SOLowPost", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Def Low Post", "value": "SDLowPost", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Off Awareness", "value": "SOAwar", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Def Awareness", "value": "SDAwar", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Consistency", "value": "SConsis", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Speed", "value": "SSpeed", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Quickness", "value": "SQuick", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Strength", "value": "SStrength", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Vertical", "value": "SVertical", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Stamina", "value": "SStamina", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Hustle", "value": "SHustle", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Durability", "value": "SDurab", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Potential", "value": "SPOT", "category": "Attributes", "type": "players", "operators": "numeric"},
    {"display": "Emotion", "value": "SEmotion", "category": "Attributes", "type": "players", "operators": "numeric"},
]


class PlayerListItem(QListWidgetItem):
    """Custom list item that holds a Player reference."""

    def __init__(self, player: Player, show_rosters: bool = True):
        super().__init__()
        self.player = player

        # Display text
        first = player["First_Name"] or ""
        last = player["Last_Name"] or ""
        name = f"{first} {last}".strip() or "Unknown"

        archetype = str(player["Archetype"]) if player["Archetype"] else ""
        rarity = player["Rarity"] or "Common"

        # Get roster info
        sprite_id = player["SpriteID"]
        rosters = get_player_rosters(sprite_id) if show_rosters else []
        roster_text = f"  ({', '.join(rosters)})" if rosters else ""

        self.setText(f"{name}{roster_text}")

        # Set archetype color
        if archetype:
            arch_style = get_archetype_style(archetype)
            if arch_style:
                self.setForeground(QBrush(QColor(arch_style["color"])))

        # Set tooltip with more info
        self.setToolTip(f"{name}\n{archetype} · {rarity}")


class AdvancedFilterDialog(QDialog):
    """
    Advanced filter dialog for complex player filtering.
    Allows adding multiple conditions with contextual value inputs.
    """

    # Signal emitted when a speedy filter condition is removed
    speedy_filter_removed = Signal(str)  # Emits field name ("Archetype_Name" or "IsOnRoster")
    # Signal emitted when a speedy filter value is changed
    speedy_filter_changed = Signal(str, object)  # Emits (field_name, new_value)

    def __init__(self, parent=None, existing_conditions: list = None, speedy_conditions: list = None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Filters")
        self.setMinimumSize(620, 420)
        self._conditions = []
        self._speedy_condition_rows = []  # Track which rows are from speedy filters
        self._setup_ui()
        # Add speedy filter conditions first (these sync with quick dropdowns)
        if speedy_conditions:
            for cond_data in speedy_conditions:
                row = self._add_condition_row(initial_data=cond_data, is_speedy=True)
                if row:
                    self._speedy_condition_rows.append(row)
        # Restore existing advanced conditions
        if existing_conditions:
            for cond_data in existing_conditions:
                self._add_condition_row(initial_data=cond_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Apply dark dialog styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_dark']};
            }}
            QLabel {{
                color: {COLORS['text_primary']};
            }}
        """)

        # Header row with title and category filter
        header_row = QHBoxLayout()

        header = QLabel("Advanced Filters")
        header.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text_primary']};")
        header_row.addWidget(header)

        header_row.addStretch()

        # Category filter dropdown
        show_label = QLabel("Show:")
        show_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        header_row.addWidget(show_label)
        self.category_filter = QComboBox()
        self.category_filter.setMinimumHeight(30)
        self.category_filter.setMinimumWidth(110)
        self.category_filter.addItem("All Fields", "All")
        self.category_filter.addItem("Special", "Special")
        self.category_filter.addItem("Basic Info", "Basic Info")
        self.category_filter.addItem("Attributes", "Attributes")
        self.category_filter.currentIndexChanged.connect(self._on_category_changed)
        header_row.addWidget(self.category_filter)

        layout.addLayout(header_row)

        # Scroll area for conditions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(180)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
                background-color: {COLORS['bg_medium']};
            }}
        """)

        self.conditions_widget = QWidget()
        self.conditions_widget.setStyleSheet(f"background-color: {COLORS['bg_medium']};")
        self.conditions_layout = QVBoxLayout(self.conditions_widget)
        self.conditions_layout.setContentsMargins(8, 8, 8, 8)
        self.conditions_layout.setSpacing(6)
        self.conditions_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(self.conditions_widget)
        layout.addWidget(scroll, stretch=1)

        # Add condition button
        add_row = QHBoxLayout()
        add_btn = QPushButton("+ Add Condition")
        add_btn.setMinimumHeight(34)
        add_btn.clicked.connect(lambda: self._add_condition_row())
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #3b8bdb;
            }}
        """)
        add_row.addWidget(add_btn)
        add_row.addStretch()
        layout.addLayout(add_row)

        # Buttons row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        clear_btn = QPushButton("Clear All")
        clear_btn.setMinimumHeight(34)
        clear_btn.clicked.connect(self._clear_conditions)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_dark']};
                padding: 8px 14px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_light']};
            }}
        """)
        btn_layout.addWidget(clear_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(34)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border_dark']};
                padding: 8px 18px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_card']};
            }}
        """)
        btn_layout.addWidget(cancel_btn)

        apply_btn = QPushButton("Apply Filters")
        apply_btn.setMinimumHeight(34)
        apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white;
                padding: 8px 20px;
                font-weight: bold;
                border-radius: 4px;
                border: none;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #0ea570;
            }}
        """)
        apply_btn.clicked.connect(self.accept)
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

    def _on_category_changed(self):
        """Update all condition rows when category filter changes."""
        category = self.category_filter.currentData()
        for row in self._conditions:
            row.set_category_filter(category)

    def _add_condition_row(self, initial_data: dict = None, is_speedy: bool = False):
        """Add a new condition row, optionally with initial data."""
        category = self.category_filter.currentData()
        row = ConditionRow(category_filter=category, initial_data=initial_data, is_speedy=is_speedy, parent=self)
        row.remove_clicked.connect(lambda r=row: self._remove_condition(r))

        # Connect value change signal for speedy filter rows
        if is_speedy:
            row.value_changed.connect(self.speedy_filter_changed.emit)

        self.conditions_layout.addWidget(row)
        self._conditions.append(row)
        return row

    def _remove_condition(self, row):
        """Remove a condition row."""
        if row in self._conditions:
            # Check if this is a speedy filter row
            if row in self._speedy_condition_rows:
                self._speedy_condition_rows.remove(row)
                # Get the field to notify which speedy filter to reset
                raw_data = row.get_raw_data()
                if raw_data:
                    self.speedy_filter_removed.emit(raw_data.get("field", ""))
            self._conditions.remove(row)
            row.deleteLater()

    def _clear_conditions(self):
        """Clear all conditions."""
        # Emit signals for any speedy filter rows being removed
        for row in self._speedy_condition_rows:
            raw_data = row.get_raw_data()
            if raw_data:
                self.speedy_filter_removed.emit(raw_data.get("field", ""))

        for row in self._conditions[:]:
            row.deleteLater()
        self._conditions.clear()
        self._speedy_condition_rows.clear()

    def get_raw_conditions(self, include_speedy: bool = True) -> list:
        """Get the raw condition data for persistence."""
        raw_data = []
        for row in self._conditions:
            # Optionally skip speedy filter rows
            if not include_speedy and row in self._speedy_condition_rows:
                continue
            data = row.get_raw_data()
            if data:
                raw_data.append(data)
        return raw_data

    def get_filter_condition(self) -> dict:
        """Build the filter condition dict from all rows."""
        if not self._conditions:
            return {}

        conditions = []
        for row in self._conditions:
            cond = row.get_condition()
            if cond:
                conditions.append(cond)

        if not conditions:
            return {}
        elif len(conditions) == 1:
            return conditions[0]
        else:
            return {"type": "and", "conditions": conditions}


class ConditionRow(QFrame):
    """A single condition row with contextual value inputs."""

    remove_clicked = Signal()
    value_changed = Signal(str, object)  # Emits (field_name, new_value) when speedy filter value changes

    def __init__(self, category_filter: str = "All", initial_data: dict = None, is_speedy: bool = False, parent=None):
        super().__init__(parent)
        self._category_filter = category_filter
        self._initial_data = initial_data
        self._is_speedy = is_speedy
        self.setFixedHeight(46)

        # Different styling for speedy filter rows
        if is_speedy:
            self.setStyleSheet(f"""
                ConditionRow {{
                    background-color: {COLORS['bg_light']};
                    border: 1px solid {COLORS['accent_primary']};
                    border-radius: 4px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                ConditionRow {{
                    background-color: {COLORS['bg_card']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 4px;
                }}
            """)
        self._setup_ui()
        self._update_field_choices()
        # Apply initial data after setup
        if initial_data:
            self._apply_initial_data(initial_data)

        # Lock field and operator for speedy filter rows
        if is_speedy:
            self.field_combo.setEnabled(False)
            self.operator_combo.setEnabled(False)
            # Connect value change signals for syncing
            self.value_combo.currentIndexChanged.connect(self._on_speedy_value_changed)
            self.value_input.textChanged.connect(self._on_speedy_value_changed)

    def _on_speedy_value_changed(self):
        """Emit signal when speedy filter value changes."""
        if not self._is_speedy:
            return
        field_data = self.field_combo.currentData()
        if not field_data:
            return
        field_name = field_data.get("value", "")
        # Get current value
        if self.value_stack.currentIndex() == 1:
            value = self.value_combo.currentData()
            if value is None:
                value = self.value_combo.currentText()
        else:
            value = self.value_input.text().strip()
        self.value_changed.emit(field_name, value)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        # Speedy indicator label
        if self._is_speedy:
            speedy_label = QLabel("⚡")
            speedy_label.setToolTip("Quick filter - synced with dropdown above")
            speedy_label.setStyleSheet(f"color: {COLORS['accent_primary']}; font-size: 12px;")
            layout.addWidget(speedy_label)

        # Field selector
        self.field_combo = QComboBox()
        self.field_combo.setMinimumHeight(32)
        self.field_combo.setMinimumWidth(120)
        self.field_combo.currentIndexChanged.connect(self._on_field_changed)
        layout.addWidget(self.field_combo)

        # Operator selector
        self.operator_combo = QComboBox()
        self.operator_combo.setMinimumHeight(32)
        self.operator_combo.setMinimumWidth(100)
        layout.addWidget(self.operator_combo)

        # Value input - stacked widget for combo or line edit
        self.value_stack = QStackedWidget()
        self.value_stack.setMinimumHeight(32)
        self.value_stack.setMinimumWidth(120)

        # Text input (index 0)
        self.value_input = QLineEdit()
        self.value_input.setMinimumHeight(32)
        self.value_input.setPlaceholderText("Value...")
        self.value_stack.addWidget(self.value_input)

        # Combo input (index 1)
        self.value_combo = QComboBox()
        self.value_combo.setMinimumHeight(32)
        self.value_stack.addWidget(self.value_combo)

        layout.addWidget(self.value_stack, stretch=1)

        # Remove button
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(28, 28)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_danger']};
                border: 1px solid {COLORS['accent_danger']};
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_danger']};
                color: white;
            }}
        """)
        remove_btn.clicked.connect(self.remove_clicked.emit)
        layout.addWidget(remove_btn)

    def _apply_initial_data(self, data: dict):
        """Apply initial data to restore a condition."""
        # Find and set the field
        field_value = data.get("field", "")
        for i in range(self.field_combo.count()):
            field_data = self.field_combo.itemData(i)
            if field_data and field_data.get("value") == field_value:
                self.field_combo.setCurrentIndex(i)
                break

        # Set the operator
        operator = data.get("operator", "equals")
        for i in range(self.operator_combo.count()):
            if self.operator_combo.itemData(i) == operator:
                self.operator_combo.setCurrentIndex(i)
                break

        # Set the value
        value = data.get("value", "")
        if self.value_stack.currentIndex() == 1:
            # Combo box value
            for i in range(self.value_combo.count()):
                if self.value_combo.itemData(i) == value or self.value_combo.itemText(i) == str(value):
                    self.value_combo.setCurrentIndex(i)
                    break
        else:
            # Text input value
            self.value_input.setText(str(value))

    def set_category_filter(self, category: str):
        """Update the category filter and refresh field choices."""
        self._category_filter = category
        self._update_field_choices()

    def _update_field_choices(self):
        """Update field dropdown based on category filter."""
        self.field_combo.blockSignals(True)
        current_value = self.field_combo.currentData()
        self.field_combo.clear()

        for field in FILTER_FIELDS:
            if self._category_filter == "All" or field["category"] == self._category_filter:
                self.field_combo.addItem(field["display"], field)

        # Try to restore previous selection
        if current_value:
            for i in range(self.field_combo.count()):
                if self.field_combo.itemData(i).get("value") == current_value.get("value"):
                    self.field_combo.setCurrentIndex(i)
                    break

        self.field_combo.blockSignals(False)
        self._on_field_changed()

    def _on_field_changed(self):
        """Update operators and value input based on selected field."""
        field_data = self.field_combo.currentData()
        if not field_data:
            return

        # Update operators
        operator_type = field_data.get("operators", "default")
        operators = OPERATOR_MAP.get(operator_type, OPERATOR_MAP["default"])

        self.operator_combo.blockSignals(True)
        current_op = self.operator_combo.currentData()
        self.operator_combo.clear()
        for display, value in operators:
            self.operator_combo.addItem(display, value)
        # Try to restore
        for i in range(self.operator_combo.count()):
            if self.operator_combo.itemData(i) == current_op:
                self.operator_combo.setCurrentIndex(i)
                break
        self.operator_combo.blockSignals(False)

        # Update value input - check if we have a combo map for this field
        field_value = field_data.get("value", "")
        combo_config = VALUE_COMBO_MAP.get(field_value)

        if combo_config:
            # Use combo box
            values = combo_config["values"]
            if callable(values):
                values = values()  # Dynamic values

            if combo_config.get("sorted", False) and values:
                values = sorted(values)

            self.value_combo.clear()
            for v in values:
                self.value_combo.addItem(str(v), v)

            self.value_stack.setCurrentIndex(1)  # Show combo
        else:
            # Use text input
            self.value_stack.setCurrentIndex(0)  # Show text

    def get_raw_data(self) -> dict:
        """Get the raw data from this row for persistence."""
        field_data = self.field_combo.currentData()
        if not field_data:
            return None

        operator = self.operator_combo.currentData()
        field_value = field_data.get("value", "")

        # Get value from appropriate widget
        if self.value_stack.currentIndex() == 1:
            value = self.value_combo.currentData()
            if value is None:
                value = self.value_combo.currentText()
        else:
            value = self.value_input.text().strip()

        if not value and value != 0:
            return None

        return {
            "field": field_value,
            "operator": operator,
            "value": value
        }

    def get_condition(self) -> dict:
        """Get the condition dict for this row."""
        field_data = self.field_combo.currentData()
        if not field_data:
            return None

        operator = self.operator_combo.currentData()
        field_value = field_data.get("value", "")
        field_type = field_data.get("type", "players")

        # Get value from appropriate widget
        if self.value_stack.currentIndex() == 1:
            value = self.value_combo.currentData()
            if value is None:
                value = self.value_combo.currentText()
        else:
            value = self.value_input.text().strip()

        if not value and value != 0:
            return None

        # Try to convert to number if applicable
        if isinstance(value, str):
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # Keep as string

        # Build condition based on field type
        if field_type == "special":
            # Special fields like IsOnRoster
            condition = {
                "type": "special",
                "field": field_value,
                "value": value
            }
            # Handle "does not equal" for special
            if operator == "does_not_equal":
                return {"type": "not", "condition": condition}
            return condition
        else:
            return {
                "type": operator,
                "domain": "Players",
                "field": field_value,
                "value": value
            }


class PlayerFinderWidget(QWidget):
    """
    The main player finder sidebar.

    Contains:
    - Search box
    - Quick filter dropdowns (Archetype, Roster)
    - Advanced filter button
    - Scrollable player list
    - Selected player detail view
    """

    player_selected = Signal(object)  # Emits Player when selection changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_players = []
        self._filtered_players = []
        self._advanced_condition = {}
        self._advanced_raw_conditions = []  # Store raw conditions for persistence
        self._available_rosters = []
        # Game-mode constraints (set by Premier match setup)
        self._constrained_ids: Optional[set] = None  # If set, only these IDs are eligible
        self._banned_ids: set = set()                 # Pre-game exile bans
        self._draft_excluded_ids: set = set()         # Live draft picks/bans (removed mid-draft)
        self._pool_draw_size: Optional[int] = None    # Random cull after all other filters
        self._slot_archetype: Optional[str] = None    # Active pick slot archetype override
        self._setup_ui()
        self._connect_signals()
        self._load_rosters()

    def _setup_ui(self):
        self.setMinimumWidth(320)
        self.setMaximumWidth(400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header - more compact
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 8, 10, 8)
        header_layout.setSpacing(6)

        # Title row with advanced filter button - compact
        title_row = QHBoxLayout()
        title_row.setSpacing(8)
        title = QLabel("Player Finder")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title_row.addWidget(title)

        title_row.addStretch()

        self.advanced_btn = QPushButton("⚙ Filters")
        self.advanced_btn.setFixedHeight(24)
        self.advanced_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_dark']};
                padding: 2px 10px;
                border-radius: 4px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
            }}
        """)
        self.advanced_btn.clicked.connect(self._open_advanced_filters)
        title_row.addWidget(self.advanced_btn)

        header_layout.addLayout(title_row)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setMinimumHeight(32)
        self.search_input.setPlaceholderText("Search players...")
        self.search_input.setClearButtonEnabled(True)
        header_layout.addWidget(self.search_input)

        # Quick filters row
        filters_row = QHBoxLayout()
        filters_row.setSpacing(6)

        # Archetype filter
        self.archetype_filter = QComboBox()
        self.archetype_filter.setMinimumHeight(30)
        self.archetype_filter.addItem("All Archetypes", None)
        self.archetype_filter.addItem("Slayer", "Slayer")
        self.archetype_filter.addItem("Vigilante", "Vigilante")
        self.archetype_filter.addItem("Medic", "Medic")
        self.archetype_filter.addItem("Guardian", "Guardian")
        self.archetype_filter.addItem("Engineer", "Engineer")
        self.archetype_filter.addItem("Director", "Director")
        filters_row.addWidget(self.archetype_filter)

        # Roster filter
        self.roster_filter = QComboBox()
        self.roster_filter.setMinimumHeight(30)
        self.roster_filter.addItem("All Players", None)
        # Rosters will be populated dynamically
        filters_row.addWidget(self.roster_filter)

        header_layout.addLayout(filters_row)

        # Result count and active filter indicator - compact single row
        count_row = QHBoxLayout()
        count_row.setSpacing(4)

        self.count_label = QLabel("0 players")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        count_row.addWidget(self.count_label)

        count_row.addStretch()

        self.filter_indicator = QLabel("")
        self.filter_indicator.setStyleSheet(f"color: {COLORS['accent_primary']}; font-size: 10px;")
        count_row.addWidget(self.filter_indicator)

        header_layout.addLayout(count_row)

        layout.addWidget(header)

        # Splitter for list and detail
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_dark']};
                height: 3px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['accent_primary']};
            }}
        """)

        # Player list
        self.player_list = QListWidget()
        self.player_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_dark']};
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 5px 10px;
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
                color: white;
            }}
            QListWidget::item:hover:!selected {{
                background-color: {COLORS['bg_light']};
            }}
        """)
        self.splitter.addWidget(self.player_list)

        # Player detail view
        self.detail_view = PlayerDetailWidget()
        self.splitter.addWidget(self.detail_view)

        # Set initial splitter sizes (list takes ~30%, detail takes ~70%)
        self.splitter.setSizes([150, 350])

        layout.addWidget(self.splitter)

    def _connect_signals(self):
        """Connect internal signals."""
        self.search_input.textChanged.connect(self._on_filter_changed)
        self.archetype_filter.currentIndexChanged.connect(self._on_filter_changed)
        self.roster_filter.currentIndexChanged.connect(self._on_filter_changed)
        self.player_list.currentItemChanged.connect(self._on_selection_changed)

        # Connect to app state
        app_state = get_app_state()
        app_state.player_list_changed.connect(self._on_player_list_updated)

    def _load_rosters(self):
        """Load available rosters from the data storage."""
        self.roster_filter.blockSignals(True)
        self.roster_filter.clear()
        self.roster_filter.addItem("All Players", None)

        try:
            # First, look for roster folders in rosterCSVs (exported/working rosters)
            roster_csvs_path = paths.get("rosterCSVs")
            if roster_csvs_path and os.path.exists(roster_csvs_path):
                for folder in os.listdir(roster_csvs_path):
                    folder_path = os.path.join(roster_csvs_path, folder)
                    if os.path.isdir(folder_path):
                        # Check if it has the expected CSV files
                        players_csv = os.path.join(folder_path, "Players.csv")
                        if os.path.exists(players_csv):
                            self.roster_filter.addItem(folder, folder)
                            self._available_rosters.append(folder)

            # If no rosters found, try looking for .ROS files in gameRosters
            if not self._available_rosters:
                rosters_path = paths.get("gameRosters")
                if rosters_path and os.path.exists(rosters_path):
                    for file in os.listdir(rosters_path):
                        if file.endswith(".ROS"):
                            roster_name = file.replace(".ROS", "")
                            self.roster_filter.addItem(roster_name, roster_name)
                            self._available_rosters.append(roster_name)

            # Default to Premier if available
            premier_idx = self.roster_filter.findData("Premier")
            if premier_idx >= 0:
                self.roster_filter.setCurrentIndex(premier_idx)
        except Exception:
            pass

        self.roster_filter.blockSignals(False)

    def _open_advanced_filters(self):
        """Open the advanced filter dialog."""
        # Build speedy conditions from current quick filter states
        speedy_conditions = []
        archetype = self.archetype_filter.currentData()
        roster = self.roster_filter.currentData()

        if archetype:
            speedy_conditions.append({
                "field": "Archetype_Name",
                "operator": "equals",
                "value": archetype
            })
        if roster:
            speedy_conditions.append({
                "field": "IsOnRoster",
                "operator": "equals",
                "value": roster
            })

        dialog = AdvancedFilterDialog(
            self,
            existing_conditions=self._advanced_raw_conditions,
            speedy_conditions=speedy_conditions
        )

        # Connect signals to handle speedy filter changes
        dialog.speedy_filter_removed.connect(self._on_speedy_filter_removed)
        dialog.speedy_filter_changed.connect(self._on_speedy_filter_changed)

        if dialog.exec() == QDialog.Accepted:
            # Get only non-speedy conditions for persistence
            self._advanced_raw_conditions = dialog.get_raw_conditions(include_speedy=False)
            self._advanced_condition = dialog.get_filter_condition()
            self._update_filter_indicator()
            self._apply_filters()

    def _on_speedy_filter_removed(self, field: str):
        """Handle removal of a speedy filter row - reset the corresponding dropdown."""
        if field == "Archetype_Name":
            self.archetype_filter.blockSignals(True)
            self.archetype_filter.setCurrentIndex(0)  # "All Archetypes"
            self.archetype_filter.blockSignals(False)
        elif field == "IsOnRoster":
            self.roster_filter.blockSignals(True)
            self.roster_filter.setCurrentIndex(0)  # "All Players"
            self.roster_filter.blockSignals(False)

    def _on_speedy_filter_changed(self, field: str, value):
        """Handle value change in a speedy filter row - update the corresponding dropdown."""
        if field == "Archetype_Name":
            self.archetype_filter.blockSignals(True)
            idx = self.archetype_filter.findData(value)
            if idx >= 0:
                self.archetype_filter.setCurrentIndex(idx)
            self.archetype_filter.blockSignals(False)
        elif field == "IsOnRoster":
            self.roster_filter.blockSignals(True)
            idx = self.roster_filter.findData(value)
            if idx >= 0:
                self.roster_filter.setCurrentIndex(idx)
            self.roster_filter.blockSignals(False)

    def _update_filter_indicator(self):
        """Update the filter indicator based on current filters."""
        total_filters = len(self._advanced_raw_conditions)
        archetype = self.archetype_filter.currentData()
        roster = self.roster_filter.currentData()

        if archetype:
            total_filters += 1
        if roster:
            total_filters += 1

        if total_filters > 0:
            self.filter_indicator.setText(f"⚡ {total_filters} filter{'s' if total_filters > 1 else ''}")
            # Style the advanced button to show filters are active
            self.advanced_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_primary']};
                    color: white;
                    border: none;
                    padding: 2px 10px;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #3b8bdb;
                }}
            """)
        else:
            self.filter_indicator.setText("")
            self.advanced_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_secondary']};
                    border: 1px solid {COLORS['border_dark']};
                    padding: 2px 10px;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['bg_card']};
                    color: {COLORS['text_primary']};
                }}
            """)

    def set_players(self, players: list):
        """Set the full list of players to display."""
        self._all_players = list(players)
        self._apply_filters()

    def _on_player_list_updated(self):
        """Handle updates from app state."""
        app_state = get_app_state()
        self.set_players(app_state.players)

    def _on_filter_changed(self):
        """Handle filter/search changes."""
        self._update_filter_indicator()
        self._apply_filters()

    def _apply_filters(self):
        """Apply current filters to the player list."""
        search_text = self.search_input.text().lower().strip()
        archetype_filter = self.archetype_filter.currentData()
        roster_filter = self.roster_filter.currentData()

        self._filtered_players = []

        # Build condition for player_filter system
        conditions = []

        # Archetype condition
        if archetype_filter:
            conditions.append({
                "type": "equals",
                "domain": "Players",
                "field": "Archetype_Name",
                "value": archetype_filter
            })

        # Roster condition (special type)
        if roster_filter:
            # Make sure roster is loaded
            if roster_filter not in d.rosters:
                try:
                    d.csv_ImportCSVs(roster_filter)
                except Exception:
                    pass

            conditions.append({
                "type": "special",
                "field": "IsOnRoster",
                "value": roster_filter
            })

        # Add advanced conditions
        if self._advanced_condition:
            conditions.append(self._advanced_condition)

        # Build combined condition
        if conditions:
            combined = {"type": "and", "conditions": conditions} if len(conditions) > 1 else conditions[0]
        else:
            combined = {}

        # Get filtered sprite IDs using player_filter
        try:
            filtered_ids = pf.filterSpriteIDs(combined)
            filtered_set = set(filtered_ids)
        except Exception as e:
            print(f"[PlayerFinder] Filter error: {e}")
            filtered_set = set(p["SpriteID"] for p in self._all_players)

        # Apply game-mode constraints
        if self._constrained_ids is not None:
            filtered_set &= self._constrained_ids
        if self._banned_ids:
            filtered_set -= self._banned_ids
        if self._draft_excluded_ids:
            filtered_set -= self._draft_excluded_ids

        # Apply active slot archetype override (from draft pick type)
        if self._slot_archetype:
            arch_ids = {
                p["SpriteID"] for p in self._all_players
                if (p["Archetype_Name"] or "").lower() == self._slot_archetype.lower()
            }
            filtered_set &= arch_ids

        # Apply search text filter on top
        for player in self._all_players:
            # Check if player passes the condition filter
            if player["SpriteID"] not in filtered_set:
                continue

            # Search filter
            if search_text:
                first = (player["First_Name"] or "").lower()
                last = (player["Last_Name"] or "").lower()
                full_name = f"{first} {last}"
                if search_text not in full_name:
                    continue

            self._filtered_players.append(player)

        # Apply pool draw (random cull) last
        if self._pool_draw_size and len(self._filtered_players) > self._pool_draw_size:
            self._filtered_players = _random.sample(self._filtered_players, self._pool_draw_size)

        self._update_list()

    def _update_list(self):
        """Update the list widget with filtered players."""
        self.player_list.clear()

        for player in self._filtered_players:
            item = PlayerListItem(player)
            self.player_list.addItem(item)

        self.count_label.setText(f"{len(self._filtered_players)} players")

    def _on_selection_changed(self, current, previous):
        """Handle player selection changes."""
        if current is None:
            self.detail_view.set_player(None)
            get_app_state().selected_player = None
            self.player_selected.emit(None)
            return

        if isinstance(current, PlayerListItem):
            player = current.player
            self.detail_view.set_player(player)
            get_app_state().selected_player = player
            self.player_selected.emit(player)

    def get_selected_player(self) -> Player:
        """Get the currently selected player."""
        current = self.player_list.currentItem()
        if isinstance(current, PlayerListItem):
            return current.player
        return None

    def select_player(self, player: Player):
        """Programmatically select a player."""
        for i in range(self.player_list.count()):
            item = self.player_list.item(i)
            if isinstance(item, PlayerListItem) and item.player == player:
                self.player_list.setCurrentItem(item)
                break

    def clear_selection(self):
        """Clear the current selection."""
        self.player_list.clearSelection()
        self.detail_view.set_player(None)

    # ── Game-mode constraint API ──────────────────────────────────────────────

    def set_game_constraints(self, config: dict):
        """
        Apply Premier match setup constraints to the player list.
        Called when a match starts; compounds with the existing filter UI.
        """
        RARITY_ORDER = ["Common", "Rare", "Epic", "Legendary", "Godlike"]

        constrained_ids: Optional[set] = None
        banned_ids: set = set()

        # Load Premier-only stats engine once if needed
        player_set = config.get("player_set", "Standard")
        stats_engine: Optional[StatsEngine] = None
        if config.get("veterans_only") or config.get("exile_mode") or player_set == "Standard":
            stats_engine = self._load_premier_stats_engine()

        # Standard player set: restrict sidebar to players with >= 1 Premier game
        if player_set == "Standard" and stats_engine and not config.get("veterans_only"):
            standard_ids = {
                cs.sprite_id
                for cs in stats_engine.get_all_career_stats()
                if cs.games_played >= 1
            }
            constrained_ids = standard_ids

        # Veterans Only: players with 20+ Premier games
        if config.get("veterans_only") and stats_engine:
            veteran_ids = {
                cs.sprite_id
                for cs in stats_engine.get_all_career_stats()
                if cs.games_played >= 20
            }
            constrained_ids = veteran_ids

        # Rarity Cap: restrict to at-or-below tier
        rarity_cap = config.get("rarity_cap")  # e.g. "Rare" means Common+Rare eligible
        if rarity_cap and rarity_cap in RARITY_ORDER:
            cap_idx = RARITY_ORDER.index(rarity_cap)
            allowed_rarities = set(RARITY_ORDER[:cap_idx + 1])
            rarity_ids = {
                p["SpriteID"] for p in d.players.values()
                if (p["Rarity"] or "Common") in allowed_rarities
            }
            constrained_ids = rarity_ids if constrained_ids is None else (constrained_ids & rarity_ids)

        # Exile Mode: ban every player from the most recent Premier game
        if config.get("exile_mode") and stats_engine:
            premier_games = stats_engine.get_games()  # Already sorted newest-first
            if premier_games:
                last_game = premier_games[0]
                for slot_info in last_game.player_slots.values():
                    if slot_info.get("IsActive"):
                        sid = slot_info.get("SpriteID", -1)
                        if sid is not None and sid >= 0:
                            banned_ids.add(sid)

        # Pool Draw size (random cull applied as a last step in _apply_filters)
        pool_draw = config.get("pool_draw")  # int or None from _build_config
        self._pool_draw_size = pool_draw if isinstance(pool_draw, int) and pool_draw > 0 else None

        self._constrained_ids = constrained_ids
        self._banned_ids = banned_ids
        self._apply_filters()

    def clear_game_constraints(self):
        """Remove all game-mode constraints (called when returning to setup)."""
        self._constrained_ids = None
        self._banned_ids = set()
        self._draft_excluded_ids = set()
        self._pool_draw_size = None
        self._slot_archetype = None
        self._apply_filters()

    def set_slot_archetype(self, archetype: Optional[str]):
        """
        Restrict the visible player list to a specific archetype for the current
        pick slot. Pass None or "" to clear the restriction.
        Called by the draft picker as each turn begins.
        """
        self._slot_archetype = archetype if archetype else None
        self._apply_filters()

    def set_draft_excluded(self, ids: set):
        """
        Exclude already-picked and already-banned players from the visible list.
        Called after each pick/ban during the draft.
        """
        self._draft_excluded_ids = set(ids)
        self._apply_filters()

    def _load_premier_stats_engine(self) -> Optional[StatsEngine]:
        """Build a StatsEngine scoped only to Premier.ROS games."""
        try:
            if not hasattr(d, 'stats') or not d.stats.get("Raw"):
                d.statsDB_Open()
                d.statsDB_DownloadRaw()

            raw_stats = d.stats.get("Raw", {})
            if not raw_stats:
                return None

            premier_raw = {
                gid: ginfo for gid, ginfo in raw_stats.items()
                if "Premier" in (ginfo.get("LoadedRoster") or "")
            }
            return StatsEngine(premier_raw, d.players) if premier_raw else None
        except Exception as e:
            print(f"[PlayerFinder] Failed to load Premier stats: {e}")
            return None

    # ── Programmatic selection ────────────────────────────────────────────────

    def select_player_by_id(self, sprite_id: int):
        """Programmatically select a player by their sprite ID."""
        # First check if player is in current filtered list
        for i in range(self.player_list.count()):
            item = self.player_list.item(i)
            if isinstance(item, PlayerListItem) and item.player["SpriteID"] == sprite_id:
                self.player_list.setCurrentItem(item)
                return True

        # If not found in filtered list, clear filters and try again
        self.search_input.clear()
        self.archetype_filter.setCurrentIndex(0)  # All Archetypes
        self.roster_filter.setCurrentIndex(0)  # All Players
        self._advanced_condition = {}
        self._advanced_raw_conditions = []
        self._update_filter_indicator()
        self._apply_filters()

        # Now try to find and select
        for i in range(self.player_list.count()):
            item = self.player_list.item(i)
            if isinstance(item, PlayerListItem) and item.player["SpriteID"] == sprite_id:
                self.player_list.setCurrentItem(item)
                return True

        return False
