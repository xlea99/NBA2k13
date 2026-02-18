"""
Stats Center Widget - Main statistics hub for Spritopia.

Features:
- Dashboard with global stats and quick metrics
- Leaderboards with multiple categories
- Game history browser
- Player stat lookup
- Analytics by archetype/rarity/faction
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QScrollArea, QFrame, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QLineEdit, QSpinBox, QPushButton,
    QSplitter, QSizePolicy, QStackedWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from spritopia.gui.theme import COLORS, get_rarity_style, get_archetype_style
from spritopia.gui.stats.stats_engine import StatsEngine, PlayerCareerStats, GameRecord
from spritopia.data_storage.data_storage import d

from typing import Optional, List, Dict, Any


class NumericTableItem(QTableWidgetItem):
    """Table item that sorts numerically but displays a formatted string."""

    def __init__(self, value: float, display_text: str):
        super().__init__()
        self._sort_value = value
        self.setText(display_text)

    def __lt__(self, other):
        if isinstance(other, NumericTableItem):
            return self._sort_value < other._sort_value
        return super().__lt__(other)


class StatCard(QFrame):
    """A styled card displaying a single statistic."""

    def __init__(self, title: str, value: str, subtitle: str = "", color: str = None):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 500;")
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_color = color or COLORS['text_primary']
        value_label.setStyleSheet(f"color: {value_color}; font-size: 28px; font-weight: bold;")
        layout.addWidget(value_label)

        # Subtitle
        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
            layout.addWidget(sub_label)

        self._value_label = value_label

    def update_value(self, value: str, color: str = None):
        self._value_label.setText(value)
        if color:
            self._value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")


class LeaderboardTable(QTableWidget):
    """A styled table for displaying leaderboards."""

    player_selected = Signal(int)  # Emits sprite_id

    # Stat tooltips for header columns
    STAT_TOOLTIPS = {
        "#": "Rank in this leaderboard",
        "Player": "Player name (double-click to view full stats)",
        "Arch": "Player's archetype class",
        "Rarity": "Player's rarity tier",
        "GP": "Games Played - Total number of games",
        "PPG": "Points Per Game - Average points scored per game",
        "FG%": "Field Goal Percentage - (FG Made / FG Attempted) x 100",
        "3P%": "Three-Point Percentage - (3PT Made / 3PT Attempted) x 100",
        "TS%": "True Shooting Percentage - Measures scoring efficiency (points relative to max possible from attempts)",
        "APG": "Assists Per Game - Average assists per game",
        "AST/TO": "Assist to Turnover Ratio - Higher is better ball security",
        "PTS Created": "Points Created Per Game - Own points + points from assists",
        "RPG": "Rebounds Per Game - Total rebounds (offensive + defensive)",
        "ORPG": "Offensive Rebounds Per Game",
        "DRPG": "Defensive Rebounds Per Game",
        "SPG": "Steals Per Game",
        "BPG": "Blocks Per Game",
        "STL+BLK": "Combined Steals + Blocks Per Game",
        "EFF": "Efficiency Rating - Custom metric: (PTS+REB+AST+STL+BLK-TO-MissedFG) / GP",
        "GmSc": "Game Score - Hollinger's formula measuring overall game impact",
        "eFG%": "Effective Field Goal % - Adjusts FG% to account for outsides being worth more than insides",
        "W": "Wins",
        "L": "Losses",
        "WIN%": "Win Percentage - (Wins / Games Played) x 100",
    }

    def __init__(self, columns: List[str], tooltips: Dict[str, str] = None):
        super().__init__()
        self._columns = columns
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # Set header tooltips
        for i, col in enumerate(columns):
            tooltip = (tooltips or {}).get(col) or self.STAT_TOOLTIPS.get(col, "")
            if tooltip:
                self.horizontalHeaderItem(i).setToolTip(tooltip)

        # Style
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
                gridline-color: {COLORS['border_dark']};
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {COLORS['accent_primary']};
                font-weight: 600;
            }}
        """)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(False)

        # Auto-resize all columns to content, with Player column getting extra stretch
        header = self.horizontalHeader()
        for i in range(len(columns)):
            if columns[i] == "Player":
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.cellDoubleClicked.connect(self._on_double_click)

    def _on_double_click(self, row: int, col: int):
        item = self.item(row, 0)
        if item and item.data(Qt.UserRole):
            self.player_selected.emit(item.data(Qt.UserRole))

    def set_data(self, rows: List[List[Any]], sprite_ids: List[int] = None):
        """Set table data."""
        self.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                # Store sprite_id in first column
                if sprite_ids and j == 0:
                    item.setData(Qt.UserRole, sprite_ids[i])

                # Color code by archetype or rarity if applicable
                if j == 2 and value:  # Archetype column
                    arch_style = get_archetype_style(value)
                    if arch_style:
                        item.setForeground(QColor(arch_style["color"]))
                elif j == 3 and value:  # Rarity column
                    rar_style = get_rarity_style(value)
                    if rar_style:
                        item.setForeground(QColor(rar_style["color"]))

                self.setItem(i, j, item)


class DashboardWidget(QWidget):
    """Dashboard view with global stats and quick metrics."""

    def __init__(self, engine: StatsEngine):
        super().__init__()
        self._engine = engine
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Title
        title = QLabel("Stats Dashboard")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        layout.addWidget(title)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)

        # Get global stats
        global_stats = self._engine.get_global_stats()

        # === ROW 1: Condensed Win Stats + Total Points + Archetype Performance ===
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(16)

        # Condensed Win/Margin Table
        win_table_widget = self._create_condensed_win_table(global_stats)
        row1_layout.addWidget(win_table_widget)

        # Total Points Card
        self._points_card = StatCard(
            "TOTAL POINTS",
            f"{global_stats['total_points_scored']:,}",
            f"{global_stats['avg_total_points_per_game']:.1f} avg per game",
            COLORS['accent_primary']
        )
        row1_layout.addWidget(self._points_card)

        # Archetype Breakdown Section (moved to row 1)
        arch_section = self._create_archetype_section()
        row1_layout.addWidget(arch_section, stretch=2)

        content_layout.addLayout(row1_layout)

        # === ROW 2: Top Performers (swapped with Rarity - more important) ===
        top_section = self._create_top_performers_section()
        content_layout.addWidget(top_section)

        # === ROW 3: Rarity Breakdown Section ===
        rarity_section = self._create_rarity_section()
        content_layout.addWidget(rarity_section)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _create_condensed_win_table(self, global_stats: dict) -> QWidget:
        """Create a condensed table showing team wins and margins."""
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header
        header = QLabel("GAME RESULTS")
        header.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 500;")
        layout.addWidget(header)

        # Calculate avg margins
        games = self._engine.get_games()
        ballerz_margin_sum = 0
        ringers_margin_sum = 0
        ballerz_wins = global_stats["ballerz_wins"]
        ringers_wins = global_stats["ringers_wins"]

        for game in games:
            diff = game.ballerz_score - game.ringers_score
            if diff > 0:  # Ballerz win
                ballerz_margin_sum += diff
            elif diff < 0:  # Ringers win
                ringers_margin_sum += abs(diff)

        ballerz_avg_margin = ballerz_margin_sum / ballerz_wins if ballerz_wins > 0 else 0
        ringers_avg_margin = ringers_margin_sum / ringers_wins if ringers_wins > 0 else 0

        # Table-like grid
        grid = QGridLayout()
        grid.setSpacing(8)

        # Header row
        team_header = QLabel("Team")
        team_header.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        wins_header = QLabel("Wins")
        wins_header.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        wins_header.setAlignment(Qt.AlignCenter)
        margin_header = QLabel("Avg Win Margin")
        margin_header.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        margin_header.setAlignment(Qt.AlignCenter)

        grid.addWidget(team_header, 0, 0)
        grid.addWidget(wins_header, 0, 1)
        grid.addWidget(margin_header, 0, 2)

        # Ballerz row
        ballerz_label = QLabel("Ballerz")
        ballerz_label.setStyleSheet(f"color: {COLORS['accent_success']}; font-size: 13px; font-weight: 600;")
        ballerz_wins_label = QLabel(str(ballerz_wins))
        ballerz_wins_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        ballerz_wins_label.setAlignment(Qt.AlignCenter)
        ballerz_margin_label = QLabel(f"{ballerz_avg_margin:.1f}")
        ballerz_margin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        ballerz_margin_label.setAlignment(Qt.AlignCenter)

        grid.addWidget(ballerz_label, 1, 0)
        grid.addWidget(ballerz_wins_label, 1, 1)
        grid.addWidget(ballerz_margin_label, 1, 2)

        # Ringers row
        ringers_label = QLabel("Ringers")
        ringers_label.setStyleSheet(f"color: {COLORS['accent_warning']}; font-size: 13px; font-weight: 600;")
        ringers_wins_label = QLabel(str(ringers_wins))
        ringers_wins_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        ringers_wins_label.setAlignment(Qt.AlignCenter)
        ringers_margin_label = QLabel(f"{ringers_avg_margin:.1f}")
        ringers_margin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        ringers_margin_label.setAlignment(Qt.AlignCenter)

        grid.addWidget(ringers_label, 2, 0)
        grid.addWidget(ringers_wins_label, 2, 1)
        grid.addWidget(ringers_margin_label, 2, 2)

        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background-color: {COLORS['border_dark']};")
        divider.setFixedHeight(1)
        grid.addWidget(divider, 3, 0, 1, 3)

        # Total row (bold)
        total_label = QLabel("Total")
        total_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: bold;")
        total_games_label = QLabel(str(global_stats["total_games"]))
        total_games_label.setStyleSheet(f"color: {COLORS['accent_primary']}; font-size: 16px; font-weight: bold;")
        total_games_label.setAlignment(Qt.AlignCenter)
        total_margin_label = QLabel(f"{global_stats['avg_point_differential']:.1f}")
        total_margin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        total_margin_label.setAlignment(Qt.AlignCenter)

        grid.addWidget(total_label, 4, 0)
        grid.addWidget(total_games_label, 4, 1)
        grid.addWidget(total_margin_label, 4, 2)

        layout.addLayout(grid)
        return container

    def _create_section_header(self, title: str) -> QLabel:
        label = QLabel(title)
        label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding-bottom: 8px;
            border-bottom: 2px solid {COLORS['accent_primary']};
        """)
        return label

    def _create_archetype_section(self) -> QWidget:
        """Create a compact archetype performance grid without a header."""
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        breakdown = self._engine.get_archetype_breakdown()

        grid = QGridLayout()
        grid.setSpacing(6)

        archetypes = ["Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"]

        for i, arch in enumerate(archetypes):
            data = breakdown.get(arch, {"count": 0, "total_games": 0, "win_pct": 0, "ppg": 0})
            arch_style = get_archetype_style(arch)

            # Create compact mini card for each archetype
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['bg_light']};
                    border-left: 3px solid {arch_style['color']};
                    border-radius: 4px;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)
            card_layout.setSpacing(4)

            name = QLabel(arch)
            name.setStyleSheet(f"font-weight: bold; font-size: 12px; color: {arch_style['color']};")
            card_layout.addWidget(name)

            # Win percentage - prominent
            win_label = QLabel(f"{data['win_pct']*100:.0f}% W")
            win_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['text_primary']};")
            card_layout.addWidget(win_label)

            # PPG - secondary
            ppg_label = QLabel(f"{data['ppg']:.1f} PPG")
            ppg_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")
            card_layout.addWidget(ppg_label)

            grid.addWidget(card, i // 3, i % 3)

        layout.addLayout(grid)
        return container

    def _create_rarity_section(self) -> QWidget:
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        layout.addWidget(self._create_section_header("Rarity Comparison"))

        breakdown = self._engine.get_rarity_breakdown()

        grid = QGridLayout()
        grid.setSpacing(12)

        rarities = ["Common", "Rare", "Epic", "Legendary", "Godlike"]

        for i, rarity in enumerate(rarities):
            data = breakdown.get(rarity, {"count": 0, "total_games": 0, "win_pct": 0, "ppg": 0, "avg_efficiency": 0})
            rar_style = get_rarity_style(rarity)

            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {rar_style['bg']};
                    border: 1px solid {rar_style['color']};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 8, 12, 8)
            card_layout.setSpacing(4)

            name = QLabel(rarity)
            name.setStyleSheet(f"font-weight: bold; color: {rar_style['color']};")
            card_layout.addWidget(name)

            stats_label = QLabel(f"{data['count']} players")
            stats_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
            card_layout.addWidget(stats_label)

            if data['total_games'] > 0:
                metrics = QLabel(f"Win: {data['win_pct']*100:.0f}% | Eff: {data['avg_efficiency']:.1f}")
            else:
                metrics = QLabel("No games played")
            metrics.setStyleSheet(f"font-size: 12px; color: {COLORS['text_secondary']};")
            card_layout.addWidget(metrics)

            grid.addWidget(card, 0, i)

        layout.addLayout(grid)
        return container

    def _create_top_performers_section(self) -> QWidget:
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        layout.addWidget(self._create_section_header("Top Performers"))

        # Create a horizontal layout for different categories
        cats_layout = QHBoxLayout()
        cats_layout.setSpacing(32)

        # Category definitions with tooltips
        categories = [
            ("Scoring", "PPG", "ppg", 3,
             "Points Per Game - Average points scored. The primary measure of offensive output."),
            ("Efficiency", "EFF", "efficiency_rating", 3,
             "Efficiency Rating - A comprehensive metric combining positive stats (PTS, REB, AST, STL, BLK) minus negatives (TO, missed shots), divided by games played. Higher = more impactful player."),
            ("Playmaking", "APG", "apg", 3,
             "Assists Per Game - Measures how well a player creates scoring opportunities for teammates."),
            ("Winning", "WIN%", "win_pct", 5,
             "Win Percentage - The percentage of games won when this player participates. Requires 5+ games to qualify."),
        ]

        for title, stat_label, stat_key, min_games, tooltip in categories:
            data = self._engine.get_leaderboard(stat_key, min_games=min_games, limit=5)
            cats_layout.addWidget(self._create_mini_leaderboard(title, stat_label, data, tooltip))

        layout.addLayout(cats_layout)
        return container

    def _create_mini_leaderboard(self, title: str, stat_label: str, data: List, tooltip: str = "") -> QWidget:
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Header with tooltip
        header = QLabel(title)
        header.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {COLORS['accent_primary']};")
        if tooltip:
            header.setToolTip(tooltip)
            header.setCursor(Qt.WhatsThisCursor)
        layout.addWidget(header)

        # Subtitle explaining the stat
        stat_desc = QLabel(f"Ranked by {stat_label}")
        stat_desc.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']}; margin-bottom: 4px;")
        layout.addWidget(stat_desc)

        # Player rows
        for i, (stats, value) in enumerate(data):
            row_frame = QFrame()
            row_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {'rgba(74, 158, 255, 0.1)' if i == 0 else 'transparent'};
                    border-radius: 4px;
                    padding: 4px;
                }}
            """)
            row = QHBoxLayout(row_frame)
            row.setContentsMargins(8, 6, 8, 6)
            row.setSpacing(12)

            # Rank with medal colors for top 3
            rank_colors = {0: "#FFD700", 1: "#C0C0C0", 2: "#CD7F32"}
            rank = QLabel(f"#{i+1}")
            rank_color = rank_colors.get(i, COLORS['text_muted'])
            rank.setStyleSheet(f"color: {rank_color}; font-weight: bold; min-width: 28px; font-size: 13px;")
            row.addWidget(rank)

            # Player name - show more characters
            name_text = stats.full_name[:20] + "..." if len(stats.full_name) > 20 else stats.full_name
            name = QLabel(name_text)
            name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
            row.addWidget(name, stretch=1)

            # Stat value
            if stat_label == "WIN%":
                val_text = f"{value*100:.0f}%"
            else:
                val_text = f"{value:.1f}"
            val_label = QLabel(val_text)
            val_label.setStyleSheet(f"color: {COLORS['accent_primary']}; font-weight: bold; font-size: 14px;")
            row.addWidget(val_label)

            # Games played indicator
            gp_label = QLabel(f"({stats.games_played}G)")
            gp_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
            row.addWidget(gp_label)

            layout.addWidget(row_frame)

        if not data:
            no_data = QLabel("No qualifying players\n(min games not met)")
            no_data.setStyleSheet(f"color: {COLORS['text_muted']}; font-style: italic; padding: 20px;")
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)

        layout.addStretch()
        return widget


class UnifiedLeaderboardTable(QTableWidget):
    """A unified leaderboard table with all stats as sortable columns."""

    player_selected = Signal(int)  # Emits sprite_id

    # Column definitions: (header, tooltip, width_hint)
    COLUMNS = [
        ("Player", "Player name (double-click to view full stats)", 150),
        ("Arch", "Player's archetype class", 70),
        ("Rarity", "Player's rarity tier", 70),
        ("GP", "Games Played", 40),
        ("W", "Wins", 35),
        ("L", "Losses", 35),
        ("WIN%", "Win Percentage", 50),
        ("PPG", "Points Per Game", 45),
        ("APG", "Assists Per Game", 45),
        ("RPG", "Rebounds Per Game", 45),
        ("SPG", "Steals Per Game", 40),
        ("BPG", "Blocks Per Game", 40),
        ("FG%", "Field Goal Percentage", 45),
        ("3P%", "Three-Point Percentage", 45),
        ("TS%", "True Shooting Percentage", 45),
        ("eFG%", "Effective FG%", 45),
        ("EFF", "Efficiency Rating", 45),
        ("GmSc", "Game Score (Hollinger)", 45),
        ("AST/TO", "Assist to Turnover Ratio", 55),
    ]

    def __init__(self):
        super().__init__()
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels([c[0] for c in self.COLUMNS])

        # Set tooltips
        for i, (name, tooltip, _) in enumerate(self.COLUMNS):
            self.horizontalHeaderItem(i).setToolTip(tooltip)

        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
                gridline-color: {COLORS['border_dark']};
            }}
            QTableWidget::item {{
                padding: 6px 8px;
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 8px 4px;
                border: none;
                border-bottom: 2px solid {COLORS['accent_primary']};
                font-weight: 600;
                font-size: 11px;
            }}
        """)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)

        # Column sizing
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Player stretches
        for i in range(1, len(self.COLUMNS)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.cellDoubleClicked.connect(self._on_double_click)

    def _on_double_click(self, row: int, col: int):
        item = self.item(row, 0)
        if item and item.data(Qt.UserRole):
            self.player_selected.emit(item.data(Qt.UserRole))

    def set_data(self, stats_list: list):
        """Set table data from a list of PlayerCareerStats objects."""
        self.setSortingEnabled(False)
        self.setRowCount(len(stats_list))

        for i, stats in enumerate(stats_list):
            # Player name (stores sprite_id)
            name_item = QTableWidgetItem(stats.full_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_item.setData(Qt.UserRole, stats.sprite_id)
            self.setItem(i, 0, name_item)

            # Archetype (color coded)
            arch_item = QTableWidgetItem(stats.archetype)
            arch_item.setFlags(arch_item.flags() & ~Qt.ItemIsEditable)
            arch_style = get_archetype_style(stats.archetype)
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            self.setItem(i, 1, arch_item)

            # Rarity (color coded)
            rar_item = QTableWidgetItem(stats.rarity)
            rar_item.setFlags(rar_item.flags() & ~Qt.ItemIsEditable)
            rar_style = get_rarity_style(stats.rarity)
            if rar_style:
                rar_item.setForeground(QColor(rar_style["color"]))
            self.setItem(i, 2, rar_item)

            # Numeric columns - use setData for proper sorting
            numeric_values = [
                stats.games_played,
                stats.wins,
                stats.losses,
                stats.win_pct * 100,
                stats.ppg,
                stats.apg,
                stats.rpg,
                stats.spg,
                stats.bpg,
                stats.fg_pct * 100,
                stats.three_pt_pct * 100,
                stats.ts_pct * 100,
                stats.efg_pct * 100,
                stats.efficiency_rating,
                stats.game_score_avg,
                stats.ast_to_ratio,
            ]

            # Format strings for display
            formats = [
                "{:.0f}",  # GP
                "{:.0f}",  # W
                "{:.0f}",  # L
                "{:.1f}%",  # WIN%
                "{:.1f}",  # PPG
                "{:.1f}",  # APG
                "{:.1f}",  # RPG
                "{:.1f}",  # SPG
                "{:.1f}",  # BPG
                "{:.1f}%",  # FG%
                "{:.1f}%",  # 3P%
                "{:.1f}%",  # TS%
                "{:.1f}%",  # eFG%
                "{:.1f}",  # EFF
                "{:.1f}",  # GmSc
                "{:.2f}",  # AST/TO
            ]

            for j, (val, fmt) in enumerate(zip(numeric_values, formats)):
                item = NumericTableItem(val, fmt.format(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j + 3, item)

        self.setSortingEnabled(True)


class LeaderboardsWidget(QWidget):
    """Unified leaderboards view with all stats in one sortable table."""

    player_selected = Signal(int)

    def __init__(self, engine: StatsEngine):
        super().__init__()
        self._engine = engine
        self._all_stats: list = []  # Cache of all stats for filtering
        self._filters_dirty = False
        # Store applied filter values
        self._applied_filters = {
            "roster": "All Rosters",
            "min_games": 1,
            "archetype": "All",
            "rarity": "All"
        }
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title and filters row
        header = QHBoxLayout()

        title = QLabel("Leaderboards")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        header.addWidget(title)

        header.addStretch()

        # Roster filter
        header.addWidget(QLabel("Roster:"))
        self._roster_filter = QComboBox()
        self._roster_filter.setMinimumWidth(120)
        self._populate_rosters()
        self._roster_filter.currentTextChanged.connect(self._on_filter_changed)
        header.addWidget(self._roster_filter)

        # Min games filter
        header.addWidget(QLabel("Min GP:"))
        self._min_games = QSpinBox()
        self._min_games.setRange(0, 100)
        self._min_games.setValue(1)
        self._min_games.valueChanged.connect(self._on_filter_changed)
        header.addWidget(self._min_games)

        # Archetype filter
        header.addWidget(QLabel("Archetype:"))
        self._arch_filter = QComboBox()
        self._arch_filter.addItems(["All", "Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"])
        self._arch_filter.currentTextChanged.connect(self._on_filter_changed)
        header.addWidget(self._arch_filter)

        # Rarity filter
        header.addWidget(QLabel("Rarity:"))
        self._rarity_filter = QComboBox()
        self._rarity_filter.addItems(["All", "Common", "Rare", "Epic", "Legendary", "Godlike"])
        self._rarity_filter.currentTextChanged.connect(self._on_filter_changed)
        header.addWidget(self._rarity_filter)

        # Apply button
        self._apply_btn = QPushButton("Apply")
        self._apply_btn.setMinimumWidth(80)
        self._apply_btn.clicked.connect(self._apply_filters)
        self._apply_btn.setEnabled(False)
        self._update_apply_button_style(False)
        header.addWidget(self._apply_btn)

        layout.addLayout(header)

        # Unified table
        self._table = UnifiedLeaderboardTable()
        self._table.player_selected.connect(self.player_selected)
        layout.addWidget(self._table)

        # Initial load (apply filters immediately on first load)
        self._apply_filters()

    def _update_apply_button_style(self, dirty: bool):
        """Update the Apply button appearance based on dirty state."""
        if dirty:
            self._apply_btn.setText("Apply *")
            self._apply_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_primary']};
                    color: white;
                    border: 2px solid {COLORS['accent_primary']};
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #3b8bdb;
                }}
            """)
            self._apply_btn.setEnabled(True)
        else:
            self._apply_btn.setText("Apply")
            self._apply_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_muted']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: normal;
                }}
            """)
            self._apply_btn.setEnabled(False)

    def _on_filter_changed(self):
        """Called when any filter value changes - check if dirty."""
        current = {
            "roster": self._roster_filter.currentText(),
            "min_games": self._min_games.value(),
            "archetype": self._arch_filter.currentText(),
            "rarity": self._rarity_filter.currentText()
        }
        self._filters_dirty = current != self._applied_filters
        self._update_apply_button_style(self._filters_dirty)

    def _apply_filters(self):
        """Apply the current filter settings and refresh the table."""
        # Store applied values
        self._applied_filters = {
            "roster": self._roster_filter.currentText(),
            "min_games": self._min_games.value(),
            "archetype": self._arch_filter.currentText(),
            "rarity": self._rarity_filter.currentText()
        }
        self._filters_dirty = False
        self._update_apply_button_style(False)
        self._refresh_leaderboard()

    def _populate_rosters(self):
        """Populate the roster dropdown with available rosters."""
        self._roster_filter.addItem("All Rosters")

        # Get unique rosters from games
        games = self._engine.get_games()
        rosters = set()
        for game in games:
            if game.loaded_roster:
                rosters.add(game.loaded_roster)

        for roster in sorted(rosters):
            self._roster_filter.addItem(roster)

        # Try to default to Premier.ROS
        premier_idx = self._roster_filter.findText("Premier.ROS")
        if premier_idx >= 0:
            self._roster_filter.setCurrentIndex(premier_idx)
            self._applied_filters["roster"] = "Premier.ROS"

    def _get_roster_player_ids(self, roster_name: str) -> set:
        """Get all sprite IDs that have played on a specific roster."""
        if roster_name == "All Rosters":
            return None  # No filter

        player_ids = set()
        for game in self._engine.get_games():
            if game.loaded_roster == roster_name:
                for slot_id, slot_info in game.player_slots.items():
                    if slot_info.get("IsActive"):
                        sprite_id = slot_info.get("SpriteID", -1)
                        if sprite_id >= 0:
                            player_ids.add(sprite_id)
        return player_ids

    def _refresh_leaderboard(self):
        """Refresh leaderboard using the applied filter values."""
        min_games = self._applied_filters["min_games"]
        arch = self._applied_filters["archetype"]
        rarity = self._applied_filters["rarity"]
        roster = self._applied_filters["roster"]

        arch_filter = None if arch == "All" else arch.lower()
        rarity_filter = None if rarity == "All" else rarity.lower()
        roster_player_ids = self._get_roster_player_ids(roster)

        # Filter stats
        filtered_stats = []
        for stats in self._engine.get_all_career_stats():
            if stats.games_played < min_games:
                continue
            if arch_filter and stats.archetype.lower() != arch_filter:
                continue
            if rarity_filter and stats.rarity.lower() != rarity_filter:
                continue
            if roster_player_ids is not None and stats.sprite_id not in roster_player_ids:
                continue
            filtered_stats.append(stats)

        # Sort by PPG by default
        filtered_stats.sort(key=lambda s: s.ppg, reverse=True)

        self._table.set_data(filtered_stats)


class GameHistoryWidget(QWidget):
    """Game history browser with full box score display."""

    player_selected = Signal(int)  # Emits sprite_id for navigation to Player Stats

    def __init__(self, engine: StatsEngine):
        super().__init__()
        self._engine = engine
        self._games_data = []  # Store games for sorting
        self._current_game = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("Game History")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        layout.addWidget(title)

        # Games table - now with 9 columns including team compositions
        self._games_table = QTableWidget()
        self._games_table.setColumnCount(10)
        self._games_table.setHorizontalHeaderLabels([
            "ID", "Date", "Roster", "Mode", "Ballerz", "Ringers", "Winner", "Margin", "Ballerz Comp", "Ringers Comp"
        ])

        self._games_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
                gridline-color: {COLORS['border_dark']};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 10px;
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
            }}
            QTableWidget::item:focus {{
                outline: none;
                border: none;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {COLORS['accent_primary']};
                font-weight: 600;
            }}
        """)

        self._games_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._games_table.setSelectionMode(QTableWidget.SingleSelection)
        self._games_table.setFocusPolicy(Qt.NoFocus)  # Fix strikeout outline
        self._games_table.verticalHeader().setVisible(False)
        self._games_table.horizontalHeader().setStretchLastSection(False)

        # Enable sorting
        self._games_table.setSortingEnabled(True)

        # Resize columns - stretch Roster (index 1), others to content
        header = self._games_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Roster (stretch this one)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Mode
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Ballerz
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Ringers
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Winner
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Margin
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Ballerz Comp
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Ringers Comp

        self._games_table.itemSelectionChanged.connect(self._on_game_selected)
        layout.addWidget(self._games_table, stretch=1)

        # Box Score Panel
        self._box_score_panel = QFrame()
        self._box_score_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        self._box_score_panel.setMinimumHeight(280)

        box_layout = QVBoxLayout(self._box_score_panel)
        box_layout.setContentsMargins(16, 12, 16, 12)
        box_layout.setSpacing(12)

        # Game header (shown when game is selected)
        self._game_header = QWidget()
        header_layout = QHBoxLayout(self._game_header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(24)

        # Game info (date, roster, mode)
        self._game_info_left = QLabel()
        self._game_info_left.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
        header_layout.addWidget(self._game_info_left)

        header_layout.addStretch()

        # Winner info
        self._game_info_right = QLabel()
        self._game_info_right.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        self._game_info_right.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self._game_info_right)

        self._game_header.hide()
        box_layout.addWidget(self._game_header)

        # Empty state
        self._empty_box_label = QLabel("Select a game to view the official box score")
        self._empty_box_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
        self._empty_box_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(self._empty_box_label)

        # Box score tables container (side by side)
        self._box_tables_container = QWidget()
        tables_layout = QHBoxLayout(self._box_tables_container)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.setSpacing(16)

        # Ballerz box score
        ballerz_container = QFrame()
        ballerz_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['accent_success']};
                border-radius: 6px;
            }}
        """)
        ballerz_layout = QVBoxLayout(ballerz_container)
        ballerz_layout.setContentsMargins(8, 8, 8, 8)
        ballerz_layout.setSpacing(4)

        # Ballerz header with score on right
        ballerz_header_row = QHBoxLayout()
        ballerz_label = QLabel("BALLERZ")
        ballerz_label.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {COLORS['accent_success']};")
        ballerz_header_row.addWidget(ballerz_label)
        ballerz_header_row.addStretch()
        self._ballerz_score_label = QLabel()
        self._ballerz_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['accent_success']};")
        self._ballerz_score_label.setAlignment(Qt.AlignRight)
        ballerz_header_row.addWidget(self._ballerz_score_label)
        ballerz_layout.addLayout(ballerz_header_row)

        self._ballerz_table = self._create_box_score_table()
        ballerz_layout.addWidget(self._ballerz_table)

        tables_layout.addWidget(ballerz_container)

        # Center divider with hyphen
        center_divider = QLabel("-")
        center_divider.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['text_muted']};")
        center_divider.setAlignment(Qt.AlignCenter)
        center_divider.setFixedWidth(30)
        tables_layout.addWidget(center_divider)

        # Ringers box score
        ringers_container = QFrame()
        ringers_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['accent_warning']};
                border-radius: 6px;
            }}
        """)
        ringers_layout = QVBoxLayout(ringers_container)
        ringers_layout.setContentsMargins(8, 8, 8, 8)
        ringers_layout.setSpacing(4)

        # Ringers header with score on left
        ringers_header_row = QHBoxLayout()
        self._ringers_score_label = QLabel()
        self._ringers_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['accent_warning']};")
        self._ringers_score_label.setAlignment(Qt.AlignLeft)
        ringers_header_row.addWidget(self._ringers_score_label)
        ringers_header_row.addStretch()
        ringers_label = QLabel("RINGERS")
        ringers_label.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {COLORS['accent_warning']};")
        ringers_header_row.addWidget(ringers_label)
        ringers_layout.addLayout(ringers_header_row)

        self._ringers_table = self._create_box_score_table()
        ringers_layout.addWidget(self._ringers_table)

        tables_layout.addWidget(ringers_container)

        self._box_tables_container.hide()
        box_layout.addWidget(self._box_tables_container)

        # Click hint
        self._click_hint = QLabel("Click a player to view their full stats")
        self._click_hint.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-style: italic;")
        self._click_hint.setAlignment(Qt.AlignCenter)
        self._click_hint.hide()
        box_layout.addWidget(self._click_hint)

        layout.addWidget(self._box_score_panel)

        self._load_games()

    def _create_box_score_table(self) -> QTableWidget:
        """Create a box score table for one team."""
        table = QTableWidget()
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["Player", "Arch", "PTS", "AST", "REB", "STL", "BLK", "TO", "FG"])

        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                border: none;
                gridline-color: {COLORS['border_dark']};
            }}
            QTableWidget::item {{
                padding: 4px 6px;
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_muted']};
                padding: 6px 4px;
                border: none;
                font-weight: 600;
                font-size: 10px;
            }}
        """)

        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setMaximumHeight(160)
        table.setSortingEnabled(True)

        # Column sizing
        hdr = table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)  # Player stretches
        for i in range(1, 9):
            hdr.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # Connect double-click to player selection
        table.cellDoubleClicked.connect(lambda r, c, t=table: self._on_box_player_clicked(t, r))

        return table

    def _on_box_player_clicked(self, table: QTableWidget, row: int):
        """Handle click on a player in the box score."""
        item = table.item(row, 0)
        if item:
            sprite_id = item.data(Qt.UserRole)
            if sprite_id is not None and sprite_id >= 0:
                self.player_selected.emit(sprite_id)

    def _get_team_composition(self, game, team: str) -> str:
        """Get archetype composition string for a team (e.g., 'SDDV' colored by archetype)."""
        # Archetype to letter mapping
        arch_letter = {
            "slayer": "S", "vigilante": "V", "medic": "M",
            "guardian": "G", "engineer": "E", "director": "D"
        }

        slot_range = range(5) if team == "ballerz" else range(5, 10)
        letters = []

        for slot_id in slot_range:
            slot = game.player_slots.get(slot_id, {})
            if slot.get("IsActive"):
                sprite_id = slot.get("SpriteID", -1)
                if sprite_id >= 0 and sprite_id in d.players:
                    p = d.players[sprite_id]
                    try:
                        arch = (p["Archetype_Name"] or "").lower()
                        letters.append(arch_letter.get(arch, "?"))
                    except (KeyError, TypeError):
                        letters.append("?")

        return "".join(sorted(letters))

    def _create_colored_comp_item(self, comp_str: str) -> QTableWidgetItem:
        """Create a table item with archetype-colored composition string."""
        item = QTableWidgetItem(comp_str)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        # Use accent color for composition
        item.setForeground(QColor(COLORS['text_secondary']))
        return item

    def _load_games(self):
        games = self._engine.get_games()
        self._games_data = games
        self._games_table.setSortingEnabled(False)  # Disable during loading
        self._games_table.setRowCount(len(games))

        for i, game in enumerate(games):
            # ID (GameID - dimmer text for troubleshooting)
            id_item = QTableWidgetItem()
            id_item.setData(Qt.DisplayRole, game.game_id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setForeground(QColor(COLORS['text_muted']))
            id_item.setData(Qt.UserRole, game)
            self._games_table.setItem(i, 0, id_item)

            # Date
            date_item = QTableWidgetItem(game.play_date or "")
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            self._games_table.setItem(i, 1, date_item)

            # Roster
            roster_item = QTableWidgetItem(game.loaded_roster.replace(".ROS", ""))
            roster_item.setFlags(roster_item.flags() & ~Qt.ItemIsEditable)
            self._games_table.setItem(i, 2, roster_item)

            # Mode
            mode_item = QTableWidgetItem(f"{game.mode}v{game.mode}")
            mode_item.setFlags(mode_item.flags() & ~Qt.ItemIsEditable)
            self._games_table.setItem(i, 3, mode_item)

            # Ballerz score
            ballerz_item = QTableWidgetItem()
            ballerz_item.setData(Qt.DisplayRole, game.ballerz_score)
            ballerz_item.setFlags(ballerz_item.flags() & ~Qt.ItemIsEditable)
            if game.winner == "Ballerz":
                ballerz_item.setForeground(QColor(COLORS['accent_success']))
            else:
                ballerz_item.setForeground(QColor(COLORS['accent_danger']))
            self._games_table.setItem(i, 4, ballerz_item)

            # Ringers score
            ringers_item = QTableWidgetItem()
            ringers_item.setData(Qt.DisplayRole, game.ringers_score)
            ringers_item.setFlags(ringers_item.flags() & ~Qt.ItemIsEditable)
            if game.winner == "Ringers":
                ringers_item.setForeground(QColor(COLORS['accent_success']))
            else:
                ringers_item.setForeground(QColor(COLORS['accent_danger']))
            self._games_table.setItem(i, 5, ringers_item)

            # Winner
            winner_item = QTableWidgetItem(game.winner)
            winner_item.setFlags(winner_item.flags() & ~Qt.ItemIsEditable)
            winner_item.setForeground(QColor(COLORS['accent_primary']))
            self._games_table.setItem(i, 6, winner_item)

            # Margin - use setData for proper numeric sorting
            margin_item = QTableWidgetItem()
            margin_item.setData(Qt.DisplayRole, game.point_differential)
            margin_item.setFlags(margin_item.flags() & ~Qt.ItemIsEditable)
            self._games_table.setItem(i, 7, margin_item)

            # Ballerz Comp
            ballerz_comp = self._get_team_composition(game, "ballerz")
            ballerz_comp_item = self._create_colored_comp_item(ballerz_comp)
            self._games_table.setItem(i, 8, ballerz_comp_item)

            # Ringers Comp
            ringers_comp = self._get_team_composition(game, "ringers")
            ringers_comp_item = self._create_colored_comp_item(ringers_comp)
            self._games_table.setItem(i, 9, ringers_comp_item)

        self._games_table.setSortingEnabled(True)  # Re-enable after loading

    def _on_game_selected(self):
        rows = self._games_table.selectedItems()
        if not rows:
            return

        row = rows[0].row()
        item = self._games_table.item(row, 0)
        game: GameRecord = item.data(Qt.UserRole)

        if not game:
            return

        self._current_game = game

        # Show box score UI
        self._empty_box_label.hide()
        self._game_header.show()
        self._box_tables_container.show()
        self._click_hint.show()

        # Update game header
        self._game_info_left.setText(
            f"<b>{game.play_date}</b> &nbsp;|&nbsp; {game.loaded_roster.replace('.ROS', '')} &nbsp;|&nbsp; {game.mode}v{game.mode}"
        )
        self._game_info_right.setText(f"{game.winner} WIN by {game.point_differential}")

        # Update score labels (winner gets brighter color)
        self._ballerz_score_label.setText(str(game.ballerz_score))
        self._ringers_score_label.setText(str(game.ringers_score))

        # Dim the loser's score
        if game.winner == "Ballerz":
            self._ballerz_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['accent_success']};")
            self._ringers_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['text_muted']};")
        else:
            self._ballerz_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['text_muted']};")
            self._ringers_score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['accent_warning']};")

        # Populate box score tables
        self._populate_box_score(self._ballerz_table, game, range(5))
        self._populate_box_score(self._ringers_table, game, range(5, 10))

    def _populate_box_score(self, table: QTableWidget, game: GameRecord, slot_range):
        """Populate a box score table with player stats."""
        # Collect active players
        players_data = []
        for slot_id in slot_range:
            slot = game.player_slots.get(slot_id, {})
            if slot.get("IsActive"):
                sprite_id = slot.get("SpriteID", -1)
                if sprite_id >= 0 and sprite_id in d.players:
                    p = d.players[sprite_id]
                    # Player objects use [] access, not .get()
                    players_data.append({
                        "sprite_id": sprite_id,
                        "name": f"{p['First_Name']} {p['Last_Name']}",
                        "archetype": p["Archetype_Name"] or "",
                        "points": slot.get("Points", 0) or 0,
                        "assists": slot.get("AssistCount", 0) or 0,
                        "rebounds": (slot.get("OffensiveRebounds", 0) or 0) + (slot.get("DefensiveRebounds", 0) or 0),
                        "steals": slot.get("Steals", 0) or 0,
                        "blocks": slot.get("Blocks", 0) or 0,
                        "turnovers": slot.get("Turnovers", 0) or 0,
                        "fg_made": (slot.get("InsidesMade", 0) or 0) + (slot.get("ThreesMade", 0) or 0),
                        "fg_attempted": (slot.get("InsidesAttempted", 0) or 0) + (slot.get("ThreesAttempted", 0) or 0),
                    })

        # Sort by points (highest first) for initial display
        players_data.sort(key=lambda x: x["points"], reverse=True)

        # Disable sorting while populating
        table.setSortingEnabled(False)
        table.setRowCount(len(players_data))

        for i, pdata in enumerate(players_data):
            # Player name (store sprite_id for navigation)
            name_item = QTableWidgetItem(pdata["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_item.setData(Qt.UserRole, pdata["sprite_id"])
            table.setItem(i, 0, name_item)

            # Archetype (color coded, abbreviated)
            arch = pdata["archetype"]
            arch_abbrev = arch[:3].upper() if arch else "?"
            arch_item = QTableWidgetItem(arch_abbrev)
            arch_item.setFlags(arch_item.flags() & ~Qt.ItemIsEditable)
            arch_style = get_archetype_style(arch)
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            arch_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 1, arch_item)

            # Stats columns - use setData for proper numeric sorting
            stats = [
                pdata["points"],
                pdata["assists"],
                pdata["rebounds"],
                pdata["steals"],
                pdata["blocks"],
                pdata["turnovers"],
            ]

            for j, val in enumerate(stats):
                stat_item = QTableWidgetItem()
                stat_item.setData(Qt.DisplayRole, val)  # Numeric sorting
                stat_item.setFlags(stat_item.flags() & ~Qt.ItemIsEditable)
                stat_item.setTextAlignment(Qt.AlignCenter)
                # Highlight high scores
                if j == 0 and val >= 10:  # Points
                    stat_item.setForeground(QColor(COLORS['accent_primary']))
                table.setItem(i, j + 2, stat_item)

            # FG column
            fg_item = QTableWidgetItem(f"{pdata['fg_made']}/{pdata['fg_attempted']}")
            fg_item.setFlags(fg_item.flags() & ~Qt.ItemIsEditable)
            fg_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 8, fg_item)

        # Re-enable sorting
        table.setSortingEnabled(True)

    def select_game_by_id(self, game_id: int) -> bool:
        """
        Select and scroll to a game by its game_id.
        Returns True if the game was found and selected.
        """
        for row in range(self._games_table.rowCount()):
            item = self._games_table.item(row, 0)
            if item:
                game: GameRecord = item.data(Qt.UserRole)
                if game and game.game_id == game_id:
                    self._games_table.selectRow(row)
                    self._games_table.scrollToItem(item, QTableWidget.PositionAtCenter)
                    return True
        return False


class PlayerStatsWidget(QWidget):
    """
    Full-screen player statistics display.
    Connected to app_state - when a player is selected in the left sidebar player_finder,
    their stats are displayed here.
    """

    # Signal to request navigation to a specific game in Game History
    navigate_to_game = Signal(int)  # Emits game_id

    def __init__(self, engine: StatsEngine):
        super().__init__()
        self._engine = engine
        self._current_sprite_id: Optional[int] = None
        self._setup_ui()
        self._connect_to_app_state()

    def _connect_to_app_state(self):
        """Connect to the app state to listen for player selection changes."""
        from spritopia.gui.app_state import get_app_state
        app_state = get_app_state()
        app_state.selected_player_changed.connect(self._on_player_selected)

        # If a player is already selected, show their stats
        if app_state.selected_player:
            self._on_player_selected(app_state.selected_player)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Main scroll area for the entire content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(32, 32, 32, 32)
        self._content_layout.setSpacing(24)
        self._content_layout.setAlignment(Qt.AlignTop)

        # Empty state
        self._empty_state = self._create_empty_state()
        self._content_layout.addWidget(self._empty_state)

        scroll.setWidget(self._content)
        layout.addWidget(scroll)

    def _create_empty_state(self) -> QWidget:
        """Create the empty state when no player is selected."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        icon = QLabel("📊")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Player Statistics")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Select a player from the sidebar to view their career stats")
        subtitle.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']};")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        hint = QLabel("Use the Player Finder on the left to search and select players")
        hint.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-style: italic;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        return container

    def _on_player_selected(self, player):
        """Handle player selection from app_state."""
        if player is None:
            self._show_empty_state()
            return

        sprite_id = player["SpriteID"]
        if sprite_id == self._current_sprite_id:
            return  # Already showing this player

        self._current_sprite_id = sprite_id
        stats = self._engine.get_career_stats(sprite_id)

        if stats is None or stats.games_played == 0:
            self._show_no_stats_state(player)
        else:
            self._show_player_stats(stats, player)

    def _clear_content(self):
        """Clear all widgets from the content layout."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_empty_state(self):
        """Show the empty state."""
        self._clear_content()
        self._current_sprite_id = None
        self._empty_state = self._create_empty_state()
        self._content_layout.addWidget(self._empty_state)

    def _show_no_stats_state(self, player):
        """Show state when player has no game stats."""
        self._clear_content()

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        name = QLabel(f"{player['First_Name']} {player['Last_Name']}")
        name.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['text_primary']};")
        name.setAlignment(Qt.AlignCenter)
        layout.addWidget(name)

        arch_style = get_archetype_style(player['Archetype_Name'])
        rar_style = get_rarity_style(player['Rarity'])

        info = QLabel(
            f"<span style='color:{arch_style['color']}'>{player['Archetype_Name']}</span> | "
            f"<span style='color:{rar_style['color']}'>{player['Rarity']}</span>"
        )
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        no_stats = QLabel("No game statistics recorded yet")
        no_stats.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']}; margin-top: 24px;")
        no_stats.setAlignment(Qt.AlignCenter)
        layout.addWidget(no_stats)

        hint = QLabel("Play some games with this player to start tracking their stats!")
        hint.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-style: italic;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        self._content_layout.addWidget(container)
        self._content_layout.addStretch()

    def _show_player_stats(self, stats: PlayerCareerStats, player):
        """Show full stats for a player with two-panel layout."""
        self._clear_content()

        # === HEADER BANNER (full width at top) ===
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        header_layout.setSpacing(32)

        # Left side - name and info
        left = QVBoxLayout()
        left.setSpacing(6)

        name_label = QLabel(stats.full_name)
        name_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['text_primary']};")
        left.addWidget(name_label)

        arch_style = get_archetype_style(stats.archetype)
        rar_style = get_rarity_style(stats.rarity)

        info_label = QLabel(
            f"<span style='color:{arch_style['color']}; font-size: 14px;'>{stats.archetype}</span>"
            f"<span style='color:{COLORS['text_muted']}'> | </span>"
            f"<span style='color:{rar_style['color']}; font-size: 14px;'>{stats.rarity}</span>"
            f"<span style='color:{COLORS['text_muted']}'> | </span>"
            f"<span style='color:{COLORS['text_secondary']}; font-size: 14px;'>{stats.faction}</span>"
        )
        left.addWidget(info_label)

        header_layout.addLayout(left, stretch=1)

        # Right side - record
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        record_label = QLabel(f"{stats.wins}W - {stats.losses}L")
        record_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        record_label.setAlignment(Qt.AlignRight)
        right.addWidget(record_label)

        win_pct = QLabel(f"{stats.win_pct*100:.1f}% Win Rate  •  {stats.games_played} Games")
        win_pct.setStyleSheet(f"font-size: 13px; color: {COLORS['text_secondary']};")
        win_pct.setAlignment(Qt.AlignRight)
        right.addWidget(win_pct)

        header_layout.addLayout(right)

        self._content_layout.addWidget(header)

        # === TWO-PANEL LAYOUT ===
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_dark']};
                width: 1px;
            }}
        """)

        # LEFT PANEL: Recent Games (scrollable)
        left_panel = self._create_game_log_panel(stats)
        splitter.addWidget(left_panel)

        # RIGHT PANEL: All aggregated stats
        right_panel = self._create_stats_panel(stats)
        splitter.addWidget(right_panel)

        # Set initial sizes (2:1 ratio - Recent Games is bigger)
        splitter.setSizes([600, 300])
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        self._content_layout.addWidget(splitter, stretch=1)

    def _create_game_log_panel(self, stats: PlayerCareerStats) -> QWidget:
        """Create the left panel with recent games."""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        header = QLabel("Recent Games")
        header.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['accent_primary']};")
        header_row.addWidget(header)
        header_row.addStretch()
        hint = QLabel("Double-click to view game")
        hint.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']}; font-style: italic;")
        header_row.addWidget(hint)
        layout.addLayout(header_row)

        game_log = self._engine.get_player_game_log(stats.sprite_id, limit=50)

        if game_log:
            log_table = QTableWidget()
            log_table.setColumnCount(9)
            log_table.setHorizontalHeaderLabels(["Date", "W/L", "PTS", "AST", "REB", "STL", "BLK", "TO", "FG"])
            log_table.setRowCount(len(game_log))
            log_table.verticalHeader().setVisible(False)
            log_table.setFocusPolicy(Qt.NoFocus)
            log_table.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {COLORS['bg_light']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 6px;
                    gridline-color: {COLORS['border_dark']};
                    outline: none;
                }}
                QTableWidget::item {{
                    padding: 6px 8px;
                }}
                QTableWidget::item:selected {{
                    background-color: {COLORS['accent_primary']};
                }}
                QHeaderView::section {{
                    background-color: {COLORS['bg_medium']};
                    color: {COLORS['text_secondary']};
                    padding: 8px;
                    border: none;
                    font-weight: 600;
                    font-size: 11px;
                }}
            """)

            log_table.setSortingEnabled(True)

            tbl_header = log_table.horizontalHeader()
            tbl_header.setSectionResizeMode(0, QHeaderView.Stretch)  # Date stretches
            for i in range(1, 9):
                tbl_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

            for i, game in enumerate(game_log):
                # Date - store game_id for navigation
                date_item = QTableWidgetItem(game["date"])
                date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                date_item.setData(Qt.UserRole, game["game_id"])  # Store game_id
                log_table.setItem(i, 0, date_item)

                # Result
                result_item = QTableWidgetItem(game["result"])
                result_item.setFlags(result_item.flags() & ~Qt.ItemIsEditable)
                if game["result"] == "W":
                    result_item.setForeground(QColor(COLORS['accent_success']))
                else:
                    result_item.setForeground(QColor(COLORS['accent_danger']))
                log_table.setItem(i, 1, result_item)

                # Stats - use setData for proper numeric sorting
                for j, key in enumerate(["points", "assists", "rebounds", "steals", "blocks", "turnovers"]):
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, game[key])
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    log_table.setItem(i, j + 2, item)

                # FG
                fg_item = QTableWidgetItem(f"{game['fg_made']}/{game['fg_attempted']}")
                fg_item.setFlags(fg_item.flags() & ~Qt.ItemIsEditable)
                log_table.setItem(i, 8, fg_item)

            # Connect double-click to navigate to game history
            log_table.cellDoubleClicked.connect(self._on_game_double_click)
            self._game_log_table = log_table  # Store reference for double-click handler

            layout.addWidget(log_table, stretch=1)
        else:
            no_games = QLabel("No games played yet")
            no_games.setStyleSheet(f"color: {COLORS['text_muted']}; font-style: italic;")
            no_games.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_games, stretch=1)

        return panel

    def _on_game_double_click(self, row: int, col: int):
        """Handle double-click on a game to navigate to Game History."""
        if hasattr(self, '_game_log_table'):
            item = self._game_log_table.item(row, 0)
            if item:
                game_id = item.data(Qt.UserRole)
                if game_id is not None:
                    self.navigate_to_game.emit(game_id)

    def _create_stats_panel(self, stats: PlayerCareerStats) -> QWidget:
        """Create the right panel with all aggregated stats."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        # === PER-GAME AVERAGES ===
        avg_header = QLabel("Per-Game Averages")
        avg_header.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']};")
        layout.addWidget(avg_header)

        avg_grid = QGridLayout()
        avg_grid.setSpacing(8)
        avg_stats = [
            ("PPG", f"{stats.ppg:.1f}", "Points Per Game"),
            ("APG", f"{stats.apg:.1f}", "Assists Per Game"),
            ("RPG", f"{stats.rpg:.1f}", "Rebounds Per Game"),
            ("SPG", f"{stats.spg:.1f}", "Steals Per Game"),
            ("BPG", f"{stats.bpg:.1f}", "Blocks Per Game"),
            ("TPG", f"{stats.tpg:.1f}", "Turnovers Per Game"),
        ]
        for i, (abbr, value, tooltip) in enumerate(avg_stats):
            avg_grid.addWidget(self._create_compact_stat(abbr, value, tooltip), i // 3, i % 3)
        layout.addLayout(avg_grid)

        # === SHOOTING SPLITS ===
        shoot_header = QLabel("Shooting")
        shoot_header.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']}; margin-top: 8px;")
        layout.addWidget(shoot_header)

        shoot_grid = QGridLayout()
        shoot_grid.setSpacing(8)
        shoot_stats = [
            ("FG%", f"{stats.fg_pct*100:.1f}%", "Field Goal Percentage"),
            ("2P%", f"{stats.two_pt_pct*100:.1f}%", "Two-Point Percentage"),
            ("3P%", f"{stats.three_pt_pct*100:.1f}%", "Three-Point Percentage"),
            ("TS%", f"{stats.ts_pct*100:.1f}%", "True Shooting %"),
            ("eFG%", f"{stats.efg_pct*100:.1f}%", "Effective FG%"),
            ("3PT Rate", f"{stats.three_pt_rate*100:.1f}%", "% of shots from 3"),
        ]
        for i, (abbr, value, tooltip) in enumerate(shoot_stats):
            shoot_grid.addWidget(self._create_compact_stat(abbr, value, tooltip), i // 3, i % 3)
        layout.addLayout(shoot_grid)

        # === ADVANCED METRICS ===
        adv_header = QLabel("Advanced")
        adv_header.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']}; margin-top: 8px;")
        layout.addWidget(adv_header)

        adv_grid = QGridLayout()
        adv_grid.setSpacing(8)
        adv_stats = [
            ("EFF", f"{stats.efficiency_rating:.1f}", "Efficiency Rating"),
            ("GmSc", f"{stats.game_score_avg:.1f}", "Game Score (Hollinger)"),
            ("AST/TO", f"{stats.ast_to_ratio:.2f}", "Assist/Turnover Ratio"),
            ("PTS Created", f"{stats.points_created_per_game:.1f}", "Points + Assisted Points"),
            ("Dunk Rate", f"{stats.dunk_rate*100:.0f}%", "% of inside = dunks"),
            ("Layup Rate", f"{stats.layup_rate*100:.0f}%", "% of inside = layups"),
        ]
        for i, (abbr, value, tooltip) in enumerate(adv_stats):
            adv_grid.addWidget(self._create_compact_stat(abbr, value, tooltip), i // 3, i % 3)
        layout.addLayout(adv_grid)

        # === CAREER TOTALS ===
        totals_header = QLabel("Career Totals")
        totals_header.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']}; margin-top: 8px;")
        layout.addWidget(totals_header)

        totals_grid = QGridLayout()
        totals_grid.setSpacing(8)
        totals_stats = [
            ("Points", str(stats.total_points), "Total points scored"),
            ("Assists", str(stats.total_assists), "Total assists"),
            ("Rebounds", str(stats.total_rebounds), "Total rebounds"),
            ("Steals", str(stats.total_steals), "Total steals"),
            ("Blocks", str(stats.total_blocks), "Total blocks"),
            ("Turnovers", str(stats.total_turnovers), "Total turnovers"),
            ("Dunks", str(stats.total_dunks), "Total dunks"),
            ("Layups", str(stats.total_layups), "Total layups"),
            ("FGM/FGA", f"{stats.fg_made}/{stats.fg_attempted}", "Field goals made/attempted"),
            ("3PM/3PA", f"{stats.threes_made}/{stats.threes_attempted}", "3-pointers made/attempted"),
        ]
        for i, (abbr, value, tooltip) in enumerate(totals_stats):
            totals_grid.addWidget(self._create_compact_stat(abbr, value, tooltip, small=True), i // 5, i % 5)
        layout.addLayout(totals_grid)

        layout.addStretch()
        scroll.setWidget(panel)
        return scroll

    def _create_compact_stat(self, label: str, value: str, tooltip: str = "", small: bool = False) -> QFrame:
        """Create a compact stat display for the right panel."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)
        if tooltip:
            card.setToolTip(tooltip)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        val_size = "18px" if not small else "14px"
        val_label = QLabel(value)
        val_label.setStyleSheet(f"font-size: {val_size}; font-weight: bold; color: {COLORS['text_primary']};")
        val_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(val_label)

        name_label = QLabel(label)
        name_label.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']};")
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        return card

    def _create_section(self, title: str) -> QFrame:
        """Create a styled section container."""
        section = QFrame()
        section.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        header = QLabel(title)
        header.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['accent_primary']};")
        layout.addWidget(header)

        return section

    def _create_stat_card(self, label: str, value: str, tooltip: str = "", small: bool = False) -> QFrame:
        """Create a mini stat card."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        if tooltip:
            card.setToolTip(tooltip)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        val_label = QLabel(value)
        val_size = "24px" if not small else "20px"
        val_label.setStyleSheet(f"font-size: {val_size}; font-weight: bold; color: {COLORS['text_primary']};")
        val_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(val_label)

        name_label = QLabel(label)
        name_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        return card

    def select_player(self, sprite_id: int):
        """Programmatically select a player by sprite_id (for backwards compat)."""
        from spritopia.gui.app_state import get_app_state
        from spritopia.data_storage.data_storage import d

        if sprite_id in d.players:
            get_app_state().selected_player = d.players[sprite_id]


class RecordsWidget(QWidget):
    """All-time records display: career totals, single-game highs, and game superlatives."""

    def __init__(self, engine: StatsEngine):
        super().__init__()
        self._engine = engine
        self._setup_ui()

    def _build_record_card(self, category: str, value_text: str, player_name: str,
                           detail_text: str, accent_border: bool = False) -> QFrame:
        """Build a styled record card."""
        card = QFrame()
        border_color = COLORS['accent_primary'] if accent_border else COLORS['border_dark']
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(6)

        cat_label = QLabel(category)
        cat_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(cat_label)

        val_label = QLabel(value_text)
        val_label.setStyleSheet(f"color: {COLORS['accent_primary']}; font-size: 36px; font-weight: bold;")
        card_layout.addWidget(val_label)

        player_label = QLabel(player_name)
        player_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: 600;")
        card_layout.addWidget(player_label)

        detail_label = QLabel(detail_text)
        detail_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        card_layout.addWidget(detail_label)

        return card

    def _build_section_header(self, text: str) -> QLabel:
        """Build a section header label."""
        label = QLabel(text)
        label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid {COLORS['border_dark']};
        """)
        return label

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("All-Time Records")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        layout.addWidget(title)

        subtitle = QLabel("Career totals and single-game highs across all players")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; margin-bottom: 16px;")
        layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        grid = QGridLayout(content)
        grid.setSpacing(16)

        current_row = 0

        # ── Career Records ──
        career_header = QLabel("Career Records")
        career_header.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            padding-bottom: 4px;
        """)
        grid.addWidget(career_header, current_row, 0, 1, 2)
        current_row += 1

        career_records = self._engine.get_career_records(min_games_for_pct=20)

        career_info = [
            ("total_points", "Total Points"),
            ("total_rebounds", "Total Rebounds"),
            ("total_assists", "Total Assists"),
            ("threes_made", "3-Pointers Made"),
            ("three_pt_pct", "3-Point % (20 GP min)"),
            ("wins", "Wins"),
            ("total_steals", "Total Steals"),
            ("total_blocks", "Total Blocks"),
            ("games_played", "Games Played"),
            ("total_dunks", "Total Dunks"),
            ("fg_made", "Field Goals Made"),
            ("total_turnovers", "Total Turnovers"),
        ]

        for i, (key, label) in enumerate(career_info):
            rec = career_records.get(key, {"display_value": "0", "player_name": "N/A", "games_played": 0})
            detail = f"{rec['games_played']} games played"
            card = self._build_record_card(label, rec["display_value"], rec["player_name"] or "N/A", detail)
            grid.addWidget(card, current_row + i // 2, i % 2)

        current_row += (len(career_info) + 1) // 2

        # ── Single Game Highs ──
        grid.addWidget(self._build_section_header("Single Game Highs"), current_row, 0, 1, 2)
        current_row += 1

        single_game_records = self._engine.get_single_game_records()

        single_game_info = [
            ("points", "Points"),
            ("assists", "Assists"),
            ("rebounds", "Rebounds"),
            ("steals", "Steals"),
            ("blocks", "Blocks"),
            ("dunks", "Dunks"),
            ("threes_made", "3-Pointers Made"),
            ("insides_made", "Field Goals Made"),
            ("offensive_rebounds", "Offensive Rebounds"),
            ("defensive_rebounds", "Defensive Rebounds"),
        ]

        for i, (key, label) in enumerate(single_game_info):
            rec = single_game_records.get(key, {"value": 0, "player_name": "N/A", "game_date": "N/A"})
            card = self._build_record_card(
                label, str(rec["value"]), rec["player_name"] or "N/A", rec["game_date"] or "Unknown"
            )
            grid.addWidget(card, current_row + i // 2, i % 2)

        current_row += (len(single_game_info) + 1) // 2

        # ── Game Superlatives ──
        grid.addWidget(self._build_section_header("Game Superlatives"), current_row, 0, 1, 2)
        current_row += 1

        superlatives = self._engine.get_game_superlatives()
        sup_keys = ["closest_game", "biggest_blowout", "highest_scoring", "lowest_scoring"]

        for j, key in enumerate(sup_keys):
            if key not in superlatives:
                continue
            sup = superlatives[key]
            card = self._build_record_card(
                sup["label"], sup["value"], sup["detail"], sup["date"],
                accent_border=True
            )
            grid.addWidget(card, current_row + j // 2, j % 2)

        grid.setRowStretch(grid.rowCount(), 1)
        scroll.setWidget(content)
        layout.addWidget(scroll)


class StatsCenterWidget(QWidget):
    """
    Main Stats Center widget combining all statistics views.
    """

    # Signal to notify external widgets (like player finder) of player selection
    player_selected_external = Signal(int)  # Emits sprite_id

    def __init__(self):
        super().__init__()
        self._engine: Optional[StatsEngine] = None
        self._setup_ui()
        self._load_stats()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Main tabs
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 12px 24px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['bg_card']};
            }}
        """)

        # Placeholder until stats are loaded
        self._loading_label = QLabel("Loading statistics...")
        self._loading_label.setAlignment(Qt.AlignCenter)
        self._loading_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 18px;")
        layout.addWidget(self._loading_label)

        self._tabs.hide()
        layout.addWidget(self._tabs)

    def _load_stats(self):
        """Load statistics from the database."""
        try:
            # Ensure stats are downloaded
            if not hasattr(d, 'stats') or not d.stats.get("Raw"):
                d.statsDB_Open()
                d.statsDB_DownloadRaw()

            raw_stats = d.stats.get("Raw", {})
            players_dict = d.players

            if not raw_stats:
                self._loading_label.setText("No game statistics found.\n\nPlay some games to start tracking stats!")
                return

            self._engine = StatsEngine(raw_stats, players_dict)
            self._build_tabs()

        except Exception as e:
            self._loading_label.setText(f"Error loading statistics:\n{str(e)}")

    def _build_tabs(self):
        """Build the tab widgets after stats are loaded."""
        self._loading_label.hide()

        # Dashboard
        self._dashboard = DashboardWidget(self._engine)
        self._tabs.addTab(self._dashboard, "Dashboard")

        # Leaderboards
        self._leaderboards = LeaderboardsWidget(self._engine)
        self._leaderboards.player_selected.connect(self._on_player_selected)
        self._tabs.addTab(self._leaderboards, "Leaderboards")

        # Game History
        self._game_history = GameHistoryWidget(self._engine)
        self._game_history.player_selected.connect(self._on_player_selected)
        self._tabs.addTab(self._game_history, "Game History")

        # Player Stats (connected to sidebar player_finder)
        self._player_stats = PlayerStatsWidget(self._engine)
        self._player_stats.navigate_to_game.connect(self._on_navigate_to_game)
        self._tabs.addTab(self._player_stats, "Player Stats")

        # Records
        self._records = RecordsWidget(self._engine)
        self._tabs.addTab(self._records, "Records")

        self._tabs.show()

    def _on_player_selected(self, sprite_id: int):
        """Handle player selection from leaderboards - switch to player stats."""
        self._tabs.setCurrentIndex(3)  # Player Stats tab
        self._player_stats.select_player(sprite_id)
        # Also emit signal for external widgets (like player finder)
        self.player_selected_external.emit(sprite_id)

    def _on_navigate_to_game(self, game_id: int):
        """Handle navigation to a specific game in Game History."""
        self._tabs.setCurrentIndex(2)  # Game History tab
        self._game_history.select_game_by_id(game_id)

    def refresh(self):
        """Refresh all statistics."""
        self._load_stats()
