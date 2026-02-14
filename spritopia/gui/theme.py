"""
Dark theme styling for Spritopia GUI.
"""

# Color palette
COLORS = {
    # Backgrounds
    "bg_dark": "#1a1a2e",
    "bg_medium": "#16213e",
    "bg_light": "#1f2b47",
    "bg_card": "#252a40",

    # Accents
    "accent_primary": "#4a9eff",
    "accent_secondary": "#7c3aed",
    "accent_success": "#10b981",
    "accent_warning": "#f59e0b",
    "accent_danger": "#ef4444",

    # Text
    "text_primary": "#f8fafc",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",

    # Borders
    "border_dark": "#2d3748",
    "border_light": "#4a5568",

    # Rarity colors (Common=gray, Rare=blue, Epic=purple, Legendary=orange, Godlike=black+gold)
    "rarity_common": "#9ca3af",
    "rarity_common_bg": "#374151",
    "rarity_common_text": "#e5e7eb",
    "rarity_rare": "#3b82f6",
    "rarity_rare_bg": "#1e3a5f",
    "rarity_epic": "#a855f7",
    "rarity_epic_bg": "#3b1f5e",
    "rarity_legendary": "#f97316",
    "rarity_legendary_bg": "#4a2512",
    "rarity_godlike": "#d4a017",  # Deep yellowish-orange text
    "rarity_godlike_bg": "#0a0a0a",  # Pitch black
    "rarity_godlike_glow": "#ffb700",  # Gold glow

    # Archetype colors (Slayer=Aquamarine, Vigi=Green, Medic=Red, Guardian=White, Engineer=Orange, Director=Purple)
    "arch_slayer": "#2578FF",
    "arch_slayer_text": "#1a1a2e",  # Dark text for light bg
    "arch_vigilante": "#22c55e",
    "arch_medic": "#ef4444",
    "arch_guardian": "#FCF7CA",
    "arch_guardian_text": "#1a1a2e",  # Dark text for white bg
    "arch_engineer": "#f97316",
    "arch_director": "#a855f7",
}

def get_rarity_color(rarity: str) -> str:
    """Get the primary color for a rarity level."""
    return COLORS.get(f"rarity_{rarity.lower()}", COLORS["text_primary"])


def get_rarity_style(rarity: str) -> dict:
    """
    Get full styling for a rarity level.
    Returns dict with: color, bg, text, glow (optional)
    """
    rarity_lower = rarity.lower() if rarity else "common"
    base = {
        "color": COLORS.get(f"rarity_{rarity_lower}", COLORS["rarity_common"]),
        "bg": COLORS.get(f"rarity_{rarity_lower}_bg", COLORS["bg_light"]),
        "text": COLORS.get(f"rarity_{rarity_lower}_text", COLORS.get(f"rarity_{rarity_lower}", COLORS["text_primary"])),
        "glow": None,
    }
    # Godlike special styling
    if rarity_lower == "godlike":
        base["glow"] = COLORS["rarity_godlike_glow"]
        base["text"] = COLORS["rarity_godlike"]
        base["bg"] = COLORS["rarity_godlike_bg"]
    return base


def get_archetype_color(archetype: str) -> str:
    """Get the color for an archetype."""
    return COLORS.get(f"arch_{archetype.lower()}", COLORS["text_primary"])


def get_archetype_style(archetype: str) -> dict:
    """
    Get full styling for an archetype.
    Returns dict with: color, text (for contrast if needed)
    """
    arch_lower = archetype.lower() if archetype else ""
    color = COLORS.get(f"arch_{arch_lower}", COLORS["text_primary"])
    text = COLORS.get(f"arch_{arch_lower}_text", None)
    return {
        "color": color,
        "text": text if text else ("#1a1a2e" if arch_lower == "guardian" else "#f8fafc"),
    }

# Main application stylesheet
STYLESHEET = f"""
/* Global */
QWidget {{
    background-color: {COLORS["bg_dark"]};
    color: {COLORS["text_primary"]};
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 13px;
}}

/* Main Window */
QMainWindow {{
    background-color: {COLORS["bg_dark"]};
}}

/* Labels */
QLabel {{
    color: {COLORS["text_primary"]};
    background-color: transparent;
}}

QLabel[class="heading"] {{
    font-size: 18px;
    font-weight: bold;
}}

QLabel[class="subheading"] {{
    font-size: 14px;
    color: {COLORS["text_secondary"]};
}}

QLabel[class="muted"] {{
    color: {COLORS["text_muted"]};
    font-size: 12px;
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLORS["bg_card"]};
    border-color: {COLORS["accent_primary"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["bg_medium"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["bg_dark"]};
    color: {COLORS["text_muted"]};
    border-color: {COLORS["border_dark"]};
}}

QPushButton[class="primary"] {{
    background-color: {COLORS["accent_primary"]};
    border-color: {COLORS["accent_primary"]};
    color: white;
}}

QPushButton[class="primary"]:hover {{
    background-color: #3b8bdb;
}}

QPushButton[class="danger"] {{
    background-color: {COLORS["accent_danger"]};
    border-color: {COLORS["accent_danger"]};
    color: white;
}}

/* Line Edits */
QLineEdit {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    padding: 8px 12px;
}}

QLineEdit:focus {{
    border-color: {COLORS["accent_primary"]};
}}

QLineEdit::placeholder {{
    color: {COLORS["text_muted"]};
}}

/* Combo Boxes */
QComboBox {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 120px;
}}

QComboBox:hover {{
    border-color: {COLORS["accent_primary"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS["text_secondary"]};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_dark"]};
    selection-background-color: {COLORS["accent_primary"]};
}}

/* Scroll Areas */
QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollBar:vertical {{
    background-color: {COLORS["bg_dark"]};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["border_light"]};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["text_muted"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS["bg_dark"]};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["border_light"]};
    border-radius: 6px;
    min-width: 30px;
}}

/* Tab Widget */
QTabWidget::pane {{
    border: none;
    background-color: {COLORS["bg_dark"]};
}}

QTabBar::tab {{
    background-color: {COLORS["bg_medium"]};
    color: {COLORS["text_secondary"]};
    padding: 12px 24px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
}}

QTabBar::tab:disabled {{
    color: {COLORS["text_muted"]};
}}

/* List Widget */
QListWidget {{
    background-color: {COLORS["bg_light"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    outline: none;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-bottom: 1px solid {COLORS["border_dark"]};
}}

QListWidget::item:selected {{
    background-color: {COLORS["accent_primary"]};
    color: white;
}}

QListWidget::item:hover:!selected {{
    background-color: {COLORS["bg_card"]};
}}

/* Splitter */
QSplitter::handle {{
    background-color: {COLORS["border_dark"]};
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

/* Frame / Cards */
QFrame[class="card"] {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 8px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {COLORS["bg_light"]};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS["accent_primary"]};
    border-radius: 4px;
}}

/* Spin Box */
QSpinBox {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    padding: 6px 10px;
}}

QSpinBox:focus {{
    border-color: {COLORS["accent_primary"]};
}}

/* Tool Tips */
QToolTip {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border_light"]};
    padding: 6px 10px;
    border-radius: 4px;
}}

/* Group Box */
QGroupBox {{
    font-weight: bold;
    border: 1px solid {COLORS["border_dark"]};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}}
"""
