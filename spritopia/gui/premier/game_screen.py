"""
Game Screen — live box score display during Pre-Game, Playing, and Post-Game phases.

Phases:
  Pre-Game  — auto-loads players into 2K13 picker screen (with auto-load toggle)
  Playing   — live box score updates from tracker stat rips
  Post-Game — final results + auto-save status + insights + MVP selector
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor

from spritopia.gui.theme import COLORS, get_archetype_style
from spritopia.gui.tracker_bridge import get_tracker_bridge
from spritopia.data_storage.data_storage import d
from spritopia.common.logger import log


# Team constants (match picker.py)
_TEAM_COLORS = {1: "#4a9eff", 2: "#ef4444"}  # blue / red
_TEAM_NAMES  = {1: "Ballerz", 2: "Ringers"}

# Stat-leader cell highlighting (amber / gold tones)
_LEADER_BG = QColor(245, 158, 11, 35)
_LEADER_FG = QColor(245, 158, 11)
_RECORD_BG = QColor(245, 158, 11, 80)
_RECORD_FG = QColor(255, 210, 60)


class GameScreen(QWidget):
    """Live game screen showing box score across Pre-Game / Playing / Post-Game."""

    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = "idle"
        self._team1 = []
        self._team2 = []
        self._match_config = {}
        self._auto_load = True
        self._load_success = False
        self._save_status = ""
        self._last_stats = None
        self._signals_connected = False
        self._last_all_rows = []    # all player rows from the most-recent completed game
        self._mvp_chips = {}        # sprite_id → QPushButton
        self._selected_mvp = None   # sprite_id of the selected MVP
        self._mvp_suggestion = None  # (name, stats_text, reason_text) for restoring on deselect

        self._auto_load_timer = QTimer(self)
        self._auto_load_timer.setInterval(2000)
        self._auto_load_timer.timeout.connect(self._try_auto_load)

        self._setup_ui()

    # ── UI Setup ──────────────────────────────────────────────────────────────

    def _setup_ui(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # Phase banner
        self._banner = QLabel("PRE-GAME")
        self._banner.setAlignment(Qt.AlignCenter)
        self._banner.setFixedHeight(64)
        self._banner.setStyleSheet(self._banner_style("Pre-Game"))
        lo.addWidget(self._banner)

        # Score header
        score_bar = QFrame()
        score_bar.setFixedHeight(56)
        score_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        score_lo = QHBoxLayout(score_bar)
        score_lo.setContentsMargins(40, 0, 40, 0)
        score_lo.setSpacing(0)

        self._ballerz_name = QLabel("BALLERZ")
        self._ballerz_name.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {_TEAM_COLORS[1]};")
        score_lo.addWidget(self._ballerz_name)

        self._ballerz_score = QLabel("0")
        self._ballerz_score.setStyleSheet(
            f"font-size: 28px; font-weight: bold; color: {_TEAM_COLORS[1]}; padding: 0 16px;")
        score_lo.addWidget(self._ballerz_score)

        score_lo.addStretch()
        dash = QLabel("—")
        dash.setStyleSheet(f"font-size: 22px; color: {COLORS['text_muted']};")
        score_lo.addWidget(dash)
        score_lo.addStretch()

        self._ringers_score = QLabel("0")
        self._ringers_score.setStyleSheet(
            f"font-size: 28px; font-weight: bold; color: {_TEAM_COLORS[2]}; padding: 0 16px;")
        score_lo.addWidget(self._ringers_score)

        self._ringers_name = QLabel("RINGERS")
        self._ringers_name.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {_TEAM_COLORS[2]};")
        score_lo.addWidget(self._ringers_name)

        lo.addWidget(score_bar)

        # Box score area
        box_area = QWidget()
        box_lo = QHBoxLayout(box_area)
        box_lo.setContentsMargins(24, 16, 24, 16)
        box_lo.setSpacing(20)

        ballerz_col = QVBoxLayout()
        ballerz_col.setSpacing(4)
        b_hdr = QLabel("BALLERZ")
        b_hdr.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {_TEAM_COLORS[1]}; letter-spacing: 1px;")
        ballerz_col.addWidget(b_hdr)
        self._ballerz_table = self._create_box_table()
        ballerz_col.addWidget(self._ballerz_table)
        box_lo.addLayout(ballerz_col, stretch=1)

        ringers_col = QVBoxLayout()
        ringers_col.setSpacing(4)
        r_hdr = QLabel("RINGERS")
        r_hdr.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {_TEAM_COLORS[2]}; letter-spacing: 1px;")
        ringers_col.addWidget(r_hdr)
        self._ringers_table = self._create_box_table()
        ringers_col.addWidget(self._ringers_table)
        box_lo.addLayout(ringers_col, stretch=1)

        lo.addWidget(box_area, stretch=1)

        # ── Post-game insight panel ──────────────────────────────────────────
        self._postgame_insight_panel = QFrame()
        self._postgame_insight_panel.setFixedHeight(400)
        self._postgame_insight_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-top: 2px solid {COLORS['border_dark']};
            }}
        """)
        insight_lo = QHBoxLayout(self._postgame_insight_panel)
        insight_lo.setContentsMargins(24, 12, 24, 12)
        insight_lo.setSpacing(0)

        # Left column: game notes / tidbits
        tidbits_col = QVBoxLayout()
        tidbits_col.setSpacing(5)
        tidbits_col.setContentsMargins(0, 0, 16, 0)

        notes_hdr = QLabel("GAME NOTES")
        notes_hdr.setStyleSheet(
            f"font-size: 10px; font-weight: bold; color: {COLORS['text_muted']}; "
            f"letter-spacing: 2px; margin-bottom: 2px;")
        tidbits_col.addWidget(notes_hdr)

        self._tidbit_labels = []
        for _ in range(10):
            lbl = QLabel("")
            lbl.setWordWrap(True)
            lbl.setVisible(False)
            self._tidbit_labels.append(lbl)
            tidbits_col.addWidget(lbl)

        self._tidbit_overflow_lbl = QLabel("")
        self._tidbit_overflow_lbl.setVisible(False)
        self._tidbit_overflow_lbl.setWordWrap(True)
        self._tidbit_overflow_lbl.setToolTip("")
        self._tidbit_overflow_lbl.setStyleSheet(
            f"font-size: 10px; color: {COLORS['text_muted']}; "
            f"padding: 2px 8px; font-style: italic; cursor: pointer;")
        tidbits_col.addWidget(self._tidbit_overflow_lbl)
        tidbits_col.addStretch()
        insight_lo.addLayout(tidbits_col, stretch=55)

        # Vertical divider
        vdiv = QFrame()
        vdiv.setFrameShape(QFrame.VLine)
        vdiv.setStyleSheet(f"color: {COLORS['border_dark']}; max-width: 1px;")
        insight_lo.addWidget(vdiv)

        # Right column: MVP selector
        mvp_col = QVBoxLayout()
        mvp_col.setSpacing(6)
        mvp_col.setContentsMargins(20, 0, 0, 0)

        mvp_hdr = QLabel("GAME MVP")
        mvp_hdr.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #f59e0b; letter-spacing: 2px; margin-bottom: 2px;")
        mvp_col.addWidget(mvp_hdr)

        self._mvp_selected_lbl = QLabel("— select a player —")
        self._mvp_selected_lbl.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {COLORS['text_muted']};")
        mvp_col.addWidget(self._mvp_selected_lbl)

        self._mvp_stats_lbl = QLabel("")
        self._mvp_stats_lbl.setWordWrap(True)
        self._mvp_stats_lbl.setStyleSheet(
            f"font-size: 12px; color: {COLORS['text_muted']}; padding: 2px 0 2px 0;")
        self._mvp_stats_lbl.setVisible(False)
        mvp_col.addWidget(self._mvp_stats_lbl)

        self._mvp_reason_lbl = QLabel("")
        self._mvp_reason_lbl.setWordWrap(True)
        self._mvp_reason_lbl.setStyleSheet(
            f"font-size: 10px; color: {COLORS['text_muted']}; font-style: italic; padding-bottom: 8px;")
        self._mvp_reason_lbl.setVisible(False)
        mvp_col.addWidget(self._mvp_reason_lbl)

        t1_team_lbl = QLabel("BALLERZ")
        t1_team_lbl.setStyleSheet(
            f"font-size: 9px; font-weight: bold; color: {_TEAM_COLORS[1]}; letter-spacing: 1px;")
        mvp_col.addWidget(t1_team_lbl)

        self._mvp_t1_chips_lo = QHBoxLayout()
        self._mvp_t1_chips_lo.setSpacing(6)
        self._mvp_t1_chips_lo.setContentsMargins(0, 2, 0, 0)
        t1_chip_w = QWidget()
        t1_chip_w.setLayout(self._mvp_t1_chips_lo)
        mvp_col.addWidget(t1_chip_w)

        t2_team_lbl = QLabel("RINGERS")
        t2_team_lbl.setStyleSheet(
            f"font-size: 9px; font-weight: bold; color: {_TEAM_COLORS[2]}; letter-spacing: 1px; margin-top: 8px;")
        mvp_col.addWidget(t2_team_lbl)

        self._mvp_t2_chips_lo = QHBoxLayout()
        self._mvp_t2_chips_lo.setSpacing(6)
        self._mvp_t2_chips_lo.setContentsMargins(0, 2, 0, 0)
        t2_chip_w = QWidget()
        t2_chip_w.setLayout(self._mvp_t2_chips_lo)
        mvp_col.addWidget(t2_chip_w)

        mvp_col.addStretch()

        insight_lo.addLayout(mvp_col, stretch=45)

        self._postgame_insight_panel.setVisible(False)
        lo.addWidget(self._postgame_insight_panel)

        # ── Pre-game notes panel ─────────────────────────────────────────────
        self._pregame_notes_panel = QFrame()
        self._pregame_notes_panel.setFixedHeight(210)
        self._pregame_notes_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-top: 2px solid {COLORS['border_dark']};
            }}
        """)
        pn_lo = QHBoxLayout(self._pregame_notes_panel)
        pn_lo.setContentsMargins(24, 12, 24, 12)
        pn_lo.setSpacing(0)
        pn_col = QVBoxLayout()
        pn_col.setSpacing(5)
        pn_col.setContentsMargins(0, 0, 0, 0)
        pn_hdr = QLabel("MATCH PREVIEW")
        pn_hdr.setStyleSheet(
            f"font-size: 10px; font-weight: bold; color: {COLORS['text_muted']}; "
            f"letter-spacing: 2px; margin-bottom: 2px;")
        pn_col.addWidget(pn_hdr)
        self._pregame_note_labels = []
        for _ in range(5):
            lbl = QLabel("")
            lbl.setWordWrap(True)
            lbl.setVisible(False)
            self._pregame_note_labels.append(lbl)
            pn_col.addWidget(lbl)
        pn_col.addStretch()
        pn_lo.addLayout(pn_col)
        self._pregame_notes_panel.setVisible(False)
        lo.addWidget(self._pregame_notes_panel)

        # ── Pre-game controls panel ──────────────────────────────────────────
        self._pregame_panel = QFrame()
        self._pregame_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        pg_lo = QHBoxLayout(self._pregame_panel)
        pg_lo.setContentsMargins(24, 10, 24, 10)
        pg_lo.setSpacing(12)

        self._auto_load_cb = QCheckBox("Auto Load")
        self._auto_load_cb.setChecked(True)
        self._auto_load_cb.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        self._auto_load_cb.toggled.connect(self._on_auto_load_toggled)
        pg_lo.addWidget(self._auto_load_cb)

        self._manual_load_btn = QPushButton("Load Manually")
        self._manual_load_btn.setFixedHeight(30)
        self._manual_load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                font-size: 11px;
                padding: 0 12px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_primary']}; color: white; }}
        """)
        self._manual_load_btn.clicked.connect(self._on_manual_load)
        self._manual_load_btn.setVisible(False)
        pg_lo.addWidget(self._manual_load_btn)

        self._load_status_lbl = QLabel("")
        self._load_status_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        pg_lo.addWidget(self._load_status_lbl, stretch=1)

        pg_lo.addStretch()

        self._sim_btn = QPushButton("⚡ Sim Post-Game")
        self._sim_btn.setFixedHeight(30)
        self._sim_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_warning']};
                border: 1px solid {COLORS['accent_warning']};
                border-radius: 4px;
                font-size: 11px;
                padding: 0 12px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_warning']}; color: #0d1117; }}
        """)
        self._sim_btn.clicked.connect(self._simulate_postgame)
        pg_lo.addWidget(self._sim_btn)

        self._pregame_cancel_btn = self._make_cancel_button("Cancel Game")
        self._pregame_cancel_btn.clicked.connect(self.back_requested)
        pg_lo.addWidget(self._pregame_cancel_btn)

        lo.addWidget(self._pregame_panel)

        # ── Playing-phase bar ────────────────────────────────────────────────
        self._playing_panel = QFrame()
        self._playing_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        play_lo = QHBoxLayout(self._playing_panel)
        play_lo.setContentsMargins(24, 8, 24, 8)
        play_lo.addStretch()

        self._playing_cancel_btn = self._make_cancel_button("Cancel Game")
        self._playing_cancel_btn.clicked.connect(self.back_requested)
        play_lo.addWidget(self._playing_cancel_btn)

        self._playing_panel.setVisible(False)
        lo.addWidget(self._playing_panel)

        # ── Post-game status bar ─────────────────────────────────────────────
        self._postgame_bar = QFrame()
        self._postgame_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        post_lo = QHBoxLayout(self._postgame_bar)
        post_lo.setContentsMargins(24, 8, 24, 8)

        post_status_col = QVBoxLayout()
        post_status_col.setContentsMargins(0, 0, 0, 0)
        post_status_col.setSpacing(2)

        self._save_status_lbl = QLabel("")
        self._save_status_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        post_status_col.addWidget(self._save_status_lbl)

        self._ballholding_warning_lbl = QLabel("")
        self._ballholding_warning_lbl.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {COLORS['accent_warning']};")
        self._ballholding_warning_lbl.setVisible(False)
        post_status_col.addWidget(self._ballholding_warning_lbl)

        post_lo.addLayout(post_status_col, stretch=1)

        self._rematch_btn = QPushButton("↺ Rematch")
        self._rematch_btn.setFixedHeight(32)
        self._rematch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 16px;
            }}
            QPushButton:hover {{ background-color: #3b8bdb; }}
        """)
        self._rematch_btn.clicked.connect(self._on_rematch)
        post_lo.addWidget(self._rematch_btn)

        self._back_btn = QPushButton("← Back to Setup")
        self._back_btn.setFixedHeight(32)
        self._back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                font-size: 12px;
                padding: 0 14px;
            }}
            QPushButton:hover {{ color: {COLORS['text_primary']}; border-color: {COLORS['text_muted']}; }}
        """)
        self._back_btn.clicked.connect(self.back_requested)
        post_lo.addWidget(self._back_btn)

        self._postgame_bar.setVisible(False)
        lo.addWidget(self._postgame_bar)

    def _create_box_table(self):
        table = QTableWidget()
        table.setColumnCount(11)
        table.setHorizontalHeaderLabels(
            ["Player", "Arch", "PTS", "AST", "REB", "STL", "BLK", "TO", "1s", "3P", "TH"])
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
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_muted']};
                padding: 6px 4px;
                border: none;
                font-weight: 600;
                font-size: 10px;
            }}
        """)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        hdr = table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 11):
            hdr.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        return table

    # ── Banner styling ────────────────────────────────────────────────────────

    def _banner_style(self, phase):
        if phase == "Pre-Game":
            bg, border, color = COLORS['bg_medium'], COLORS['accent_primary'], COLORS['accent_primary']
        elif phase == "Playing":
            bg, border, color = "#0a2e1a", COLORS['accent_success'], COLORS['accent_success']
        elif phase == "Post-Game":
            bg, border, color = COLORS['bg_dark'], COLORS['text_muted'], COLORS['text_primary']
        else:
            bg, border, color = COLORS['bg_dark'], COLORS['border_dark'], COLORS['text_muted']
        return (
            f"font-size: 22px; font-weight: bold; color: {color}; letter-spacing: 3px; "
            f"background-color: {bg}; border-bottom: 2px solid {border};"
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def start_game(self, team1, team2, config):
        """Enter pre-game phase with the drafted teams."""
        self._team1 = team1
        self._team2 = team2
        self._match_config = config
        self._load_success = False
        self._save_status = ""
        self._last_stats = None
        self._last_all_rows = []
        self._mvp_chips = {}
        self._selected_mvp = None
        self._mvp_suggestion = None
        for lbl in self._pregame_note_labels:
            lbl.setVisible(False)
        self._save_status_lbl.setText("")
        self._ballholding_warning_lbl.setText("")
        self._ballholding_warning_lbl.setVisible(False)
        self._postgame_insight_panel.setVisible(False)

        self._set_phase("pre_game")

        self._populate_team_table(self._ballerz_table, team1)
        self._populate_team_table(self._ringers_table, team2)
        self._ballerz_score.setText("0")
        self._ringers_score.setText("0")

        self._build_pregame_content(team1, team2)

        bridge = get_tracker_bridge()
        if not self._signals_connected:
            bridge.location_changed.connect(self._on_location_changed)
            bridge.game_status_changed.connect(self._on_game_status_changed)
            bridge.live_stats.connect(self._on_live_stats)
            bridge.game_won.connect(self._on_game_won)
            self._signals_connected = True

        if self._auto_load:
            self._auto_load_timer.start()
            self._try_auto_load()

    def stop(self):
        """Disconnect signals and stop timers."""
        self._auto_load_timer.stop()
        if self._signals_connected:
            try:
                bridge = get_tracker_bridge()
                bridge.location_changed.disconnect(self._on_location_changed)
                bridge.game_status_changed.disconnect(self._on_game_status_changed)
                bridge.live_stats.disconnect(self._on_live_stats)
                bridge.game_won.disconnect(self._on_game_won)
            except (RuntimeError, TypeError):
                pass
            self._signals_connected = False

    # ── Phase management ──────────────────────────────────────────────────────

    def _set_phase(self, phase):
        self._phase = phase

        if phase == "pre_game":
            self._banner.setText("PRE-GAME")
            self._banner.setStyleSheet(self._banner_style("Pre-Game"))
            self._pregame_panel.setVisible(True)
            self._playing_panel.setVisible(False)
            self._postgame_bar.setVisible(False)
            self._postgame_insight_panel.setVisible(False)
            self._pregame_notes_panel.setVisible(True)
        elif phase == "playing":
            self._banner.setText("PLAYING")
            self._banner.setStyleSheet(self._banner_style("Playing"))
            self._pregame_panel.setVisible(False)
            self._playing_panel.setVisible(True)
            self._postgame_bar.setVisible(False)
            self._postgame_insight_panel.setVisible(False)
            self._pregame_notes_panel.setVisible(False)
            self._auto_load_timer.stop()
        elif phase == "post_game":
            self._banner.setText("POST-GAME")
            self._banner.setStyleSheet(self._banner_style("Post-Game"))
            self._pregame_panel.setVisible(False)
            self._playing_panel.setVisible(False)
            self._postgame_bar.setVisible(True)
            self._pregame_notes_panel.setVisible(False)
            # insight panel revealed after _build_postgame_insights populates it

    def _make_cancel_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                font-size: 12px;
                padding: 0 14px;
            }}
            QPushButton:hover {{
                color: {COLORS['accent_danger']};
                border-color: {COLORS['accent_danger']};
            }}
        """)
        return btn

    # ── Pre-game: auto-load ───────────────────────────────────────────────────

    def _on_auto_load_toggled(self, checked):
        self._auto_load = checked
        self._manual_load_btn.setVisible(not checked)
        if checked and self._phase == "pre_game":
            self._auto_load_timer.start()
        else:
            self._auto_load_timer.stop()

    def _on_manual_load(self):
        self._try_auto_load()

    def _try_auto_load(self):
        if self._phase != "pre_game":
            self._auto_load_timer.stop()
            return
        if self._load_success:
            self._load_status_lbl.setText("Players loaded successfully.")
            self._load_status_lbl.setStyleSheet(
                f"font-size: 11px; color: {COLORS['accent_success']};")
            return

        bridge = get_tracker_bridge()
        loc = bridge.get_location()

        if loc != "PickUp":
            self._load_status_lbl.setText(f"Waiting for PickUp screen... (current: {loc})")
            self._load_status_lbl.setStyleSheet(
                f"font-size: 11px; color: {COLORS['text_muted']};")
            return

        result = bridge.load_players(self._team1, self._team2)
        if result["success"]:
            self._load_success = True
            self._load_status_lbl.setText(
                f"Loaded {result['loaded_count']} players into 2K13.")
            self._load_status_lbl.setStyleSheet(
                f"font-size: 11px; color: {COLORS['accent_success']};")
            log.info("Pre-game auto-load successful")
        else:
            self._load_status_lbl.setText(f"Load failed: {result['error']}")
            self._load_status_lbl.setStyleSheet(
                f"font-size: 11px; color: {COLORS['accent_danger']};")

    # ── Tracker signal handlers ───────────────────────────────────────────────

    def _on_location_changed(self, location):
        if self._phase == "pre_game" and location == "InGame":
            self._set_phase("playing")

    def _on_game_status_changed(self, status):
        if self._phase == "pre_game" and status == "Running":
            self._set_phase("playing")

    def _on_live_stats(self, stats):
        if self._phase not in ("playing",):
            return
        self._last_stats = stats
        self._update_box_score(stats)

    def _on_game_won(self, stats):
        self._last_stats = stats
        self._update_box_score(stats)
        self._set_phase("post_game")
        self._auto_save_stats(stats)
        self._build_postgame_insights(stats)

    def _simulate_postgame(self):
        """Generate realistic blacktop stats and jump to post-game (dev/preview only)."""
        import random

        # Blacktop: to 21, win by 2.  25% chance of a deuce game.
        deuce       = random.random() < 0.25
        winner_side = random.randint(1, 2)
        if deuce:
            winner_target = random.choice([22, 24])
            loser_target  = winner_target - 2
        else:
            winner_target = 21
            loser_target  = random.randint(4, 19)

        t1_target = winner_target if winner_side == 1 else loser_target
        t2_target = winner_target if winner_side == 2 else loser_target

        slot_stats = {}

        def _fill(team, base_slot, target_pts):
            n = len(team)
            raw = []
            for p in team:
                fg = random.randint(0, 4)
                th = random.randint(0, 2)
                raw.append({
                    "player": p,
                    "fg_made": fg, "fg_att": fg + random.randint(0, 3),
                    "th_made": th, "th_att": th + random.randint(0, 2),
                    "rp": fg + th * 2,
                })
            total_raw = sum(x["rp"] for x in raw) or 1
            # Scale to target, distribute remainder by highest fraction first
            scaled  = [x["rp"] / total_raw * target_pts for x in raw]
            pts_int = [int(s) for s in scaled]
            diff    = target_pts - sum(pts_int)
            order   = sorted(range(n), key=lambda i: scaled[i] - pts_int[i], reverse=True)
            for i in range(diff):
                pts_int[order[i]] += 1

            for i, (x, pts) in enumerate(zip(raw, pts_int)):
                slot_stats[base_slot + i] = {
                    "IsActive": 1,
                    "SpriteID": x["player"]["SpriteID"],
                    "Points": max(0, pts),
                    "AssistCount": random.randint(0, 5),
                    "OffensiveRebounds": random.randint(0, 2),
                    "DefensiveRebounds": random.randint(0, 4),
                    "Steals": random.randint(0, 3),
                    "Blocks": random.randint(0, 2),
                    "Turnovers": random.randint(0, 4),
                    "Fouls": random.randint(0, 3),
                    "InsidesMade": x["fg_made"],
                    "InsidesAttempted": x["fg_att"],
                    "ThreesMade": x["th_made"],
                    "ThreesAttempted": x["th_att"],
                    "BallHolding_InPlay": round(random.uniform(4.0, 75.0), 1)
                        if random.random() > 0.1 else None,
                    "BallHolding_OutOfPlay": round(random.uniform(1.0, 15.0), 1),
                    "Dunks": min(random.randint(0, 2), x["fg_made"]),
                    "Layups": 0,
                }

        _fill(self._team1, 0, t1_target)
        _fill(self._team2, 5, t2_target)

        ballerz_score = t1_target
        ringers_score = t2_target

        fake_stats = {
            "GameStats": {
                "BallerzScore": ballerz_score,
                "RingersScore": ringers_score,
                "GameMode": len(self._team1),
                "LoadedRoster": "Simulated.ROS",
            },
            "SlotStats": slot_stats,
        }

        self._last_stats = fake_stats
        self._update_box_score(fake_stats)
        self._set_phase("post_game")
        self._save_status_lbl.setText("[ SIMULATION — stats not saved ]")
        self._save_status_lbl.setStyleSheet(
            f"font-size: 11px; color: {COLORS['accent_warning']}; font-style: italic;")
        self._ballholding_warning_lbl.setVisible(False)
        self._build_postgame_insights(fake_stats)

    def _on_rematch(self):
        self.start_game(self._team1, self._team2, self._match_config)

    # ── Box score display ─────────────────────────────────────────────────────

    def _build_rows_for_slots(self, slot_stats, slot_range, team_id: int) -> list:
        """Build a list of stat-row dicts for the given slot range."""
        rows = []
        for slot_id in slot_range:
            slot = slot_stats.get(slot_id, {})
            if not slot or slot.get("IsActive", 0) != 1:
                continue
            sprite_id = slot.get("SpriteID", -1)

            name, arch = "Unknown", ""
            if sprite_id >= 0 and sprite_id in d.players:
                p = d.players[sprite_id]
                name = f"{p['First_Name']} {p['Last_Name']}".strip()
                arch = p["Archetype_Name"] or ""
            else:
                idx = slot_id if slot_id < 5 else slot_id - 5
                team = self._team1 if team_id == 1 else self._team2
                if idx < len(team):
                    p = team[idx]
                    name = f"{p['First_Name']} {p['Last_Name']}".strip()
                    arch = p["Archetype_Name"] or ""

            pts         = slot.get("Points", 0) or 0
            ast         = slot.get("AssistCount", 0) or 0
            orb         = slot.get("OffensiveRebounds", 0) or 0
            drb         = slot.get("DefensiveRebounds", 0) or 0
            reb         = orb + drb
            stl         = slot.get("Steals", 0) or 0
            blk         = slot.get("Blocks", 0) or 0
            tov         = slot.get("Turnovers", 0) or 0
            fouls       = slot.get("Fouls", 0) or 0
            threes_made = slot.get("ThreesMade", 0) or 0
            threes_att  = slot.get("ThreesAttempted", 0) or 0
            fg_made     = slot.get("InsidesMade", 0) or 0
            fg_att      = slot.get("InsidesAttempted", 0) or 0
            bh_raw      = slot.get("BallHolding_InPlay")
            bh          = round(bh_raw, 1) if bh_raw is not None else None

            total_fg  = fg_made + threes_made
            total_fga = fg_att + threes_att
            gmsc = (pts + 0.2 * total_fg - 0.35 * total_fga
                    + 0.35 * orb + 0.15 * drb
                    + 0.5 * stl + 0.35 * ast + 0.35 * blk
                    - 0.2 * fouls - 0.5 * tov)

            rows.append({
                "sprite_id": sprite_id, "name": name, "arch": arch, "team": team_id,
                "pts": pts, "ast": ast, "reb": reb, "stl": stl, "blk": blk,
                "tov": tov, "fg_made": fg_made, "fg_att": fg_att,
                "threes_made": threes_made, "threes_att": threes_att,
                "bh": bh, "gmsc": gmsc, "orb": orb, "drb": drb, "fouls": fouls,
            })
        return rows

    def _populate_team_table(self, table, team):
        """Fill table with player names and zeroed stats (pre-game)."""
        table.setSortingEnabled(False)
        table.setRowCount(len(team))
        for i, player in enumerate(team):
            first = player["First_Name"] or ""
            last  = player["Last_Name"] or ""
            name  = f"{first} {last}".strip() or "Unknown"

            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.UserRole, player["SpriteID"])
            table.setItem(i, 0, name_item)

            arch = player["Archetype_Name"]
            arch_item = QTableWidgetItem(arch[:3].upper() if arch else "?")
            arch_item.setTextAlignment(Qt.AlignCenter)
            arch_style = get_archetype_style(arch)
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            table.setItem(i, 1, arch_item)

            for j in range(2, 8):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, 0)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, item)

            fg_item = QTableWidgetItem("0/0")
            fg_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 8, fg_item)

            threept_item = QTableWidgetItem("0/0")
            threept_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 9, threept_item)

            th_item = QTableWidgetItem("—")
            th_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 10, th_item)

    def _update_box_score(self, stats):
        """Update tables and score from a ripped stats dict."""
        game_stats = stats.get("GameStats", {})
        slot_stats  = stats.get("SlotStats", {})

        self._ballerz_score.setText(str(game_stats.get("BallerzScore", 0)))
        self._ringers_score.setText(str(game_stats.get("RingersScore", 0)))

        game_mode = game_stats.get("GameMode", len(self._team1))
        t1_rows = self._build_rows_for_slots(slot_stats, range(0, game_mode), 1)
        t2_rows = self._build_rows_for_slots(slot_stats, range(5, 5 + game_mode), 2)

        self._render_team_table(self._ballerz_table, t1_rows)
        self._render_team_table(self._ringers_table, t2_rows)

    def _render_team_table(self, table, rows: list):
        """Render a team's box score table from pre-built row dicts."""
        rows_sorted = sorted(rows, key=lambda r: r["pts"], reverse=True)
        table.setSortingEnabled(False)
        table.setRowCount(len(rows_sorted))

        for i, r in enumerate(rows_sorted):
            name_item = QTableWidgetItem(r["name"])
            name_item.setData(Qt.UserRole, r["sprite_id"])
            table.setItem(i, 0, name_item)

            arch_item = QTableWidgetItem(r["arch"][:3].upper() if r["arch"] else "?")
            arch_item.setTextAlignment(Qt.AlignCenter)
            arch_style = get_archetype_style(r["arch"])
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            table.setItem(i, 1, arch_item)

            for j, val in enumerate([r["pts"], r["ast"], r["reb"], r["stl"], r["blk"], r["tov"]]):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, val)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j + 2, item)

            fg_item = QTableWidgetItem(f"{r['fg_made']}/{r['fg_att']}")
            fg_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 8, fg_item)

            threept_item = QTableWidgetItem(f"{r['threes_made']}/{r['threes_att']}")
            threept_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 9, threept_item)

            bh = r["bh"]
            th_item = QTableWidgetItem(f"{bh:.1f}s" if bh is not None else "—")
            th_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 10, th_item)

    # ── Post-game insights ────────────────────────────────────────────────────

    def _build_postgame_insights(self, stats):
        """Populate stat-leader highlights, tidbits, and MVP selector."""
        game_stats = stats.get("GameStats", {})
        slot_stats  = stats.get("SlotStats", {})
        game_mode   = game_stats.get("GameMode", len(self._team1))

        t1_rows = self._build_rows_for_slots(slot_stats, range(0, game_mode), 1)
        t2_rows = self._build_rows_for_slots(slot_stats, range(5, 5 + game_mode), 2)
        all_rows = t1_rows + t2_rows
        self._last_all_rows = all_rows

        records = None
        engine  = None
        try:
            from spritopia.gui.stats.stats_engine import StatsEngine
            engine  = StatsEngine(d.stats.get("Raw", {}), d.players)
            records = engine.get_single_game_records()
        except Exception:
            pass

        self._highlight_stat_leaders(all_rows, records)
        self._populate_tidbits(all_rows, game_stats, engine)
        self._populate_mvp_chips(all_rows)
        self._postgame_insight_panel.setVisible(True)

        # Winner announcement banner
        bs = game_stats.get("BallerzScore", 0)
        rs = game_stats.get("RingersScore", 0)
        if bs > rs:
            self._banner.setText("BALLERZ WIN")
            self._banner.setStyleSheet(
                f"font-size: 24px; font-weight: bold; color: {_TEAM_COLORS[1]}; "
                f"letter-spacing: 3px; background-color: #040e1c; "
                f"border-bottom: 2px solid {_TEAM_COLORS[1]};")
        elif rs > bs:
            self._banner.setText("RINGERS WIN")
            self._banner.setStyleSheet(
                f"font-size: 24px; font-weight: bold; color: {_TEAM_COLORS[2]}; "
                f"letter-spacing: 3px; background-color: #1c0404; "
                f"border-bottom: 2px solid {_TEAM_COLORS[2]};")
        else:
            self._banner.setText("TIE GAME")
            self._banner.setStyleSheet(self._banner_style("Post-Game"))

    def _highlight_stat_leaders(self, all_rows: list, records=None):
        """Gold-highlight the per-stat leader cell in both box score tables."""
        if not all_rows:
            return

        # (col_index, row_key, record_key)
        stat_defs = [
            (2, "pts", "points"),
            (3, "ast", "assists"),
            (4, "reb", "rebounds"),
            (5, "stl", "steals"),
            (6, "blk", "blocks"),
        ]

        # Build {col: (max_val, {sprite_ids})}
        leaders = {}
        for col, key, _ in stat_defs:
            max_val = max(r[key] for r in all_rows)
            sids    = {r["sprite_id"] for r in all_rows if r[key] == max_val} if max_val > 0 else set()
            leaders[col] = (max_val, sids)

        # BH column (10)
        bh_rows = [r for r in all_rows if r["bh"] is not None]
        if bh_rows:
            max_bh   = max(r["bh"] for r in bh_rows)
            bh_sids  = {r["sprite_id"] for r in bh_rows if r["bh"] == max_bh} if max_bh > 0 else set()
        else:
            max_bh, bh_sids = 0, set()
        leaders[10] = (max_bh, bh_sids)

        # All-time record lookup: col → (record_val, record_sprite_id)
        rec_check = {}
        if records:
            for col, key, rec_key in stat_defs:
                rec = records.get(rec_key)
                if rec and rec["value"] > 0:
                    rec_check[col] = (rec["value"], rec["sprite_id"])

        for table in (self._ballerz_table, self._ringers_table):
            for i in range(table.rowCount()):
                name_item = table.item(i, 0)
                if not name_item:
                    continue
                sid = name_item.data(Qt.UserRole)
                if sid is None:
                    continue

                for col in (2, 3, 4, 5, 6, 10):
                    item = table.item(i, col)
                    if not item:
                        continue
                    max_val, leader_sids = leaders.get(col, (0, set()))
                    if max_val > 0 and sid in leader_sids:
                        is_record = False
                        if col in rec_check:
                            rec_val, rec_sid = rec_check[col]
                            is_record = (rec_sid == sid and rec_val == max_val)

                        item.setBackground(_RECORD_BG if is_record else _LEADER_BG)
                        item.setForeground(_RECORD_FG if is_record else _LEADER_FG)
                        if is_record:
                            f = item.font()
                            f.setBold(True)
                            item.setFont(f)

    def _populate_tidbits(self, all_rows: list, game_stats: dict, engine=None):
        """Build post-game tidbits for a blacktop game (to-21, win-by-2)."""
        pool = []

        bs = game_stats.get("BallerzScore", 0)
        rs = game_stats.get("RingersScore", 0)
        margin       = abs(bs - rs)
        winner_team  = 1 if bs > rs else (2 if rs > bs else 0)
        winner_name  = "Ballerz" if winner_team == 1 else ("Ringers" if winner_team == 2 else None)
        loser_name   = "Ringers" if winner_team == 1 else ("Ballerz" if winner_team == 2 else None)
        winner_score = bs if winner_team == 1 else rs
        loser_score  = rs if winner_team == 1 else bs

        t1 = [r for r in all_rows if r["team"] == 1]
        t2 = [r for r in all_rows if r["team"] == 2]

        def _last(r):
            return r["name"].split()[-1] if r["name"] else "?"

        # ── SCORE CONTEXT ────────────────────────────────────────────────────────

        if winner_team:
            if winner_score > 21:
                pool.append((0, "epic",
                    f"Went to deuce! {winner_name} finally closed it out {winner_score}-{loser_score}"))
            else:
                pool.append((2, "note", f"{winner_name} clinched it clean at 21"))

            if loser_score == 0:
                pool.append((0, "epic", f"Perfect shutout — {loser_name} never scored"))
            elif loser_score <= 5:
                pool.append((0, "note", f"Dominant — {loser_name} held to just {loser_score}"))
            elif loser_score <= 10:
                pool.append((1, "note",
                    f"{winner_name} handled business — {loser_name} only reached {loser_score}"))
            elif loser_score >= 19:
                pool.append((1, "hot",
                    f"{loser_name} put up {loser_score} and still lost — what a game"))
            elif loser_score >= 17:
                pool.append((2, "note",
                    f"{loser_name} made a real run of it, scoring {loser_score}"))

        if margin >= 12 and winner_name:
            pool.append((1, "note", f"A {margin}-point blowout — {winner_name} never let up"))
        elif margin >= 7 and winner_name:
            pool.append((2, "note", f"Comfortable {margin}-point margin for {winner_name}"))

        # Turnovers
        combined_tos = sum(r["tov"] for r in all_rows)
        if combined_tos == 0:
            pool.append((1, "star", "Zero combined turnovers — a pristine game"))
        elif combined_tos <= 2:
            pool.append((2, "star", f"Only {combined_tos} turnover(s) all game — clean"))
        elif combined_tos >= 16:
            pool.append((2, "fun",
                f"{combined_tos} combined turnovers — ball was everywhere tonight"))

        # Fouls
        combined_fouls = sum(r["fouls"] for r in all_rows)
        if combined_fouls == 0:
            pool.append((2, "star", "Nobody fouled all game — pure basketball"))
        elif combined_fouls <= 2:
            pool.append((3, "note", f"Just {combined_fouls} foul(s) — remarkably clean contest"))

        # Three-point context
        total_3pa   = sum(r["threes_att"] for r in all_rows)
        total_fga_g = sum(r["fg_att"] + r["threes_att"] for r in all_rows)
        if total_3pa == 0 and total_fga_g >= 10:
            pool.append((2, "fun", "Nobody stepped outside the arc — strictly inside work"))
        elif total_fga_g > 0 and total_3pa / total_fga_g >= 0.65:
            pool.append((2, "note",
                f"Perimeter-heavy game — {total_3pa} of {total_fga_g} shots from deep"))

        # Pace feel
        if total_fga_g <= 20:
            pool.append((3, "note", f"Quiet game — only {total_fga_g} combined shot attempts"))
        elif total_fga_g >= 50:
            pool.append((3, "note", f"Shoot-out — {total_fga_g} combined shot attempts tonight"))

        # 3PT decided outcome
        if winner_team:
            wr = t1 if winner_team == 1 else t2
            win_3pts = sum(r["threes_made"] for r in wr) * 2
            if win_3pts > 0 and win_3pts >= margin:
                pool.append((2, "note",
                    f"Three-point shooting was the difference for {winner_name}"))

        # Team rebounding edge
        t1_reb = sum(r["reb"] for r in t1)
        t2_reb = sum(r["reb"] for r in t2)
        reb_edge = abs(t1_reb - t2_reb)
        if reb_edge >= 8:
            reb_winner = "Ballerz" if t1_reb > t2_reb else "Ringers"
            pool.append((2, "star",
                f"{reb_winner} dominated the glass: {max(t1_reb, t2_reb)} vs {min(t1_reb, t2_reb)} boards"))
        elif reb_edge >= 4:
            reb_winner = "Ballerz" if t1_reb > t2_reb else "Ringers"
            pool.append((3, "note",
                f"{reb_winner} had the rebounding edge: {max(t1_reb, t2_reb)} vs {min(t1_reb, t2_reb)}"))

        # Squeaker / close finish
        if margin <= 2 and winner_name:
            pool.append((0, "epic",
                f"{winner_name} survived a squeaker — won by just {margin}"))
        elif margin == 3 and winner_name:
            pool.append((1, "note", f"Tight one — {winner_name} edged it out by 3"))

        # Turnover battle (team level)
        t1_to_tm = sum(r["tov"] for r in t1)
        t2_to_tm = sum(r["tov"] for r in t2)
        to_gap = abs(t1_to_tm - t2_to_tm)
        if to_gap >= 4:
            sloppy_tm = "Ballerz" if t1_to_tm > t2_to_tm else "Ringers"
            sl_n = max(t1_to_tm, t2_to_tm)
            cl_n = min(t1_to_tm, t2_to_tm)
            pool.append((2, "fun",
                f"{sloppy_tm} gave it away — {sl_n} TOs vs {cl_n} for their opponents"))
        elif to_gap >= 2 and max(t1_to_tm, t2_to_tm) >= 5:
            sloppy_tm = "Ballerz" if t1_to_tm > t2_to_tm else "Ringers"
            pool.append((3, "fun",
                f"{sloppy_tm} had the turnover edge going the wrong way"))

        # Defensive grind (low combined score)
        if bs + rs <= 18 and winner_name:
            pool.append((1, "note",
                f"Defensive grind — just {bs+rs} combined points all game"))

        # Team passing
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            t_ast_p = sum(r["ast"] for r in tr)
            t_fg_p  = sum(r["fg_made"] + r["threes_made"] for r in tr)
            if t_fg_p >= 4 and t_ast_p / t_fg_p >= 0.75:
                pool.append((2, "star",
                    f"{tname} moved the ball — {t_ast_p} assists on {t_fg_p} makes"))

        # Solo scorer on losing team
        if winner_team and loser_name:
            loser_rows_p = t2 if winner_team == 1 else t1
            loser_scorers = [r for r in loser_rows_p if r["pts"] > 0]
            if len(loser_scorers) == 1 and loser_rows_p:
                pool.append((1, "fun",
                    f"{_last(loser_scorers[0])} was the only {loser_name} player to score"))

        # Shooting zone exclusivity
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            t_in = sum(r["fg_made"] for r in tr)
            t_3  = sum(r["threes_made"] for r in tr)
            if t_in == 0 and t_3 > 0:
                pool.append((2, "fun", f"{tname} scored exclusively from the perimeter"))
            if t_3 == 0 and t_in > 0:
                pool.append((3, "note", f"{tname} went exclusively inside — not a single three"))

        # Balanced attack / scoreless
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            if tr and all(r["pts"] > 0 for r in tr):
                pool.append((2, "star", f"Balanced attack — every {tname} player got on the board"))
            scoreless = sum(1 for r in tr if r["pts"] == 0)
            if scoreless >= 2:
                pool.append((2, "note", f"{scoreless} {tname} players went scoreless tonight"))

        # Top scorer duel
        if t1 and t2:
            t1_top = max(t1, key=lambda r: r["pts"])
            t2_top = max(t2, key=lambda r: r["pts"])
            if t1_top["pts"] >= 6 and t2_top["pts"] >= 6:
                pool.append((2, "note",
                    f"Scoring duel: {_last(t1_top)} ({t1_top['pts']}) vs {_last(t2_top)} ({t2_top['pts']})"))

        # Team FG%
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            t_total_m = sum(r["fg_made"] + r["threes_made"] for r in tr)
            t_total_a = sum(r["fg_att"] + r["threes_att"] for r in tr)
            if t_total_a >= 8:
                t_pct = t_total_m / t_total_a
                if t_pct >= 0.70:
                    pool.append((1, "hot", f"{tname} were on fire — {round(t_pct*100)}% from the floor"))
                elif t_pct <= 0.30:
                    pool.append((2, "fun", f"{tname} went cold — just {round(t_pct*100)}% shooting"))

        # Team with zero defensive stocks
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            team_stks = sum(r["stl"] + r["blk"] for r in tr)
            if team_stks == 0 and len(tr) >= 3:
                pool.append((2, "fun",
                    f"{tname} had zero defensive stocks — no blocks, no steals all game"))

        # Lone wolf scorer
        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            if len(tr) >= 3:
                ts_score = bs if tname == "Ballerz" else rs
                if ts_score >= 8:
                    top = max(tr, key=lambda r: r["pts"])
                    rest_pts = sum(r["pts"] for r in tr if r["sprite_id"] != top["sprite_id"])
                    if top["pts"] / ts_score >= 0.80 and rest_pts <= 3:
                        pool.append((1, "fun",
                            f"Only {_last(top)} showed up for {tname} — "
                            f"everyone else combined for {rest_pts} pts"))

        # Loser's top scorer outscored the winner's top scorer
        if winner_team and t1 and t2:
            loser_rows  = t2 if winner_team == 1 else t1
            winner_rows = t1 if winner_team == 1 else t2
            loser_top  = max(loser_rows,  key=lambda r: r["pts"])
            winner_top = max(winner_rows, key=lambda r: r["pts"])
            if loser_top["pts"] > winner_top["pts"] and loser_top["pts"] >= 8:
                pool.append((2, "note",
                    f"{_last(loser_top)} outscored everyone on the court but {loser_name} still lost"))

        # ── INDIVIDUAL ───────────────────────────────────────────────────────────

        for r in all_rows:
            nm        = _last(r)
            ts        = bs if r["team"] == 1 else rs
            tname     = "Ballerz" if r["team"] == 1 else "Ringers"
            stocks    = r["stl"] + r["blk"]
            fga_total = r["fg_att"] + r["threes_att"]

            if r["pts"] >= 15:
                pool.append((0, "hot", f"{nm} dropped a bag — {r['pts']} of {tname}'s points"))
            elif r["pts"] >= 12:
                pool.append((1, "hot", f"{nm} had a big night: {r['pts']} points"))
            elif r["pts"] >= 9:
                pool.append((2, "note", f"{nm} led {tname} with {r['pts']} pts"))

            if ts >= 8 and r["pts"] > 0:
                pct = r["pts"] / ts
                if pct >= 0.70:
                    pool.append((1, "star", f"{nm} shouldered {round(pct*100)}% of {tname}'s offense"))
                elif pct >= 0.55 and r["pts"] >= 8:
                    pool.append((2, "note", f"{nm} carried the load: {r['pts']} of {ts} {tname} points"))

            if r["pts"] == 0 and winner_team == r["team"]:
                pool.append((2, "fun", f"{tname} got the W without a point from {nm}"))

            if r["pts"] == 0 and fga_total >= 2:
                pool.append((2, "fun", f"{nm} couldn't find the net: 0/{fga_total} from the floor"))
            elif r["pts"] == 0 and fga_total == 0:
                pool.append((3, "note", f"{nm} never got a shot off tonight"))

            if r["pts"] >= 5 and r["reb"] >= 5:
                pool.append((1, "star", f"Double from {nm}: {r['pts']} pts / {r['reb']} boards"))
            if r["pts"] >= 5 and r["ast"] >= 5:
                pool.append((1, "star",
                    f"Scoring-playmaking double for {nm}: {r['pts']} pts / {r['ast']} dimes"))

            if r["fg_att"] >= 2 and r["fg_made"] == r["fg_att"]:
                pool.append((1, "hot", f"{nm} was perfect inside: {r['fg_made']}/{r['fg_att']}"))
            elif r["fg_att"] >= 4 and (r["fg_made"] / r["fg_att"]) < 0.25:
                pool.append((2, "fun", f"{nm} went cold inside — {r['fg_made']}/{r['fg_att']}"))

            if r["threes_att"] >= 2 and r["threes_made"] == r["threes_att"]:
                pool.append((1, "hot",
                    f"{nm} was lights-out from deep: {r['threes_made']}/{r['threes_att']}"))

            if r["threes_made"] >= 6:
                pool.append((1, "hot", f"{nm} rained threes — {r['threes_made']} from outside"))
            elif r["threes_made"] >= 5:
                pool.append((2, "note", f"{nm} hit {r['threes_made']} from deep tonight"))

            if r["threes_att"] == 0 and r["pts"] >= 5:
                pool.append((3, "note",
                    f"{nm} never stepped outside — {r['pts']} pts purely in the paint"))
            if r["fg_made"] == 0 and r["threes_made"] >= 2:
                pool.append((2, "fun",
                    f"{nm}'s entire {r['pts']}-pt night came from outside the arc"))

            # ── Shooting failures ──────────────────────────────────────────────
            if r["threes_att"] >= 3 and r["threes_made"] == 0:
                pool.append((1, "fun",
                    f"{nm} went 0/{r['threes_att']} from deep — put those away"))
            if r["fg_att"] >= 5 and r["fg_made"] == 0:
                pool.append((1, "fun",
                    f"{nm} bricked all {r['fg_att']} shots inside — couldn't finish at the rim"))
            total_makes = r["fg_made"] + r["threes_made"]
            if fga_total >= 6 and total_makes / fga_total < 0.20:
                pool.append((1, "fun",
                    f"{nm} was in a complete shooting slump: {total_makes}/{fga_total} from the floor"))

            if r["ast"] >= 6:
                pool.append((1, "star", f"{nm} was running the show: {r['ast']} assists"))
            elif r["ast"] >= 4:
                pool.append((2, "star", f"{nm} was the playmaker tonight: {r['ast']} dimes"))
            elif r["ast"] >= 3:
                pool.append((3, "note", f"{nm} set up teammates nicely: {r['ast']} assists"))

            if r["ast"] > r["pts"] and r["ast"] >= 3:
                pool.append((2, "star",
                    f"{nm} had more assists ({r['ast']}) than points ({r['pts']}) tonight"))

            if r["tov"] == 0 and r["ast"] >= 3:
                pool.append((1, "star",
                    f"{nm} dished {r['ast']} dimes without a single turnover"))

            if r["tov"] >= 5:
                pool.append((1, "fun", f"{nm} couldn't hold onto it — {r['tov']} turnovers"))
            elif r["tov"] >= 4:
                pool.append((2, "note", f"{nm} was sloppy: {r['tov']} TOs tonight"))

            if r["tov"] > 0 and r["ast"] >= 2 and r["ast"] / r["tov"] >= 3:
                pool.append((3, "note",
                    f"{nm}: {r['ast']} ast / {r['tov']} TO — elite ratio"))

            if r["tov"] >= r["pts"] and r["tov"] >= 3:
                pool.append((1, "fun",
                    f"{nm} had more turnovers ({r['tov']}) than points ({r['pts']}) — rough night"))
            if r["tov"] >= 3 and r["ast"] == 0:
                pool.append((2, "fun",
                    f"{nm} gave it away {r['tov']} times and didn't set up a single basket"))

            if stocks >= 5:
                pool.append((0, "record",
                    f"{nm} terrorized both ends: {r['stl']} stl + {r['blk']} blk"))
            elif stocks >= 4:
                pool.append((3, "note", f"{nm} locked in: {r['stl']} stl + {r['blk']} blk"))
            elif stocks >= 3:
                pool.append((4, "note", f"{nm} was active defensively: {stocks} stocks"))

            if r["blk"] >= 4:
                pool.append((0, "record", f"{nm} was swatting everything — {r['blk']} rejections"))
            elif r["blk"] >= 3:
                pool.append((2, "note", f"{nm} denied the rim {r['blk']} times tonight"))
            if r["stl"] >= 5:
                pool.append((1, "hot", f"{nm} was all hands — {r['stl']} steals"))
            elif r["stl"] >= 3:
                pool.append((3, "note", f"{nm} swiped the ball {r['stl']} times"))

            if r["fouls"] >= 4:
                pool.append((2, "note", f"{nm} in serious foul trouble: {r['fouls']} fouls"))

            if r["fouls"] == 0 and r["tov"] == 0 and r["pts"] >= 5:
                pool.append((2, "star",
                    f"Spotless night for {nm}: {r['pts']} pts, 0 TOs, 0 fouls"))

            if r["pts"] == 0 and r["ast"] == 0 and r["reb"] == 0 and stocks == 0:
                pool.append((1, "fun",
                    f"{nm} was a ghost tonight — nothing to show on the stat sheet"))
            if r["fouls"] >= 3 and r["pts"] == 0 and stocks == 0:
                pool.append((2, "fun",
                    f"{nm} racked up {r['fouls']} fouls without contributing a single point or stock"))
            if r["gmsc"] < 0:
                pool.append((1, "fun",
                    f"{nm} finished with a negative Game Score — more harm than good"))

            if r["reb"] >= 7:
                pool.append((1, "star",
                    f"{nm} dominated the glass: {r['reb']} boards ({r['orb']} off, {r['drb']} def)"))
            elif r["reb"] >= 5:
                pool.append((2, "star", f"{nm} owned the boards: {r['reb']} rebounds"))
            elif r["reb"] >= 3 and r["orb"] >= 2:
                pool.append((3, "note",
                    f"{nm} relentless on the offensive glass: {r['orb']} OREB"))

            impact = r["pts"] + r["reb"] + r["ast"] + stocks
            if impact >= 18:
                pool.append((1, "star",
                    f"Complete game from {nm}: {r['pts']}/{r['reb']}/{r['ast']} + {stocks} stocks"))
            elif impact >= 12 and r["pts"] >= 4:
                pool.append((2, "star",
                    f"{nm} all over the box score: {r['pts']}pts/{r['reb']}reb/{r['ast']}ast"))

            non_score = r["reb"] + r["ast"] + stocks
            if r["pts"] <= 2 and non_score >= 7:
                pool.append((2, "note",
                    f"{nm} barely scored but contributed: {r['reb']} reb / {r['ast']} ast / {stocks} stocks"))

            if r["bh"] is not None:
                if r["bh"] >= 90:
                    pool.append((1, "note",
                        f"{nm} held the rock for {r['bh']:.1f}s — ran the entire offense"))
                elif r["bh"] >= 55:
                    pool.append((2, "note", f"{nm}: {r['bh']:.1f}s of ball time in-play"))
                elif r["bh"] >= 45 and r["pts"] <= 2 and fga_total >= 2:
                    pool.append((2, "fun",
                        f"{nm} monopolized the ball ({r['bh']:.1f}s) and only managed {r['pts']} pts"))
                elif r["bh"] <= 4 and fga_total >= 3:
                    pool.append((3, "fun",
                        f"{nm} barely touched it ({r['bh']:.1f}s) but still got shots up"))

        # ── TEAM STARS ────────────────────────────────────────────────────────────

        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            if tr:
                star = max(tr, key=lambda r: r["gmsc"])
                pool.append((3, "star",
                    f"{tname} best: {_last(star)} — "
                    f"{star['pts']} pts / {star['reb']} reb / {star['ast']} ast"))

        # ── ALWAYS-FIRE FILLERS ───────────────────────────────────────────────────

        for tr, tname in [(t1, "Ballerz"), (t2, "Ringers")]:
            t_im = sum(r["fg_made"]     for r in tr)
            t_ia = sum(r["fg_att"]      for r in tr)
            t_3m = sum(r["threes_made"] for r in tr)
            t_3a = sum(r["threes_att"]  for r in tr)
            pct_i = f" ({round(t_im/t_ia*100)}%)" if t_ia > 0 else ""
            pct_3 = f" ({round(t_3m/t_3a*100)}%)" if t_3a > 0 else ""
            pool.append((4, "note",
                f"{tname}: {t_im}/{t_ia} inside{pct_i} · {t_3m}/{t_3a} from deep{pct_3}"))

        t1_orb = sum(r["orb"] for r in t1)
        t1_drb = sum(r["drb"] for r in t1)
        t2_orb = sum(r["orb"] for r in t2)
        t2_drb = sum(r["drb"] for r in t2)
        if t1 and t2:
            pool.append((4, "note",
                f"Boards — Ballerz {t1_orb+t1_drb} ({t1_orb} off) · "
                f"Ringers {t2_orb+t2_drb} ({t2_orb} off)"))

        total_ast  = sum(r["ast"] for r in all_rows)
        total_reb  = sum(r["reb"] for r in all_rows)
        total_stks = sum(r["stl"] + r["blk"] for r in all_rows)
        pool.append((4, "note",
            f"Combined: {total_ast} assists · {total_reb} boards · {total_stks} stocks"))

        # ── CAREER / HISTORICAL ───────────────────────────────────────────────────

        if engine:
            try:
                games      = engine.get_games()
                game_count = len(games)
                if game_count in (10, 25, 50, 75, 100, 150, 200, 300):
                    pool.append((0, "epic", f"Milestone: game #{game_count} all time!"))
                elif game_count > 0:
                    pool.append((4, "note", f"All-time game #{game_count}"))

                if game_count >= 5:
                    last5 = [g.winner for g in games[:5]]
                    for tn, tk in [("Ballerz", "Ballerz"), ("Ringers", "Ringers")]:
                        if all(w == tk for w in last5):
                            pool.append((1, "streak", f"{tn} have won 5 in a row"))
                if game_count >= 3:
                    last3 = [g.winner for g in games[:3]]
                    for tn, tk in [("Ballerz", "Ballerz"), ("Ringers", "Ringers")]:
                        if all(w == tk for w in last3):
                            pool.append((2, "streak", f"{tn} have taken 3 straight"))
            except Exception:
                pass

            ch_map = [
                ("pts", "points",   "pts"),
                ("reb", "rebounds", "reb"),
                ("ast", "assists",  "ast"),
                ("stl", "steals",   "stl"),
                ("blk", "blocks",   "blk"),
            ]
            for r in all_rows:
                sid = r["sprite_id"]
                if sid < 0:
                    continue
                nm = _last(r)
                try:
                    game_log = engine.get_player_game_log(sid, limit=200)
                    past = game_log[1:]
                    if not past:
                        pool.append((1, "star", f"Debut night for {nm} — welcome to Premier!"))
                        continue
                    if len(past) >= 2:
                        # One career-high note per player — pick the most impressive stat
                        ch_best = None
                        for key, log_key, label in ch_map:
                            val = r[key]
                            if val <= 0:
                                continue
                            past_max = max(g.get(log_key, 0) for g in past)
                            if val > past_max:
                                ratio = val / max(past_max, 0.5)
                                if ch_best is None or ratio > ch_best[0]:
                                    ch_best = (ratio, val, label)
                        if ch_best:
                            pool.append((0, "record",
                                f"Career high! {nm}: {ch_best[1]} {ch_best[2]}"))
                    gp = len(game_log)
                    if gp in (5, 10, 20, 25, 50, 100):
                        pool.append((1, "star", f"Game #{gp} for {nm}!"))
                    career = engine.get_career_stats(sid)
                    if career and career.games_played >= 3:
                        ppg = career.ppg
                        if ppg > 0:
                            diff = r["pts"] - ppg
                            if diff >= 4:
                                pool.append((1, "hot",
                                    f"{nm} went {r['pts']} pts — {diff:+.1f} above their {ppg:.1f} avg"))
                            elif diff <= -4 and r["pts"] < ppg * 0.5:
                                pool.append((2, "fun",
                                    f"{nm} went quiet — {r['pts']} pts vs {ppg:.1f} ppg avg"))
                        rpg = career.rpg
                        if rpg > 0:
                            rdiff = r["reb"] - rpg
                            if rdiff >= 4:
                                pool.append((1, "star",
                                    f"{nm} hauled in {r['reb']} boards — {rdiff:+.1f} above their {rpg:.1f} avg"))
                    if career and career.games_played >= 6:
                        if career.win_pct >= 0.80:
                            pool.append((2, "star",
                                f"{nm} is {career.wins}-{career.losses} "
                                f"({round(career.win_pct*100)}% W)"))
                        elif career.win_pct == 0.0:
                            pool.append((2, "fun",
                                f"{nm} still searching for that first W ({career.losses} losses)"))
                        if career.ppg >= 7.0:
                            pool.append((3, "note",
                                f"{nm} averaging {career.ppg:.1f} ppg on the season"))
                    # Bounce-back / step-down vs last game
                    if career and career.games_played >= 3 and len(game_log) >= 2:
                        prev_pts = game_log[1].get("points", 0)
                        if r["pts"] >= prev_pts + 8 and r["pts"] >= 8:
                            pool.append((2, "hot",
                                f"{nm} bounced back — {prev_pts} pts last game, {r['pts']} tonight"))
                        elif prev_pts >= r["pts"] + 8 and prev_pts >= 8:
                            pool.append((2, "fun",
                                f"{nm} fell off — {prev_pts} pts last time, only {r['pts']} tonight"))
                    # Career total pts milestone
                    if career and r["pts"] > 0:
                        new_tot = career.total_points
                        for ms in (50, 100, 150, 200, 300, 500):
                            if new_tot - r["pts"] < ms <= new_tot:
                                pool.append((1, "record",
                                    f"{nm} crossed {ms} career points tonight"))
                                break
                    # Career total rebounds milestone
                    if career and r["reb"] > 0:
                        new_reb = career.total_rebounds
                        for ms in (50, 100, 150, 200):
                            if new_reb - r["reb"] < ms <= new_reb:
                                pool.append((1, "star",
                                    f"{nm} crossed {ms} career rebounds tonight"))
                                break
                    # Career steals milestone
                    if career and r["stl"] > 0:
                        new_stl = career.total_steals
                        for ms in (25, 50, 75, 100):
                            if new_stl - r["stl"] < ms <= new_stl:
                                pool.append((1, "record",
                                    f"{nm} crossed {ms} career steals tonight"))
                                break
                except Exception:
                    pass

            for r in all_rows:
                sid = r["sprite_id"]
                if sid < 0:
                    continue
                nm = _last(r)
                try:
                    streak_len, streak_type = self._compute_streak(sid, engine)
                    if streak_len >= 6:
                        label = "win" if streak_type == "W" else "loss"
                        pool.append((0, "epic", f"{nm}: {streak_len}-game {label} streak"))
                    elif streak_len >= 3:
                        label = "win" if streak_type == "W" else "loss"
                        pool.append((1, "streak", f"{nm}: {streak_len}-game {label} streak"))
                except Exception:
                    pass

        # ── FINALIZE ──────────────────────────────────────────────────────────────

        import random as _rnd
        from itertools import groupby as _gb
        _KIND_ORD = {"epic": -1, "record": 0, "hot": 1, "streak": 2, "star": 3, "note": 4, "fun": 5}
        pool.sort(key=lambda x: (x[0], _KIND_ORD.get(x[1], 99)))
        final, seen = [], set()
        for _, grp in _gb(pool, key=lambda x: (x[0], x[1])):
            items = [(k, t) for _, k, t in grp]
            _rnd.shuffle(items)
            for kind, text in items:
                if text not in seen:
                    seen.add(text)
                    final.append((kind, text))

        kind_colors = {
            "epic":   "#22d3ee",   # cyan   — ultra-rare events (shutout, deuce, milestones)
            "record": "#facc15",   # yellow — career records & highs
            "hot":    "#f97316",   # orange — on-fire performances
            "streak": "#4a9eff",   # blue   — streaks & momentum
            "star":   "#10b981",   # green  — excellent stat lines
            "note":   "#94a3b8",   # gray   — neutral observations
            "fun":    "#ef4444",   # red    — critical / negative
        }

        for i, lbl in enumerate(self._tidbit_labels):
            if i < len(final):
                kind, text = final[i]
                color = kind_colors.get(kind, COLORS["text_secondary"])
                lbl.setText(text)
                lbl.setStyleSheet(f"""
                    QLabel {{
                        color: {color};
                        font-size: 11px;
                        padding: 3px 8px;
                        border-radius: 3px;
                        background-color: rgba(255, 255, 255, 6);
                        border-left: 3px solid {color};
                    }}
                """)
                lbl.setVisible(True)
            else:
                lbl.setVisible(False)

        # Overflow: show indicator if important notes didn't fit
        _OVERFLOW_KINDS = {"epic", "record", "hot", "streak"}
        overflow = [(k, t) for k, t in final[10:] if k in _OVERFLOW_KINDS]
        if overflow:
            tip_lines = []
            for k, t in overflow[:8]:
                prefix = {
                    "epic": "★",
                    "record": "★",
                    "hot": "▸",
                    "streak": "▸",
                }.get(k, "·")
                tip_lines.append(f"{prefix}  {t}")
            self._tidbit_overflow_lbl.setText(
                f"★  {len(overflow)} more notable note{"s" if len(overflow) > 1 else ""} (hover)")
            self._tidbit_overflow_lbl.setToolTip("\n".join(tip_lines))
            self._tidbit_overflow_lbl.setVisible(True)
        else:
            self._tidbit_overflow_lbl.setVisible(False)

    def _get_duo_record(self, sid_a: int, sid_b: int, games: list) -> tuple:
        """Return (shared_games, shared_wins) when sid_a and sid_b are on the same team."""
        shared = wins = 0
        for game in games:
            b = {info.get("SpriteID") for slot, info in game.player_slots.items()
                 if info.get("IsActive") and info.get("SpriteID") is not None and slot < 5}
            r = {info.get("SpriteID") for slot, info in game.player_slots.items()
                 if info.get("IsActive") and info.get("SpriteID") is not None and slot >= 5}
            if sid_a in b and sid_b in b:
                shared += 1
                if game.winner == "Ballerz":
                    wins += 1
            elif sid_a in r and sid_b in r:
                shared += 1
                if game.winner == "Ringers":
                    wins += 1
        return shared, wins

    def _build_pregame_content(self, team1: list, team2: list):
        """Load engine, decorate tables with streak badges, populate match preview notes."""
        try:
            from spritopia.gui.stats.stats_engine import StatsEngine
            engine = StatsEngine(d.stats.get("Raw", {}), d.players)
        except Exception:
            return
        self._decorate_table_streaks(self._ballerz_table, engine)
        self._decorate_table_streaks(self._ringers_table, engine)
        self._populate_pregame_notes(team1, team2, engine)

    def _decorate_table_streaks(self, table, engine):
        """Prefix player name cells with a streak badge for 3+ game win/loss streaks."""
        for i in range(table.rowCount()):
            name_item = table.item(i, 0)
            if not name_item:
                continue
            sid = name_item.data(Qt.UserRole)
            if sid is None or sid < 0:
                continue
            try:
                streak_len, streak_type = self._compute_streak(sid, engine)
                if streak_len >= 3:
                    badge = ("🔥🔥" if streak_len >= 6 else "🔥")                             if streak_type == "W" else "❄️"
                    name_item.setText(f"{badge} {name_item.text()}")
            except Exception:
                pass

    def _populate_pregame_notes(self, team1: list, team2: list, engine):
        """Generate and display match-preview notes with per-tier randomization."""
        import random as _rnd
        from itertools import groupby as _gb
        pool = []
        games = engine.get_games()
        all_players = team1 + team2

        def _last(p):
            return p["Last_Name"] or "?"

        t1_sids = {p["SpriteID"] for p in team1}
        t2_sids = {p["SpriteID"] for p in team2}
        all_sids = t1_sids | t2_sids

        # ── EXACT LINEUP ───────────────────────────────────────────────────────
        exact = 0
        for game in games:
            b = {info.get("SpriteID") for slot, info in game.player_slots.items()
                 if info.get("IsActive") and info.get("SpriteID") is not None and slot < 5}
            r = {info.get("SpriteID") for slot, info in game.player_slots.items()
                 if info.get("IsActive") and info.get("SpriteID") is not None and slot >= 5}
            if b == t1_sids and r == t2_sids:
                exact += 1
        if exact:
            pool.append((0, "record",
                f"These exact lineups have met {exact} time{'s' if exact > 1 else ''} before"))

# ── RECENT FORM ────────────────────────────────────────────────────────
        if len(games) >= 3:
            last5 = games[:5]
            n5 = len(last5)
            for tn, wk in [("Ballerz", "Ballerz"), ("Ringers", "Ringers")]:
                tw = sum(1 for g in last5 if g.winner == wk)
                if tw >= 4:
                    pool.append((1, "streak", f"{tn} have gone {tw}-{n5-tw} in their last {n5}"))
                elif tw == 0 and n5 >= 3:
                    pool.append((2, "fun", f"{tn} have dropped their last {n5} — winless run"))

        # ── INDIVIDUAL STREAKS ─────────────────────────────────────────────────
        for p in all_players:
            nm = _last(p)
            try:
                streak_len, streak_type = self._compute_streak(p["SpriteID"], engine)
                if streak_len >= 6:
                    if streak_type == "W":
                        pool.append((0, "hot",
                            f"{nm} has won {streak_len} straight — on absolute fire"))
                    else:
                        pool.append((0, "fun",
                            f"{nm} has lost {streak_len} in a row — desperate for a win"))
                elif streak_len >= 3:
                    if streak_type == "W":
                        pool.append((1, "hot", f"{nm} riding a {streak_len}-game win streak"))
                    else:
                        pool.append((1, "fun", f"{nm} on a {streak_len}-game losing skid"))
            except Exception:
                pass

        # ── DEBUTS ────────────────────────────────────────────────────────────
        debut_names = []
        for p in all_players:
            c = engine.get_career_stats(p["SpriteID"])
            if not c or c.games_played == 0:
                debut_names.append(_last(p))
                pool.append((1, "star", f"Tonight is {_last(p)}'s Premier debut"))
        if len(debut_names) >= 3:
            pool.append((1, "star", f"{len(debut_names)} players making their Premier debut tonight"))

        # ── CAREER NARRATIVES ──────────────────────────────────────────────────
        careers = [(p, engine.get_career_stats(p["SpriteID"])) for p in all_players]
        careers = [(p, c) for p, c in careers if c and c.games_played >= 1]

        for p, c in careers:
            nm = _last(p)
            if c.wins == 0 and c.games_played >= 3:
                pool.append((1, "fun",
                    f"{nm} is 0-{c.games_played} all time — still chasing win #1"))
            if c.losses == 0 and c.games_played >= 3:
                pool.append((0, "hot", f"{nm} enters tonight undefeated ({c.games_played}-0)"))
            if c.games_played >= 5 and c.win_pct >= 0.80:
                pool.append((1, "star",
                    f"{nm} wins {round(c.win_pct*100)}% of games ({c.wins}-{c.losses})"))
            if c.games_played >= 5 and c.win_pct <= 0.20:
                pool.append((2, "fun",
                    f"{nm} has won just {c.wins} of {c.games_played} games — rough track record"))

        # Top scorer / rebounder in this game
        scored = [(p, c) for p, c in careers if c.games_played >= 3 and c.ppg >= 5.0]
        if scored:
            top = max(scored, key=lambda x: x[1].ppg)
            pool.append((2, "note",
                f"{_last(top[0])} leads all players tonight at {top[1].ppg:.1f} ppg"))

        boarders = [(p, c) for p, c in careers if c.games_played >= 3 and c.rpg >= 3.0]
        if boarders:
            top = max(boarders, key=lambda x: x[1].rpg)
            pool.append((2, "star",
                f"{_last(top[0])} is the top rebounder in this game ({top[1].rpg:.1f} rpg)"))

        # Efficient shooter
        shooters = [(p, c) for p, c in careers
                    if c.games_played >= 3 and c.fg_attempted >= c.games_played * 2]
        if shooters:
            top = max(shooters, key=lambda x: x[1].efg_pct)
            if top[1].efg_pct >= 0.55:
                pool.append((2, "star",
                    f"{_last(top[0])} shoots {round(top[1].efg_pct*100)}% eFG — most efficient shooter here"))

        # Bad ball security
        for p, c in careers:
            if c.games_played >= 4 and c.tpg >= 3.5:
                pool.append((3, "fun",
                    f"{_last(p)} averages {c.tpg:.1f} TOs a game — ball security is a concern"))

        # Game milestones tonight
        for p, c in careers:
            upcoming = c.games_played + 1
            if upcoming in (5, 10, 20, 25, 50, 100):
                pool.append((1, "star", f"Tonight is game #{upcoming} for {_last(p)}"))

        # Last game hot/cold
        for p, c in careers:
            nm = _last(p)
            try:
                gl = engine.get_player_game_log(p["SpriteID"], limit=2)
                if gl and c.games_played >= 3:
                    lp = gl[0]["points"]
                    lr = gl[0]["rebounds"]
                    if lp >= c.ppg + 5 and lp >= 9:
                        pool.append((2, "hot", f"{nm} dropped {lp} pts last game — in form"))
                    elif lp == 0 and c.ppg >= 4:
                        pool.append((2, "fun",
                            f"{nm} was shut out last game — looking to bounce back"))
                    if lr >= c.rpg + 5 and lr >= 7:
                        pool.append((2, "star",
                            f"{nm} hauled in {lr} boards last game — glass menace"))
            except Exception:
                pass

        # All-time single-game record holders in this game
        try:
            sg = engine.get_single_game_records()
            for stat_key, label in [("points", "single-game scoring"),
                                     ("rebounds", "single-game rebounding"),
                                     ("steals", "single-game steals")]:
                rec = sg.get(stat_key, {})
                rsid = rec.get("sprite_id", -1)
                if rsid in all_sids and rec.get("value", 0) > 0:
                    for p in all_players:
                        if p["SpriteID"] == rsid:
                            pool.append((1, "record",
                                f"{_last(p)} holds the {label} record ({rec['value']})"))
                            break
        except Exception:
            pass


        # ── LAST GAME FLASHBACK ─────────────────────────────────────────────
        if games:
            lg0 = games[0]
            pool.append((2, "note",
                f"Last game: Ballerz {lg0.ballerz_score} – Ringers {lg0.ringers_score} ({lg0.winner} won)"))

        # ── CAREER LEADERS & NARRATIVES ───────────────────────────────
        qualified = [(p, c) for p, c in careers if c.games_played >= 4]
        if qualified:
            top_def = max(qualified, key=lambda x: x[1].spg + x[1].bpg)
            pd_, cd_ = top_def
            if cd_.spg + cd_.bpg >= 1.5:
                pool.append((2, "star",
                    f"{_last(pd_)} leads this game on defense ({cd_.spg:.1f} spg / {cd_.bpg:.1f} bpg)"))
            top_3pt = [(p, c) for p, c in qualified
                        if c.threes_attempted >= c.games_played * 2]
            if top_3pt:
                best_3 = max(top_3pt, key=lambda x: x[1].three_pt_pct)
                p3_, c3_ = best_3
                if c3_.three_pt_pct >= 0.50:
                    pool.append((2, "hot",
                        f"{_last(p3_)} is shooting {round(c3_.three_pt_pct*100)}% from three — watch the arc"))
                elif c3_.three_pt_pct <= 0.20:
                    pool.append((3, "fun",
                        f"{_last(p3_)} shoots just {round(c3_.three_pt_pct*100)}% from deep — yet keeps pulling the trigger"))

        # Approaching career pts / reb milestone
        for p, c in careers:
            nm = _last(p)
            if c.games_played >= 2:
                for ms in (50, 100, 150, 200, 300, 500):
                    if c.total_points < ms and ms - c.total_points <= 15:
                        pool.append((2, "note",
                            f"{nm} could reach career {ms} pts tonight ({c.total_points} so far)"))
                        break
                for ms in (25, 50, 100, 150, 200):
                    if c.total_rebounds < ms and ms - c.total_rebounds <= 10:
                        pool.append((2, "star",
                            f"{nm} is just {ms - c.total_rebounds} boards away from career {ms}"))
                        break

        # Back-to-back big scoring games
        for p, c in careers:
            if c.games_played < 3:
                continue
            nm = _last(p)
            try:
                gl2 = engine.get_player_game_log(p["SpriteID"], limit=2)
                if len(gl2) >= 2 and gl2[0]["points"] >= 9 and gl2[1]["points"] >= 9:
                    pool.append((2, "hot",
                        f"{nm} has scored 9+ in back-to-back games — rolling"))
            except Exception:
                pass

        # Career dunks leader in this matchup
        dunkers = [(p, c) for p, c in careers if c.games_played >= 3 and c.total_dunks >= 5]
        if dunkers:
            top_d = max(dunkers, key=lambda x: x[1].total_dunks)
            pool.append((3, "note",
                f"{_last(top_d[0])} leads this game in career dunks ({top_d[1].total_dunks} all time)"))

        # ── DUO NOTES ─────────────────────────────────────────────────────────
        if len(games) >= 3:
            for team in (team1, team2):
                for i, pa in enumerate(team):
                    for pb in team[i+1:]:
                        sa, sb = pa["SpriteID"], pb["SpriteID"]
                        shared, sw = self._get_duo_record(sa, sb, games)
                        na, nb = _last(pa), _last(pb)
                        if shared >= 4:
                            wp = sw / shared
                            if wp >= 0.80:
                                pool.append((1, "hot",
                                    f"{na} & {nb} are {sw}-{shared-sw} when they team up"))
                            elif wp <= 0.20:
                                pool.append((1, "fun",
                                    f"{na} & {nb} are {sw}-{shared-sw} together — questionable combo"))
                            elif shared >= 8 and 0.40 <= wp <= 0.60:
                                pool.append((3, "note",
                                    f"{na} & {nb} are dead even together ({sw}-{shared-sw})"))
                        elif shared == 0 and len(games) >= 4:
                            pool.append((3, "note",
                                f"First time {na} & {nb} share a lineup"))

        # ── ALWAYS-FIRE ────────────────────────────────────────────────────────
        pool.append((4, "note", f"Game #{len(games)+1} in Premier history"))

        # ── FINALIZE ──────────────────────────────────────────────────────────
        _KIND_ORD = {"epic": -1, "record": 0, "hot": 1, "streak": 2, "star": 3, "note": 4, "fun": 5}
        pool.sort(key=lambda x: (x[0], _KIND_ORD.get(x[1], 99)))
        final, seen = [], set()
        for _, grp in _gb(pool, key=lambda x: (x[0], x[1])):
            items = [(k, t) for _, k, t in grp]
            _rnd.shuffle(items)
            for kind, text in items:
                if text not in seen:
                    seen.add(text)
                    final.append((kind, text))

        kind_colors = {
            "epic":   "#22d3ee",   # cyan   — ultra-rare events (shutout, deuce, milestones)
            "record": "#facc15",   # yellow — career records & highs
            "hot":    "#f97316",   # orange — on-fire performances
            "streak": "#4a9eff",   # blue   — streaks & momentum
            "star":   "#10b981",   # green  — excellent achievements
            "note":   "#94a3b8",   # gray   — neutral observations
            "fun":    "#ef4444",   # red    — critical / negative
        }
        for i, lbl in enumerate(self._pregame_note_labels):
            if i < len(final):
                kind, text = final[i]
                color = kind_colors.get(kind, COLORS["text_secondary"])
                lbl.setText(text)
                lbl.setStyleSheet(f"""
                    QLabel {{
                        color: {color};
                        font-size: 11px;
                        padding: 3px 8px;
                        border-radius: 3px;
                        background-color: rgba(255, 255, 255, 6);
                        border-left: 3px solid {color};
                    }}
                """)
                lbl.setVisible(True)
            else:
                lbl.setVisible(False)
        self._pregame_notes_panel.setVisible(True)

    def _compute_streak(self, sprite_id: int, engine) -> tuple:
        """Return (streak_length, 'W'/'L') for the player's current streak."""
        game_log = engine.get_player_game_log(sprite_id, limit=20)
        if not game_log:
            return 0, ""
        streak_result = game_log[0]["result"]
        count = 0
        for entry in game_log:
            if entry["result"] == streak_result:
                count += 1
            else:
                break
        return count, streak_result

    @staticmethod
    def _mvp_score(r: dict) -> float:
        """Custom MVP score weighted by importance: pts > reb > stl > ast > blk, penalise TOs + misses."""
        misses = (r["fg_att"] - r["fg_made"]) + (r["threes_att"] - r["threes_made"])
        return (r["pts"] * 1.0
                + r["reb"] * 1.1
                + r["stl"] * 1.25
                + r["ast"] * 0.7
                + r["blk"] * 0.5
                - r["tov"] * 1.5
                - misses * 0.3)

    def _populate_mvp_chips(self, all_rows: list):
        """Build the MVP chip buttons (one per player, split by team row)."""
        for chip_lo in (self._mvp_t1_chips_lo, self._mvp_t2_chips_lo):
            while chip_lo.count():
                item = chip_lo.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        self._mvp_chips = {}
        self._selected_mvp = None
        self._mvp_suggestion = None

        if not all_rows:
            self._mvp_selected_lbl.setText("— select a player —")
            self._mvp_selected_lbl.setStyleSheet(
                f"font-size: 20px; font-weight: bold; color: {COLORS['text_muted']};")
            self._mvp_stats_lbl.setVisible(False)
            self._mvp_reason_lbl.setVisible(False)
            return

        sug_row = max(all_rows, key=self._mvp_score)
        suggested_sid = sug_row["sprite_id"]

        # Build reason string
        max_pts = max(r["pts"] for r in all_rows)
        max_reb = max(r["reb"] for r in all_rows)
        max_stl = max(r["stl"] for r in all_rows)
        reasons = []
        if sug_row["pts"] == max_pts and sug_row["pts"] >= 7:
            reasons.append(f"game-high {sug_row['pts']} pts")
        if sug_row["reb"] == max_reb and sug_row["reb"] >= 4:
            reasons.append(f"led rebounding ({sug_row['reb']})")
        if sug_row["stl"] == max_stl and sug_row["stl"] >= 2:
            reasons.append(f"led steals ({sug_row['stl']})")
        fga = sug_row["fg_att"] + sug_row["threes_att"]
        fgm = sug_row["fg_made"] + sug_row["threes_made"]
        if fga >= 4 and fgm / fga >= 0.65:
            reasons.append("efficient shooting")
        reason_text = "  ·  ".join(reasons[:2]) if reasons else "Best overall performance"

        parts = [f"{sug_row['pts']} pts", f"{sug_row['reb']} reb", f"{sug_row['ast']} ast"]
        if sug_row["stl"] > 0:
            parts.append(f"{sug_row['stl']} stl")
        if sug_row["blk"] > 0:
            parts.append(f"{sug_row['blk']} blk")
        parts.append(f"eMVP {self._mvp_score(sug_row):.1f}")
        stats_text = "  ·  ".join(parts)
        self._mvp_suggestion = (sug_row["name"], stats_text, reason_text)

        self._show_suggestion()

        for team_id, chip_lo in [(1, self._mvp_t1_chips_lo), (2, self._mvp_t2_chips_lo)]:
            team_rows = sorted(
                [r for r in all_rows if r["team"] == team_id],
                key=lambda r: -self._mvp_score(r)
            )
            team_color = _TEAM_COLORS[team_id]

            for r in team_rows:
                sid = r["sprite_id"]
                last = r["name"].split()[-1] if r["name"] else "?"
                is_suggested = (sid == suggested_sid)
                score = self._mvp_score(r)

                border  = "#f59e0b" if is_suggested else COLORS["border_dark"]
                weight  = "bold"    if is_suggested else "normal"

                chip_text = last
                btn = QPushButton(chip_text)
                btn.setFixedHeight(34)
                btn.setCheckable(True)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['bg_medium']};
                        color: {team_color};
                        border: 1px solid {border};
                        border-radius: 4px;
                        font-size: 12px;
                        font-weight: {weight};
                        padding: 0 12px;
                        min-width: 72px;
                    }}
                    QPushButton:hover {{
                        background-color: {COLORS['bg_light']};
                        border-color: {team_color};
                    }}
                    QPushButton:checked {{
                        background-color: #7c3aed;
                        color: white;
                        border-color: #7c3aed;
                        font-weight: bold;
                    }}
                """)
                btn.clicked.connect(
                    lambda checked, s=sid, n=r["name"], b=btn, row=r: self._on_mvp_chip_clicked(s, n, b, row)
                )
                self._mvp_chips[sid] = btn
                chip_lo.addWidget(btn)

            chip_lo.addStretch()

    def _show_suggestion(self):
        """Restore the pre-filled suggestion display (called on init and deselect)."""
        if not self._mvp_suggestion:
            return
        name, stats_text, reason_text = self._mvp_suggestion
        self._mvp_selected_lbl.setText(name)
        self._mvp_selected_lbl.setStyleSheet(
            "font-size: 20px; font-weight: normal; color: #c8900a; font-style: italic;")
        self._mvp_stats_lbl.setText(stats_text)
        self._mvp_stats_lbl.setStyleSheet(
            f"font-size: 12px; color: {COLORS['text_muted']}; padding: 2px 0 2px 0;")
        self._mvp_stats_lbl.setVisible(True)
        self._mvp_reason_lbl.setText(f"Suggested: {reason_text}")
        self._mvp_reason_lbl.setVisible(True)

    def _on_mvp_chip_clicked(self, sprite_id, name, btn, row=None):
        if not btn.isChecked():
            self._selected_mvp = None
            self._show_suggestion()
            return

        for sid, b in self._mvp_chips.items():
            if sid != sprite_id:
                b.setChecked(False)

        self._selected_mvp = sprite_id
        self._mvp_selected_lbl.setText(f"★  {name}")
        self._mvp_selected_lbl.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #f59e0b; font-style: normal;")
        self._mvp_reason_lbl.setVisible(False)
        if row:
            parts = [f"{row['pts']} pts", f"{row['reb']} reb", f"{row['ast']} ast"]
            if row["stl"] > 0:
                parts.append(f"{row['stl']} stl")
            if row["blk"] > 0:
                parts.append(f"{row['blk']} blk")
            parts.append(f"eMVP {self._mvp_score(row):.1f}")
            self._mvp_stats_lbl.setText("  ·  ".join(parts))
            self._mvp_stats_lbl.setStyleSheet(
                "font-size: 12px; color: #a3a3a3; padding: 2px 0 10px 0;")
            self._mvp_stats_lbl.setVisible(True)

    # ── Post-game: auto-save ──────────────────────────────────────────────────

    def _auto_save_stats(self, stats):
        """Automatically save ripped game stats to the DB."""
        game_stats = stats.get("GameStats", {})
        slot_stats  = stats.get("SlotStats", {})

        ballerz_score = game_stats.get("BallerzScore", 0)
        ringers_score = game_stats.get("RingersScore", 0)

        active_slots = [s for s in slot_stats.values() if s.get("IsActive") == 1]
        ballholding_missing = any(
            s.get("BallHolding_InPlay") is None for s in active_slots
        ) if active_slots else False

        if ballholding_missing:
            self._ballholding_warning_lbl.setText(
                "⚠ Ball-holding stats unavailable for this game — at least one player "
                "never touched the ball, so the iValue map could not be solved. The "
                "rest of the box score saved normally."
            )
            self._ballholding_warning_lbl.setVisible(True)
            log.warning("Ball holding incomplete for this game — saving with NULL ball-holding columns.")
        else:
            self._ballholding_warning_lbl.setVisible(False)
            self._ballholding_warning_lbl.setText("")

        class _StatsWrapper:
            def __init__(self, gs, ss):
                self.loadedRoster = gs.get("LoadedRoster", "Unknown.ROS")
                self.gameMode     = gs.get("GameMode", 0)
                self.ballerzScore = gs.get("BallerzScore", 0)
                self.ringersScore = gs.get("RingersScore", 0)
                self.slotStats    = {"slotStats": {}}
                for slot_id, info in ss.items():
                    self.slotStats["slotStats"][f"Slot{slot_id}"] = info

        try:
            wrapper = _StatsWrapper(game_stats, slot_stats)
            game_id = d.statsDB_AddRippedGame(wrapper)
            d.statsDB_UploadRaw()
            self._save_status = (
                f"Game saved successfully (ID: {game_id})  ·  "
                f"Ballerz {ballerz_score} - {ringers_score} Ringers"
            )
            self._save_status_lbl.setText(self._save_status)
            self._save_status_lbl.setStyleSheet(
                f"font-size: 11px; color: {COLORS['accent_success']};")
            log.info(f"Auto-saved game as GameID={game_id}")
        except Exception as e:
            self._save_status = f"SAVE FAILED: {e}"
            self._save_status_lbl.setText(self._save_status)
            self._save_status_lbl.setStyleSheet(
                f"font-size: 13px; font-weight: bold; color: {COLORS['accent_danger']};")
            log.exception(f"Failed to auto-save game: {e}")
