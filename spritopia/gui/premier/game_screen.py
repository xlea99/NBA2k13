"""
Game Screen — live box score display during Pre-Game, Playing, and Post-Game phases.

Phases:
  Pre-Game  — auto-loads players into 2K13 picker screen (with auto-load toggle)
  Playing   — live box score updates from tracker stat rips
  Post-Game — final results + auto-save status
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


class GameScreen(QWidget):
    """Live game screen showing box score across Pre-Game / Playing / Post-Game."""

    back_requested = Signal()  # user wants to go back to setup

    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = "idle"        # idle / pre_game / playing / post_game
        self._team1 = []            # Ballerz player dicts
        self._team2 = []            # Ringers player dicts
        self._match_config = {}
        self._auto_load = True
        self._load_success = False
        self._save_status = ""      # status text for post-game save
        self._last_stats = None     # latest ripped stats dict
        self._signals_connected = False

        # Auto-load retry timer (tries every 2s during pre-game)
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

        # Ballerz table
        ballerz_col = QVBoxLayout()
        ballerz_col.setSpacing(4)
        b_hdr = QLabel("BALLERZ")
        b_hdr.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {_TEAM_COLORS[1]}; letter-spacing: 1px;")
        ballerz_col.addWidget(b_hdr)
        self._ballerz_table = self._create_box_table()
        ballerz_col.addWidget(self._ballerz_table)
        box_lo.addLayout(ballerz_col, stretch=1)

        # Ringers table
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

        # Pre-game controls panel (auto-load checkbox + manual load button)
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
        self._manual_load_btn.setVisible(False)  # hidden when auto-load is on
        pg_lo.addWidget(self._manual_load_btn)

        self._load_status_lbl = QLabel("")
        self._load_status_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        pg_lo.addWidget(self._load_status_lbl, stretch=1)

        pg_lo.addStretch()

        self._pregame_cancel_btn = self._make_cancel_button("Cancel Game")
        self._pregame_cancel_btn.clicked.connect(self.back_requested)
        pg_lo.addWidget(self._pregame_cancel_btn)

        lo.addWidget(self._pregame_panel)

        # Playing-phase bar (just a Cancel button — no other controls during a live game)
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

        # Post-game status bar (save status)
        self._postgame_bar = QFrame()
        self._postgame_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        post_lo = QHBoxLayout(self._postgame_bar)
        post_lo.setContentsMargins(24, 8, 24, 8)

        # Stack save-status and ball-holding warning vertically in the left slot
        # so each can be styled and toggled independently of the other.
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
        for i in range(1, 9):
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
        self._save_status_lbl.setText("")
        self._ballholding_warning_lbl.setText("")
        self._ballholding_warning_lbl.setVisible(False)

        self._set_phase("pre_game")

        # Pre-populate tables with player names (stats all zero)
        self._populate_team_table(self._ballerz_table, team1)
        self._populate_team_table(self._ringers_table, team2)
        self._ballerz_score.setText("0")
        self._ringers_score.setText("0")

        # Connect bridge signals
        bridge = get_tracker_bridge()
        if not self._signals_connected:
            bridge.location_changed.connect(self._on_location_changed)
            bridge.game_status_changed.connect(self._on_game_status_changed)
            bridge.live_stats.connect(self._on_live_stats)
            bridge.game_won.connect(self._on_game_won)
            self._signals_connected = True

        # Start auto-load
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
        elif phase == "playing":
            self._banner.setText("PLAYING")
            self._banner.setStyleSheet(self._banner_style("Playing"))
            self._pregame_panel.setVisible(False)
            self._playing_panel.setVisible(True)
            self._postgame_bar.setVisible(False)
            self._auto_load_timer.stop()
        elif phase == "post_game":
            self._banner.setText("POST-GAME")
            self._banner.setStyleSheet(self._banner_style("Post-Game"))
            self._pregame_panel.setVisible(False)
            self._playing_panel.setVisible(False)
            self._postgame_bar.setVisible(True)

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
            # Transition: picker → in-game = game has started
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

    # ── Box score display ─────────────────────────────────────────────────────

    def _populate_team_table(self, table, team):
        """Fill table with player names and zeroed stats (pre-game)."""
        table.setSortingEnabled(False)
        table.setRowCount(len(team))
        for i, player in enumerate(team):
            first = player["First_Name"] or ""
            last = player["Last_Name"] or ""
            name = f"{first} {last}".strip() or "Unknown"

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

    def _update_box_score(self, stats):
        """Update tables and score from a ripped stats dict."""
        game_stats = stats.get("GameStats", {})
        slot_stats = stats.get("SlotStats", {})

        ballerz_pts = game_stats.get("BallerzScore", 0)
        ringers_pts = game_stats.get("RingersScore", 0)
        self._ballerz_score.setText(str(ballerz_pts))
        self._ringers_score.setText(str(ringers_pts))

        game_mode = game_stats.get("GameMode", len(self._team1))

        # Update Ballerz table (slots 0..N-1)
        self._update_team_table(self._ballerz_table, self._team1, slot_stats,
                                range(0, game_mode))
        # Update Ringers table (slots 5..5+N-1)
        self._update_team_table(self._ringers_table, self._team2, slot_stats,
                                range(5, 5 + game_mode))

    def _update_team_table(self, table, team, slot_stats, slot_range):
        """Refresh a team's table with live slot stats."""
        # Build per-player stat rows from slots
        rows = []
        for slot_id in slot_range:
            slot = slot_stats.get(slot_id, {})
            if not slot or slot.get("IsActive", 0) != 1:
                continue
            sprite_id = slot.get("SpriteID", -1)

            # Find player name from team list or d.players
            name = "Unknown"
            arch = ""
            if sprite_id >= 0 and sprite_id in d.players:
                p = d.players[sprite_id]
                name = f"{p['First_Name']} {p['Last_Name']}".strip()
                arch = p["Archetype_Name"] or ""
            else:
                # Fallback: match by position in team list
                idx = slot_id if slot_id < 5 else slot_id - 5
                if idx < len(team):
                    p = team[idx]
                    name = f"{p['First_Name']} {p['Last_Name']}".strip()
                    arch = p["Archetype_Name"] or ""

            pts = slot.get("Points", 0) or 0
            ast = slot.get("AssistCount", 0) or 0
            reb = (slot.get("OffensiveRebounds", 0) or 0) + (slot.get("DefensiveRebounds", 0) or 0)
            stl = slot.get("Steals", 0) or 0
            blk = slot.get("Blocks", 0) or 0
            tov = slot.get("Turnovers", 0) or 0
            fg_made = (slot.get("InsidesMade", 0) or 0) + (slot.get("ThreesMade", 0) or 0)
            fg_att = (slot.get("InsidesAttempted", 0) or 0) + (slot.get("ThreesAttempted", 0) or 0)

            rows.append({
                "sprite_id": sprite_id, "name": name, "arch": arch,
                "pts": pts, "ast": ast, "reb": reb, "stl": stl,
                "blk": blk, "tov": tov, "fg_made": fg_made, "fg_att": fg_att,
            })

        # Sort by points desc
        rows.sort(key=lambda r: r["pts"], reverse=True)

        table.setSortingEnabled(False)
        table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            name_item = QTableWidgetItem(r["name"])
            name_item.setData(Qt.UserRole, r["sprite_id"])
            table.setItem(i, 0, name_item)

            arch_item = QTableWidgetItem(r["arch"][:3].upper() if r["arch"] else "?")
            arch_item.setTextAlignment(Qt.AlignCenter)
            arch_style = get_archetype_style(r["arch"])
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            table.setItem(i, 1, arch_item)

            stats_vals = [r["pts"], r["ast"], r["reb"], r["stl"], r["blk"], r["tov"]]
            for j, val in enumerate(stats_vals):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, val)
                item.setTextAlignment(Qt.AlignCenter)
                if j == 0 and val >= 10:
                    item.setForeground(QColor(COLORS['accent_primary']))
                table.setItem(i, j + 2, item)

            fg_item = QTableWidgetItem(f"{r['fg_made']}/{r['fg_att']}")
            fg_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 8, fg_item)

    # ── Post-game: auto-save ──────────────────────────────────────────────────

    def _auto_save_stats(self, stats):
        """Automatically save ripped game stats to the DB."""
        game_stats = stats.get("GameStats", {})
        slot_stats = stats.get("SlotStats", {})

        ballerz_score = game_stats.get("BallerzScore", 0)
        ringers_score = game_stats.get("RingersScore", 0)

        # Detect the "nuclear" ball-holding case: the tracker only injects
        # BallHolding_InPlay into active slots once every player has touched the
        # ball at least once. If any active slot is missing it (or it's None),
        # the iValue list never completed and ball-holding will be NULL for the
        # whole game. Warn the user visibly.
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
                self.gameMode = gs.get("GameMode", 0)
                self.ballerzScore = gs.get("BallerzScore", 0)
                self.ringersScore = gs.get("RingersScore", 0)
                self.slotStats = {"slotStats": {}}
                for slot_id, info in ss.items():
                    self.slotStats["slotStats"][f"Slot{slot_id}"] = info

        try:
            wrapper = _StatsWrapper(game_stats, slot_stats)
            game_id = d.statsDB_AddRippedGame(wrapper)
            d.statsDB_UploadRaw()
            self._save_status = f"Game saved successfully (ID: {game_id})  ·  Ballerz {ballerz_score} - {ringers_score} Ringers"
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
