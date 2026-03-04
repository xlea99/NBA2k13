"""
Play Widget - Match setup and picker flow for Premier mode.

Flow: Game Setup screen → (Start Match) → Draft/Picker screen → (Start Game) → Game Screen
"""

import random

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QCheckBox, QLineEdit, QSpinBox,
    QScrollArea, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from spritopia.gui.theme import COLORS, get_archetype_color
from spritopia.gui.premier.picker import PremierPickerWidget
from spritopia.gui.premier.game_screen import GameScreen


# ── Data ─────────────────────────────────────────────────────────────────────

DRAFT_ORDERS = {
    "Classic":
        "Alternating single picks. All bans (if any) are completed before picks begin.",
    "Smite":
        "Half of bans happen before picks (1-2-1 snake), then remaining bans, then another 1-2-1 snake.",
    "Danny-First":
        "All bans first. Danny selects his full team, then Alex selects his full team.",
    "Alex-First":
        "All bans first. Alex selects his full team, then Danny selects his full team.",
    "2-4-2":
        "All bans first. Team 1 gets 2 picks, Team 2 gets 4 picks, Team 1 gets the final 2 picks.",
}

DRAFT_CONTENTS = {
    "Normal":
        "Every pick is a free selection from the available pool.",
    "Random":
        "Every pick is automatically filled with a random player.",
    "Semi-Random":
        "Alternating normal and random picks.",
    "Archetypal-Random":
        "Every pick pulls a random player of a randomly assigned archetype.",
    "Captains":
        "First pick per team is random. All others are free selections.",
    "Affirmative-Action":
        "Last pick for each team is forced random.",
    "Archetype Showdown":
        "Each team is locked to one randomly assigned archetype for all their picks.",
    "Spritopian Duos":
        "Each team is assigned one shooter archetype and one non-shooter archetype, alternating between them.",
    "Chaos":
        "Every pick slot is independently and randomly assigned its own rule.",
    "Choice":
        "Each pick presents 2 random players — choose the one you want.",
    "Choice 3":
        "Each pick presents 3 random players — choose the one you want.",
}

PICK_TYPE_OPTIONS = [
    "Normal", "Random", "Choice", "Choice 3",
    "Archetype (Random)", "Archetype (Slayer)", "Archetype (Vigilante)",
    "Archetype (Medic)", "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)",
]

# Randomized presets - we show a sample preview with a note
RANDOM_PRESETS = {"Archetype Showdown", "Spritopian Duos", "Chaos"}

MODIFIERS = [
    {
        "key": "rarity_cap",
        "label": "Rarity Cap",
        "type": "dropdown",
        "options": ["No Cap", "Common Only", "Rare & Below", "Epic & Below", "Legendary & Below"],
        "description": "Restricts picks to players at or below this rarity tier. 'Common Only' is pure vanilla — no artifacts.",
    },
    {
        "key": "pool_draw",
        "label": "Pool Draw",
        "type": "dropdown",
        "options": ["Full Roster", "16 Players", "12 Players", "8 Players"],
        "description": "The available pool is randomly culled to this size before drafting. Creates scarcity and forces adaptation.",
    },
    {
        "key": "exile_mode",
        "label": "Exile Mode",
        "type": "checkbox",
        "description": "Players who appeared in the most recent game are banned. Forces fresh blood every session.",
    },
    {
        "key": "wild_card_slot",
        "label": "Wild Card Slot",
        "type": "checkbox",
        "description": "After all picks are locked, one random slot per team is secretly swapped for a completely random player.",
    },
    {
        "key": "archetype_mirror",
        "label": "Archetype Mirror",
        "type": "checkbox",
        "description": "Team 2 must draft players matching Team 1's archetypes in pick order. Same archetypes, different players.",
    },
    {
        "key": "veterans_only",
        "label": "Veterans Only",
        "type": "checkbox",
        "description": "Only players with 20 or more career games are eligible. Rookies sit this one out.",
    },
    {
        "key": "draft_lottery",
        "label": "Draft Lottery",
        "type": "checkbox",
        "description": "Pick order is fully randomized each round rather than snaking. Neither player knows who's up next.",
    },
]


# ── Pick slot generation ──────────────────────────────────────────────────────

def gen_pick_slots(preset: str, player_count: int) -> list:
    """Generate the pick slot type list for each slot (Ballerz first, then Ringers)."""
    total = player_count * 2
    slots = []

    if preset == "Normal":
        slots = ["Normal"] * total

    elif preset == "Random":
        slots = ["Random"] * total

    elif preset == "Semi-Random":
        for i in range(total):
            slots.append("Normal" if i % 2 == 0 else "Random")

    elif preset == "Archetypal-Random":
        archs = ["Archetype (Slayer)", "Archetype (Vigilante)", "Archetype (Medic)",
                 "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)"]
        slots = [random.choice(archs) for _ in range(total)]

    elif preset == "Captains":
        for i in range(total):
            slots.append("Random" if (i == 0 or i == player_count) else "Normal")

    elif preset == "Affirmative-Action":
        for i in range(total):
            slots.append("Random" if (i == player_count - 1 or i == total - 1) else "Normal")

    elif preset == "Archetype Showdown":
        archs = ["Archetype (Slayer)", "Archetype (Vigilante)", "Archetype (Medic)",
                 "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)"]
        b, r = random.choice(archs), random.choice(archs)
        slots = [b] * player_count + [r] * player_count

    elif preset == "Spritopian Duos":
        shooters = ["Archetype (Slayer)", "Archetype (Vigilante)"]
        non = ["Archetype (Medic)", "Archetype (Guardian)",
               "Archetype (Engineer)", "Archetype (Director)"]
        b1, b2 = random.choice(shooters), random.choice(non)
        r1, r2 = random.choice(shooters), random.choice(non)
        for i in range(player_count):
            slots.append(b1 if i % 2 == 0 else b2)
        for i in range(player_count):
            slots.append(r1 if i % 2 == 0 else r2)

    elif preset == "Chaos":
        slots = [random.choice(PICK_TYPE_OPTIONS) for _ in range(total)]

    elif preset == "Choice":
        slots = ["Choice"] * total

    elif preset == "Choice 3":
        slots = ["Choice 3"] * total

    else:
        slots = ["Normal"] * total

    return slots


def _slot_short_label(slot_type: str) -> str:
    if slot_type == "Normal":
        return "Normal"
    if slot_type == "Random":
        return "Random"
    if slot_type == "Choice":
        return "Choice"
    if slot_type == "Choice 3":
        return "3-Way"
    if slot_type == "Archetype (Random)":
        return "Rnd Arch"
    if slot_type.startswith("Archetype ("):
        return slot_type[len("Archetype ("):-1]
    return slot_type


def _slot_chip_colors(slot_type: str):
    """Returns (bg, text) colors for a pick slot chip."""
    if slot_type == "Normal":
        return COLORS['bg_light'], COLORS['text_secondary']
    if slot_type == "Random":
        return COLORS['accent_warning'], "#1a1a1a"
    if slot_type in ("Choice", "Choice 3"):
        return "#06b6d4", "#ffffff"
    if "Archetype" in slot_type:
        return COLORS['accent_primary'], "#ffffff"
    return COLORS['bg_light'], COLORS['text_secondary']


# ── Style constants ───────────────────────────────────────────────────────────

def _spinbox_style() -> str:
    return f"""
        QSpinBox {{
            background-color: {COLORS['bg_medium']};
            border: 1px solid {COLORS['border_dark']};
            border-radius: 4px;
            padding: 4px 6px;
            font-size: 13px;
            color: {COLORS['text_primary']};
        }}
        QSpinBox:focus {{
            border-color: {COLORS['accent_primary']};
        }}
        QSpinBox::up-button {{
            background-color: {COLORS['bg_light']};
            border-left: 1px solid {COLORS['border_dark']};
            border-bottom: 1px solid {COLORS['border_dark']};
            border-top-right-radius: 4px;
            width: 22px;
        }}
        QSpinBox::down-button {{
            background-color: {COLORS['bg_light']};
            border-left: 1px solid {COLORS['border_dark']};
            border-bottom-right-radius: 4px;
            width: 22px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background-color: {COLORS['accent_primary']};
        }}
        QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
            background-color: {COLORS['accent_primary']};
        }}
    """


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
        QComboBox::drop-down {{ border: none; width: 16px; }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['bg_medium']};
            border: 1px solid {COLORS['border_dark']};
            selection-background-color: {COLORS['accent_primary']};
            font-size: 13px;
        }}
    """


# ── Helper builders ───────────────────────────────────────────────────────────

def _make_label(text: str, style: str = "", fixed_width: int = 0) -> QLabel:
    lbl = QLabel(text)
    if style:
        lbl.setStyleSheet(style)
    if fixed_width:
        lbl.setFixedWidth(fixed_width)
    return lbl


def _section_frame() -> QFrame:
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border_dark']};
            border-radius: 8px;
        }}
    """)
    return frame


def _section_header(text: str) -> QLabel:
    label = QLabel(text.upper())
    label.setStyleSheet(f"""
        font-size: 10px;
        font-weight: bold;
        color: {COLORS['text_muted']};
        letter-spacing: 1px;
        padding-bottom: 8px;
        border-bottom: 1px solid {COLORS['border_dark']};
    """)
    return label


def _field_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
    label.setMinimumWidth(116)
    return label


def _description_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; font-style: italic; padding: 2px 0;")
    return label


def _styled_combo(options: list, default_index: int = 0) -> QComboBox:
    cb = QComboBox()
    cb.addItems(options)
    cb.setCurrentIndex(default_index)
    cb.setStyleSheet(_combo_style())
    return cb


def _divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-height: 1px;")
    return line


# ── Pick Preview Widget ───────────────────────────────────────────────────────

class PickPreviewWidget(QFrame):
    """Displays a visual preview of how pick slots will be assigned."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)
        self._outer_layout = QVBoxLayout(self)
        self._outer_layout.setContentsMargins(10, 10, 10, 10)
        self._outer_layout.setSpacing(0)
        self._content: QWidget = QWidget()
        self._outer_layout.addWidget(self._content)

    def update_preview(self, preset: str, player_count: int):
        # Replace the content widget entirely — avoids nested-layout ghost issue
        self._outer_layout.removeWidget(self._content)
        self._content.deleteLater()

        self._content = QWidget()
        inner = QVBoxLayout(self._content)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(6)

        is_random = preset in RANDOM_PRESETS
        slots     = gen_pick_slots(preset, player_count)

        # Header row
        hrow = QHBoxLayout()
        hrow.setSpacing(4)
        hrow.addWidget(_make_label("PICK PREVIEW",
                                   f"font-size: 9px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;"))
        if is_random:
            hrow.addWidget(_make_label("sample — randomized each game",
                                       f"font-size: 9px; color: {COLORS['accent_warning']}; font-style: italic;"))
        hrow.addStretch()
        inner.addLayout(hrow)

        ballerz_slots = slots[:player_count]
        ringers_slots = slots[player_count:]

        for team_name, team_slots in [("Ballerz", ballerz_slots), ("Ringers", ringers_slots)]:
            row = QHBoxLayout()
            row.setSpacing(6)
            row.addWidget(_make_label(team_name,
                                      f"font-size: 11px; font-weight: 600; color: {COLORS['text_secondary']};",
                                      fixed_width=54))
            for i, slot_type in enumerate(team_slots):
                row.addWidget(self._make_chip(i + 1, slot_type))
            row.addStretch()
            inner.addLayout(row)

        self._outer_layout.addWidget(self._content)

    def _make_chip(self, number: int, slot_type: str) -> QFrame:
        bg, fg = _slot_chip_colors(slot_type)
        label_text = _slot_short_label(slot_type)

        chip = QFrame()
        chip.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: 4px;
                border: none;
            }}
        """)
        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(7, 3, 7, 3)
        chip_layout.setSpacing(4)

        num_lbl = QLabel(str(number))
        num_lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {fg}; opacity: 0.7;")
        chip_layout.addWidget(num_lbl)

        text_lbl = QLabel(label_text)
        text_lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {fg};")
        chip_layout.addWidget(text_lbl)

        return chip


# ── GameSetupWidget ───────────────────────────────────────────────────────────

class GameSetupWidget(QWidget):
    """Full match configuration screen."""

    start_match = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._modifier_controls = {}
        self._setup_ui()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(28, 24, 28, 20)
        cl.setSpacing(20)

        title = QLabel("Match Setup")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        cl.addWidget(title)

        sub = QLabel("Configure your game before entering the draft.")
        sub.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px; margin-bottom: 4px;")
        cl.addWidget(sub)

        cols = QHBoxLayout()
        cols.setSpacing(16)
        cols.addWidget(self._build_general_section(), stretch=1)
        cols.addWidget(self._build_draft_section(), stretch=1)
        cols.addWidget(self._build_modifiers_section(), stretch=1)
        cl.addLayout(cols)
        cl.addStretch()

        scroll.setWidget(content)
        outer.addWidget(scroll, stretch=1)

        # Bottom bar
        bottom = QFrame()
        bottom.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(28, 14, 28, 14)
        bl.setSpacing(12)

        self._config_summary = QLabel("")
        self._config_summary.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        bl.addWidget(self._config_summary, stretch=1)

        start_btn = QPushButton("Start Match  →")
        start_btn.setFixedHeight(46)
        start_btn.setMinimumWidth(190)
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 28px;
            }}
            QPushButton:hover {{ background-color: #0ea572; }}
            QPushButton:pressed {{ background-color: #0b8a5a; }}
        """)
        start_btn.clicked.connect(self._on_start_match)
        bl.addWidget(start_btn)

        outer.addWidget(bottom)
        self._update_summary()

    # ── Section builders ──────────────────────────────────────────────────────

    def _build_general_section(self) -> QFrame:
        frame = _section_frame()
        lo = QVBoxLayout(frame)
        lo.setContentsMargins(18, 16, 18, 16)
        lo.setSpacing(12)
        lo.addWidget(_section_header("General"))

        # Player Set
        self._player_set = _styled_combo(["Standard", "Wild"])
        lo.addLayout(self._option_row("Player Set:", self._player_set))

        # Player Count
        self._player_count = _styled_combo(["1v1", "2v2", "3v3", "4v4", "5v5"], default_index=3)
        self._player_count.currentTextChanged.connect(self._update_summary)
        self._player_count.currentTextChanged.connect(self._refresh_preview)
        lo.addLayout(self._option_row("Player Count:", self._player_count))

        # Pick/Ban Time
        self._pick_time = _styled_combo(
            ["Unlimited", "5s", "10s", "20s", "30s", "40s", "50s", "60s"]
        )
        lo.addLayout(self._option_row("Pick/Ban Time:", self._pick_time))

        # First Pick
        self._first_pick = _styled_combo(["Random", "Alex", "Danny"])
        lo.addLayout(self._option_row("First Pick:", self._first_pick))

        lo.addWidget(_divider())

        # Save Stats
        self._save_stats = QCheckBox("Save Stats")
        self._save_stats.setChecked(True)
        self._save_stats.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
        lo.addWidget(self._save_stats)

        # Special Label
        lo.addWidget(_field_label("Special Label:"))
        self._special_label = QLineEdit()
        self._special_label.setPlaceholderText("Optional game label…")
        self._special_label.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent_primary']}; }}
        """)
        lo.addWidget(self._special_label)

        lo.addStretch()
        return frame

    def _build_draft_section(self) -> QFrame:
        frame = _section_frame()
        lo = QVBoxLayout(frame)
        lo.setContentsMargins(18, 16, 18, 16)
        lo.setSpacing(12)
        lo.addWidget(_section_header("Draft"))

        # Draft Order
        self._draft_order = _styled_combo(list(DRAFT_ORDERS.keys()))
        self._draft_order.currentTextChanged.connect(self._on_draft_order_changed)
        lo.addLayout(self._option_row("Draft Order:", self._draft_order))
        self._draft_order_desc = _description_label(DRAFT_ORDERS["Classic"])
        lo.addWidget(self._draft_order_desc)

        lo.addWidget(_divider())

        # Bans row (side by side)
        bans_row = QHBoxLayout()
        bans_row.setSpacing(20)

        bans_col = QVBoxLayout()
        bans_col.setSpacing(4)
        bans_col.addWidget(_field_label("Bans:"))
        self._bans = QSpinBox()
        self._bans.setRange(0, 20)
        self._bans.setValue(0)
        self._bans.setStyleSheet(_spinbox_style())
        bans_col.addWidget(self._bans)
        bans_row.addLayout(bans_col)

        rand_bans_col = QVBoxLayout()
        rand_bans_col.setSpacing(4)
        rand_bans_col.addWidget(_field_label("Random Bans:"))
        self._random_bans = QSpinBox()
        self._random_bans.setRange(0, 20)
        self._random_bans.setValue(0)
        self._random_bans.setStyleSheet(_spinbox_style())
        rand_bans_col.addWidget(self._random_bans)
        bans_row.addLayout(rand_bans_col)

        lo.addLayout(bans_row)

        lo.addWidget(_divider())

        # Draft Content
        self._draft_content = _styled_combo(list(DRAFT_CONTENTS.keys()))
        self._draft_content.setMaxVisibleItems(len(DRAFT_CONTENTS))
        self._draft_content.currentTextChanged.connect(self._on_draft_content_changed)
        lo.addLayout(self._option_row("Draft Content:", self._draft_content))
        self._draft_content_desc = _description_label(DRAFT_CONTENTS["Normal"])
        lo.addWidget(self._draft_content_desc)

        # Pick Preview
        self._pick_preview = PickPreviewWidget()
        lo.addWidget(self._pick_preview)
        self._refresh_preview()

        lo.addStretch()
        return frame

    def _build_modifiers_section(self) -> QFrame:
        frame = _section_frame()
        lo = QVBoxLayout(frame)
        lo.setContentsMargins(18, 16, 18, 16)
        lo.setSpacing(8)
        lo.addWidget(_section_header("Modifiers"))

        hint = QLabel("Stack modifiers to create wilder game modes.")
        hint.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; margin-bottom: 4px;")
        lo.addWidget(hint)

        for mod in MODIFIERS:
            mod_frame = QFrame()
            mod_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['bg_medium']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 6px;
                }}
            """)
            mod_lo = QVBoxLayout(mod_frame)
            mod_lo.setContentsMargins(12, 10, 12, 10)
            mod_lo.setSpacing(5)

            hdr = QHBoxLayout()
            hdr.setSpacing(8)

            lbl = QLabel(mod["label"])
            lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['text_primary']};")
            hdr.addWidget(lbl, stretch=1)

            if mod["type"] == "dropdown":
                ctrl = _styled_combo(mod["options"])
                ctrl.setFixedWidth(148)
                self._modifier_controls[mod["key"]] = ctrl
                hdr.addWidget(ctrl)
            else:
                ctrl = QCheckBox()
                ctrl.setStyleSheet("""
                    QCheckBox::indicator { width: 17px; height: 17px; }
                """)
                self._modifier_controls[mod["key"]] = ctrl
                hdr.addWidget(ctrl)

            mod_lo.addLayout(hdr)
            mod_lo.addWidget(_description_label(mod["description"]))
            lo.addWidget(mod_frame)

        lo.addStretch()
        return frame

    # ── Helpers ───────────────────────────────────────────────────────────────

    def option_row(self, label_text: str, control: QWidget) -> QHBoxLayout:
        return self._option_row(label_text, control)

    def _option_row(self, label_text: str, control: QWidget) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(_field_label(label_text))
        row.addWidget(control, stretch=1)
        return row

    def _on_draft_order_changed(self, order: str):
        self._draft_order_desc.setText(DRAFT_ORDERS.get(order, ""))

    def _on_draft_content_changed(self, content: str):
        self._draft_content_desc.setText(DRAFT_CONTENTS.get(content, ""))
        self._refresh_preview()

    def _refresh_preview(self):
        preset = self._draft_content.currentText() if hasattr(self, "_draft_content") else "Normal"
        count_text = self._player_count.currentText() if hasattr(self, "_player_count") else "4v4"
        count = int(count_text.split("v")[0])
        self._pick_preview.update_preview(preset, count)

    def _update_summary(self):
        count = self._player_count.currentText() if hasattr(self, "_player_count") else "4v4"
        pool = self._player_set.currentText() if hasattr(self, "_player_set") else "Standard"
        self._config_summary.setText(f"{count}  ·  {pool}")

    # ── Config ────────────────────────────────────────────────────────────────

    def _build_config(self) -> dict:
        pick_time_map = {
            "Unlimited": None, "5s": 5, "10s": 10, "20s": 20,
            "30s": 30, "40s": 40, "50s": 50, "60s": 60,
        }
        rarity_cap_map = {
            "No Cap": None, "Common Only": "Common", "Rare & Below": "Rare",
            "Epic & Below": "Epic", "Legendary & Below": "Legendary",
        }
        pool_draw_map = {
            "Full Roster": None, "16 Players": 16, "12 Players": 12, "8 Players": 8,
        }

        player_count = int(self._player_count.currentText().split("v")[0])

        return {
            "player_set":       self._player_set.currentText(),
            "player_count":     player_count,
            "pick_time":        pick_time_map.get(self._pick_time.currentText()),
            "first_pick":       self._first_pick.currentText(),
            "save_stats":       self._save_stats.isChecked(),
            "special_label":    self._special_label.text().strip() or None,
            "draft_order":      self._draft_order.currentText(),
            "bans":             self._bans.value(),
            "random_bans":      self._random_bans.value(),
            "draft_content":    self._draft_content.currentText(),
            "pick_slots":       gen_pick_slots(self._draft_content.currentText(), player_count),
            # Modifiers
            "rarity_cap":       rarity_cap_map.get(self._modifier_controls["rarity_cap"].currentText()),
            "pool_draw":        pool_draw_map.get(self._modifier_controls["pool_draw"].currentText()),
            "exile_mode":       self._modifier_controls["exile_mode"].isChecked(),
            "wild_card_slot":   self._modifier_controls["wild_card_slot"].isChecked(),
            "archetype_mirror": self._modifier_controls["archetype_mirror"].isChecked(),
            "veterans_only":    self._modifier_controls["veterans_only"].isChecked(),
            "draft_lottery":    self._modifier_controls["draft_lottery"].isChecked(),
        }

    def _on_start_match(self):
        self.start_match.emit(self._build_config())

    def get_config(self) -> dict:
        return self._build_config()


# ── PlayWidget ────────────────────────────────────────────────────────────────

class PlayWidget(QWidget):
    """Top-level Play tab widget. Manages Game Setup → Picker → Game Screen flow."""

    load_requested      = Signal()
    match_started       = Signal(dict)  # Emits config when entering the picker
    match_ended         = Signal()      # Emits when returning to setup
    slot_filter_changed = Signal(str)   # Re-emits from picker for archetype restriction
    excluded_updated    = Signal(set)   # Re-emits picked+banned IDs after each pick/ban

    def __init__(self, parent=None):
        super().__init__(parent)
        self._match_config: dict = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget()
        layout.addWidget(self._stack)

        # Page 0: Game Setup
        self._setup_widget = GameSetupWidget()
        self._setup_widget.start_match.connect(self._on_start_match)
        self._stack.addWidget(self._setup_widget)

        # Page 1: Picker with back bar
        self._stack.addWidget(self._build_picker_page())

        # Page 2: Game screen (live box score)
        self._game_screen = GameScreen()
        self._game_screen.back_requested.connect(self._on_game_back_to_setup)
        self._stack.addWidget(self._game_screen)

        self._stack.setCurrentIndex(0)

    def _build_picker_page(self) -> QWidget:
        container = QWidget()
        lo = QVBoxLayout(container)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        back_bar = QFrame()
        back_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        back_bar.setFixedHeight(44)
        back_row = QHBoxLayout(back_bar)
        back_row.setContentsMargins(16, 0, 16, 0)
        back_row.setSpacing(12)

        back_btn = QPushButton("← Back to Setup")
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                font-size: 13px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{ color: {COLORS['text_primary']}; }}
        """)
        back_btn.clicked.connect(self._on_back_to_setup)
        back_row.addWidget(back_btn)

        self._match_summary_label = QLabel("")
        self._match_summary_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        back_row.addWidget(self._match_summary_label)
        back_row.addStretch()

        lo.addWidget(back_bar)

        self._picker = PremierPickerWidget()
        self._picker.load_requested.connect(self._on_start_game)
        self._picker.slot_filter_changed.connect(self.slot_filter_changed)
        self._picker.excluded_updated.connect(self.excluded_updated)
        lo.addWidget(self._picker, stretch=1)

        return container

    def _on_back_to_setup(self):
        self._picker.stop_draft()
        self._stack.setCurrentIndex(0)
        self.match_ended.emit()

    def _on_start_game(self):
        """Transition from picker to game screen."""
        team1, team2 = self._picker.get_teams()
        self._picker.stop_draft()
        self._game_screen.start_game(team1, team2, self._match_config)
        self._stack.setCurrentIndex(2)

    def _on_game_back_to_setup(self):
        """Return from game screen to setup."""
        self._game_screen.stop()
        self._stack.setCurrentIndex(0)
        self.match_ended.emit()

    def _on_start_match(self, config: dict):
        self._match_config = config
        self.match_started.emit(config)
        self._picker.start_draft(config)
        parts = [config["draft_content"], config["draft_order"]]
        if config.get("rarity_cap"):
            parts.append(f"Cap: {config['rarity_cap']}")
        if config.get("pool_draw"):
            parts.append(f"Pool: {config['pool_draw']}")
        active_mods = [k for k in ["exile_mode", "wild_card_slot", "archetype_mirror",
                                    "veterans_only", "draft_lottery"] if config.get(k)]
        if active_mods:
            parts.append(f"+{len(active_mods)} modifier{'s' if len(active_mods) != 1 else ''}")
        self._match_summary_label.setText("  ·  ".join(parts))
        self._stack.setCurrentIndex(1)

    def get_match_config(self) -> dict:
        return self._match_config

    def get_teams(self) -> tuple:
        return self._picker.get_teams()
