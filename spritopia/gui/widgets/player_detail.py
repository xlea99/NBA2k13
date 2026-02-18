"""
Detailed player view widget for the sidebar.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QGridLayout, QProgressBar, QTabWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from spritopia.players.players import Player
from spritopia.players import archetypes
from spritopia.gui.theme import COLORS, get_rarity_style, get_archetype_style
from spritopia.common.paths import paths


class IconWithTooltip(QLabel):
    """A label that displays an image with a rich tooltip."""

    def __init__(self, size: int = 48, parent=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)

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
                self.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px; font-weight: bold;")
        else:
            self.setText("?")
            self.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px; font-weight: bold;")

    def set_tooltip_content(self, title: str, description: str):
        """Set the tooltip title and description."""
        tooltip = f"<b>{title}</b>"
        if description:
            wrapped = description[:400] + "..." if len(description) > 400 else description
            tooltip += f"<br/><br/>{wrapped}"
        self.setToolTip(tooltip)


class StatBar(QWidget):
    """A labeled progress bar for showing a stat value."""

    def __init__(self, label: str, value: int = 0, max_value: int = 99, parent=None):
        super().__init__(parent)
        self._setup_ui(label)
        self.set_value(value, max_value)

    def _setup_ui(self, label: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 1, 0, 1)
        layout.setSpacing(6)

        self.label = QLabel(label)
        self.label.setFixedWidth(90)
        self.label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(6)
        self.bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['bg_dark']};
                border-radius: 3px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent_primary']};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.bar, stretch=1)

        self.value_label = QLabel("0")
        self.value_label.setFixedWidth(24)
        self.value_label.setAlignment(Qt.AlignRight)
        self.value_label.setStyleSheet(f"font-weight: bold; font-size: 10px;")
        layout.addWidget(self.value_label)

    def set_value(self, value: int, max_value: int = 99):
        self.bar.setMaximum(max_value)
        self.bar.setValue(value)
        self.value_label.setText(str(value))

        # Color code based on value
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


class StatMiniBar(QWidget):
    """Compact stat bar for overview section."""

    def __init__(self, label: str, value: int = 0, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        self.label = QLabel(label)
        self.label.setFixedWidth(80)
        self.label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(8)
        self.bar.setMaximum(99)
        self.bar.setValue(value)
        layout.addWidget(self.bar, stretch=1)

        self.value_label = QLabel(str(value))
        self.value_label.setFixedWidth(28)
        self.value_label.setAlignment(Qt.AlignRight)
        self.value_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.value_label)

        self._update_color(value)

    def set_value(self, value: int):
        self.bar.setValue(value)
        self.value_label.setText(str(value))
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
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)


class PlayerDetailWidget(QWidget):
    """
    Full player detail view with overview, stats, and more.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Compact header section
        self.header = self._create_header()
        layout.addWidget(self.header)

        # Main tab widget (Overview, Attributes, Stats)
        self.main_tabs = QTabWidget()
        self.main_tabs.setDocumentMode(True)
        self.main_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 8px 16px;
                margin-right: 1px;
                font-size: 11px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['bg_card']};
            }}
        """)

        # Overview tab
        self.overview_widget = self._create_overview_tab()
        self.main_tabs.addTab(self.overview_widget, "Overview")

        # Attributes tab (with subtabs)
        self.attributes_widget = self._create_attributes_tab()
        self.main_tabs.addTab(self.attributes_widget, "Attributes")

        # Stats tab (placeholder)
        self.stats_widget = self._create_stats_placeholder()
        self.main_tabs.addTab(self.stats_widget, "Stats")

        layout.addWidget(self.main_tabs)

        # Empty state
        self._show_empty_state()

    def _create_header(self) -> QFrame:
        """Create compact player header section."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Name + Rarity row
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.name_label = QLabel("Select a Player")
        self.name_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_row.addWidget(self.name_label)

        top_row.addStretch()

        self.rarity_badge = QLabel("")
        self.rarity_badge.setAlignment(Qt.AlignCenter)
        self.rarity_badge.setStyleSheet(f"""
            font-size: 9px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 3px;
            background-color: {COLORS['bg_light']};
        """)
        top_row.addWidget(self.rarity_badge)

        layout.addLayout(top_row)

        # Archetype + Height/Weight row
        info_row = QHBoxLayout()
        info_row.setSpacing(8)

        self.archetype_label = QLabel("")
        self.archetype_label.setStyleSheet(f"font-size: 12px; font-weight: 500;")
        info_row.addWidget(self.archetype_label)

        self.physical_label = QLabel("")
        self.physical_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        info_row.addWidget(self.physical_label)

        info_row.addStretch()

        layout.addLayout(info_row)

        return frame

    def _create_overview_tab(self) -> QWidget:
        """Create the Overview tab with bio, top stats, and icons."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Faction and Artifact icons row
        icons_frame = QFrame()
        icons_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)

        icons_grid = QGridLayout(icons_frame)
        icons_grid.setContentsMargins(12, 10, 12, 10)
        icons_grid.setHorizontalSpacing(12)
        icons_grid.setVerticalSpacing(6)
        icons_grid.setColumnStretch(0, 1)
        icons_grid.setColumnStretch(1, 1)

        # Row 0: Headers
        faction_header = QLabel("FACTION")
        faction_header.setAlignment(Qt.AlignCenter)
        faction_header.setStyleSheet(f"font-size: 8px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;")
        icons_grid.addWidget(faction_header, 0, 0)

        artifact_header = QLabel("ARTIFACT")
        artifact_header.setAlignment(Qt.AlignCenter)
        artifact_header.setStyleSheet(f"font-size: 8px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;")
        icons_grid.addWidget(artifact_header, 0, 1)

        # Row 1: Icons
        self.faction_icon = IconWithTooltip(size=48)
        self.faction_icon.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 4px;")
        icons_grid.addWidget(self.faction_icon, 1, 0, Qt.AlignCenter)

        self.artifact_icon = IconWithTooltip(size=48)
        self.artifact_icon.setStyleSheet(f"background-color: {COLORS['bg_light']}; border-radius: 4px;")
        icons_grid.addWidget(self.artifact_icon, 1, 1, Qt.AlignCenter)

        # Row 2: Names (these can vary in height)
        self.faction_name_label = QLabel("None")
        self.faction_name_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.faction_name_label.setWordWrap(True)
        self.faction_name_label.setStyleSheet(f"font-size: 10px; color: {COLORS['text_secondary']};")
        icons_grid.addWidget(self.faction_name_label, 2, 0)

        self.artifact_name_label = QLabel("None")
        self.artifact_name_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.artifact_name_label.setWordWrap(True)
        self.artifact_name_label.setStyleSheet(f"font-size: 10px; color: {COLORS['text_secondary']};")
        icons_grid.addWidget(self.artifact_name_label, 2, 1)

        layout.addWidget(icons_frame)

        # Key Stats section
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)

        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(12, 10, 12, 10)
        stats_layout.setSpacing(4)

        stats_header = QLabel("KEY ATTRIBUTES")
        stats_header.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;")
        stats_layout.addWidget(stats_header)

        self.key_stat_bars = []
        for i in range(5):
            bar = StatMiniBar("--", 0)
            self.key_stat_bars.append(bar)
            stats_layout.addWidget(bar)

        layout.addWidget(stats_frame)

        # Bio section
        bio_frame = QFrame()
        bio_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)

        bio_layout = QVBoxLayout(bio_frame)
        bio_layout.setContentsMargins(12, 10, 12, 10)
        bio_layout.setSpacing(4)

        bio_header = QLabel("BIO")
        bio_header.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;")
        bio_layout.addWidget(bio_header)

        self.bio_label = QLabel("No bio available.")
        self.bio_label.setWordWrap(True)
        self.bio_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")
        bio_layout.addWidget(self.bio_label)

        layout.addWidget(bio_frame)

        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_attributes_tab(self) -> QWidget:
        """Create the Attributes tab with Offense/Defense/Control/General subtabs."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sub-tab widget
        self.stats_tabs = QTabWidget()
        self.stats_tabs.setDocumentMode(True)
        self.stats_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_secondary']};
                padding: 6px 12px;
                margin-right: 1px;
                font-size: 10px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
        """)

        # Offensive tab
        self.offensive_bars = {}
        offensive_widget = self._create_stat_scroll(archetypes.OFFENSIVE_ATTRIBUTES, self.offensive_bars)
        self.stats_tabs.addTab(offensive_widget, "Offense")

        # Defensive tab
        self.defensive_bars = {}
        defensive_widget = self._create_stat_scroll(archetypes.DEFENSIVE_ATTRIBUTES, self.defensive_bars)
        self.stats_tabs.addTab(defensive_widget, "Defense")

        # Control tab
        self.control_bars = {}
        control_widget = self._create_stat_scroll(archetypes.CONTROL_ATTRIBUTES, self.control_bars)
        self.stats_tabs.addTab(control_widget, "Control")

        # General tab
        self.general_bars = {}
        general_widget = self._create_stat_scroll(archetypes.GENERAL_ATTRIBUTES, self.general_bars)
        self.stats_tabs.addTab(general_widget, "General")

        layout.addWidget(self.stats_tabs)
        return widget

    def _create_stat_scroll(self, attributes: list, bar_dict: dict) -> QScrollArea:
        """Create a scrollable stat section."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        for attr in attributes:
            name = archetypes.MAPPED_ATTRIBUTES.get(attr, attr)
            bar = StatBar(name)
            layout.addWidget(bar)
            bar_dict[attr] = bar

        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_stats_placeholder(self) -> QWidget:
        """Create placeholder for Stats tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Game Statistics")
        label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['text_secondary']};")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        sublabel = QLabel("Coming soon...")
        sublabel.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        sublabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(sublabel)

        return widget

    def _show_empty_state(self):
        """Show the empty state when no player is selected."""
        self.name_label.setText("Select a Player")
        self.rarity_badge.hide()
        self.archetype_label.setText("")
        self.physical_label.setText("")
        self.main_tabs.hide()

    def set_player(self, player: Player):
        """Update the view with player data."""
        self._player = player

        if player is None:
            self._show_empty_state()
            return

        # Show all sections
        self.rarity_badge.show()
        self.main_tabs.show()

        # Header info
        first = player["First_Name"] or ""
        last = player["Last_Name"] or ""
        self.name_label.setText(f"{first} {last}".strip() or "Unknown")

        # Rarity with new styling
        rarity = player["Rarity"] or "Common"
        rarity_style = get_rarity_style(rarity)
        self.rarity_badge.setText(rarity.upper())

        if rarity.lower() == "godlike":
            # Special godlike styling with glow effect
            self.rarity_badge.setStyleSheet(f"""
                font-size: 9px;
                font-weight: bold;
                padding: 3px 8px;
                border-radius: 3px;
                background-color: {rarity_style['bg']};
                color: {rarity_style['text']};
                border: 1px solid {rarity_style['glow']};
            """)
        else:
            self.rarity_badge.setStyleSheet(f"""
                font-size: 9px;
                font-weight: bold;
                padding: 3px 8px;
                border-radius: 3px;
                background-color: {rarity_style['bg']};
                color: {rarity_style['color']};
            """)

        # Archetype with new colors
        archetype = player["Archetype"]
        if archetype:
            arch_style = get_archetype_style(str(archetype))
            self.archetype_label.setText(str(archetype))
            self.archetype_label.setStyleSheet(f"font-size: 12px; font-weight: 500; color: {arch_style['color']};")
        else:
            self.archetype_label.setText("No Archetype")
            self.archetype_label.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']};")

        # Height/Weight (no position)
        height_inches = player["Height"] or 70
        height_ft = height_inches // 12
        height_in = height_inches % 12
        weight = player["Weight"] or 0
        self.physical_label.setText(f"{height_ft}'{height_in}\" · {int(weight)} lbs")

        # Overview tab - Faction icon
        faction = player["Faction"] or ""
        if faction:
            self.faction_name_label.setText(faction)
            faction_icon_path = paths["graphics"] / "FactionIcons" / f"{faction}.png"
            self.faction_icon.set_image(str(faction_icon_path))

            try:
                from spritopia.players import factions
                faction_info = factions.dbDict["Factions"].get(faction, {})
                faction_desc = faction_info.get("Description", "")
                self.faction_icon.set_tooltip_content(faction, faction_desc)
            except Exception:
                self.faction_icon.set_tooltip_content(faction, "")
        else:
            self.faction_name_label.setText("None")
            self.faction_icon.setText("-")
            self.faction_icon.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px; background-color: {COLORS['bg_light']}; border-radius: 4px;")
            self.faction_icon.setToolTip("No faction")

        # Overview tab - Artifact icon
        pmods = player.pmods if hasattr(player, 'pmods') else []
        if pmods:
            pmod = pmods[0]
            artifact_name = pmod.get("Name", "Unknown")
            artifact_desc = pmod.get("Description", "")
            artifact_image = pmod.get("Image", "")

            self.artifact_name_label.setText(artifact_name)

            if artifact_image:
                artifact_icon_path = paths["graphics"] / artifact_image
                self.artifact_icon.set_image(str(artifact_icon_path))
            else:
                self.artifact_icon.setText("?")
                self.artifact_icon.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px; background-color: {COLORS['bg_light']}; border-radius: 4px;")

            self.artifact_icon.set_tooltip_content(artifact_name, artifact_desc)
        else:
            self.artifact_name_label.setText("None")
            self.artifact_icon.setText("-")
            self.artifact_icon.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px; background-color: {COLORS['bg_light']}; border-radius: 4px;")
            self.artifact_icon.setToolTip("No artifact")

        # Overview tab - Key stats (top 5 most important for archetype)
        if archetype and hasattr(archetype, 'attributeImportance'):
            important_attrs = archetype.attributeImportance[:5]
            for i, attr in enumerate(important_attrs):
                if i < len(self.key_stat_bars):
                    name = archetypes.MAPPED_ATTRIBUTES.get(attr, attr)
                    value = player[attr] or 0
                    self.key_stat_bars[i].label.setText(name)
                    self.key_stat_bars[i].set_value(value)
        else:
            # Default stats if no archetype
            default_attrs = ["ClsRngSht", "MdRngSht", "3PtSht", "SpeedRat", "StealRat"]
            for i, attr in enumerate(default_attrs):
                if i < len(self.key_stat_bars):
                    name = archetypes.MAPPED_ATTRIBUTES.get(attr, attr)
                    value = player[attr] or 0
                    self.key_stat_bars[i].label.setText(name)
                    self.key_stat_bars[i].set_value(value)

        # Overview tab - Bio
        bio_parts = []
        if faction:
            bio_parts.append(f"Member of {faction}.")
        if archetype:
            bio_parts.append(f"Plays as a {archetype}.")
        if pmods:
            bio_parts.append(f"Wielding the {pmods[0].get('Name', 'Unknown')} artifact.")

        if bio_parts:
            self.bio_label.setText(" ".join(bio_parts))
        else:
            self.bio_label.setText("No bio available.")

        # Attributes tab - all stats
        for attr, bar in self.offensive_bars.items():
            bar.set_value(player[attr] or 0)
        for attr, bar in self.defensive_bars.items():
            bar.set_value(player[attr] or 0)
        for attr, bar in self.control_bars.items():
            bar.set_value(player[attr] or 0)
        for attr, bar in self.general_bars.items():
            bar.set_value(player[attr] or 0)

    def get_player(self) -> Player:
        return self._player
