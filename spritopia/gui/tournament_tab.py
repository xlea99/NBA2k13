"""
Tournament tab — create, draft, and run Spritopia tournaments.

Flow:  Setup Form → Draft Phase → Bracket Hub (active/complete)
All data is in-memory filler; backend model is not yet wired.
"""

import random
import uuid
from typing import Optional, Callable

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QFrame, QScrollArea, QSizePolicy, QPushButton, QStackedWidget,
    QComboBox, QGridLayout, QDialog,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QColor

from spritopia.gui.theme import COLORS, get_archetype_color
from spritopia.gui.app_state import get_app_state
from spritopia.data_storage.data_storage import d
from spritopia.gui.stats.stats_engine import StatsEngine

# ── Helpers ───────────────────────────────────────────────────────────────────

def _rgba(hex_color: str, alpha: int) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _get_premier_player_ids() -> Optional[set]:
    """Return sprite IDs of players with at least 1 Premier game, or None on failure."""
    try:
        raw_stats = (d.stats or {}).get("Raw")
        if not raw_stats:
            return None
        premier_raw = {
            gid: ginfo for gid, ginfo in raw_stats.items()
            if "Premier" in (ginfo.get("LoadedRoster") or "")
        }
        if not premier_raw:
            return None
        engine = StatsEngine(premier_raw, d.players)
        return {cs.sprite_id for cs in engine.get_all_career_stats() if cs.games_played >= 1}
    except Exception as e:
        print(f"[TournamentTab] Failed to load Premier player IDs: {e}")
        return None


# ── Option lists ──────────────────────────────────────────────────────────────

_DRAFT_MODES = [
    "Normal", "Random", "Semi-Random", "Archetypal-Random",
    "Captains", "Affirmative-Action", "Archetype Showdown",
    "Spritopian Duos", "Chaos", "Choice", "Choice 3",
]
_FORMATS     = ["Single Elimination", "Double Elimination", "Round Robin", "Swiss"]
_TEAM_COUNTS = [4, 8, 16]
_MATCH_FMTS  = ["Best of 1", "Best of 3", "Best of 5"]
_SEEDINGS    = ["Random", "Manual"]

_STATUS_STYLE = {
    "setup":    ("#f59e0b", "#1c0d00"),
    "active":   ("#22c55e", "#052e16"),
    "complete": ("#4a9eff", "#0c1a2e"),
}

# ── Filler player names ───────────────────────────────────────────────────────

_FILLER_PLAYERS = [
    "J. Williams",  "C. Jackson",   "D. Thomas",   "M. Davis",
    "T. Smith",     "K. Johnson",   "R. Brown",    "L. Garcia",
    "E. Martinez",  "A. Rodriguez", "B. Wilson",   "S. Miller",
    "P. Anderson",  "G. Taylor",    "F. Moore",    "H. Jones",
    "N. White",     "O. Harris",    "Q. Clark",    "I. Lewis",
    "Y. Robinson",  "Z. Walker",    "V. Hall",     "X. Allen",
    "U. Young",     "W. King",      "A. Wright",   "B. Scott",
    "C. Torres",    "D. Nguyen",    "E. Hill",     "F. Flores",
]

# ── Filler tournaments ────────────────────────────────────────────────────────

_FILLER = [
    {
        "id": "spring_classic",
        "name": "Spritopia Spring Classic",
        "format": "Single Elimination",
        "teams_count": 8,
        "draft_mode": "Chaos",
        "match_format": "Best of 1",
        "status": "active",
        "current_round": 1,
        "rosters": {
            "The Ballerz":       ["J. Williams",  "C. Jackson",  "D. Thomas",   "M. Davis"],
            "Ghost Squad":       ["T. Smith",     "K. Johnson",  "R. Brown",    "L. Garcia"],
            "The Ringers":       ["E. Martinez",  "A. Rodriguez","B. Wilson",   "S. Miller"],
            "Street Kings":      ["P. Anderson",  "G. Taylor",   "F. Moore",    "H. Jones"],
            "Iron Fives":        ["N. White",     "O. Harris",   "Q. Clark",    "I. Lewis"],
            "Concrete Cowboys":  ["Y. Robinson",  "Z. Walker",   "V. Hall",     "X. Allen"],
            "The Snipers":       ["U. Young",     "W. King",     "A. Wright",   "B. Scott"],
            "Hoops Wizards":     ["C. Torres",    "D. Nguyen",   "E. Hill",     "F. Flores"],
        },
        "rounds": [
            [
                {"team1": "The Ballerz",       "team2": "Ghost Squad",      "score1": 11, "score2": 7,    "winner": 0},
                {"team1": "The Ringers",        "team2": "Street Kings",     "score1": 9,  "score2": 11,   "winner": 1},
                {"team1": "Iron Fives",         "team2": "Concrete Cowboys", "score1": 11, "score2": 4,    "winner": 0},
                {"team1": "The Snipers",        "team2": "Hoops Wizards",    "score1": 7,  "score2": 11,   "winner": 1},
            ],
            [
                {"team1": "The Ballerz",        "team2": "Street Kings",     "score1": None, "score2": None, "winner": None},
                {"team1": "Iron Fives",         "team2": "Hoops Wizards",    "score1": None, "score2": None, "winner": None},
            ],
            [
                {"team1": "TBD",                "team2": "TBD",              "score1": None, "score2": None, "winner": None},
            ],
        ],
        "created": "Feb 15",
    },
    {
        "id": "winter_cup",
        "name": "The Winter Cup",
        "format": "Single Elimination",
        "teams_count": 4,
        "draft_mode": "Captains",
        "match_format": "Best of 1",
        "status": "complete",
        "current_round": 2,
        "rosters": {
            "The Ballerz":   ["J. Williams", "C. Jackson",  "D. Thomas",  "M. Davis"],
            "Iron Fives":    ["T. Smith",    "K. Johnson",  "R. Brown",   "L. Garcia"],
            "The Ringers":   ["E. Martinez", "A. Rodriguez","B. Wilson",  "S. Miller"],
            "Hoops Wizards": ["P. Anderson", "G. Taylor",   "F. Moore",   "H. Jones"],
        },
        "rounds": [
            [
                {"team1": "The Ballerz",  "team2": "Iron Fives",    "score1": 11, "score2": 6,  "winner": 0},
                {"team1": "The Ringers",  "team2": "Hoops Wizards", "score1": 8,  "score2": 11, "winner": 1},
            ],
            [
                {"team1": "The Ballerz",  "team2": "Hoops Wizards", "score1": 11, "score2": 9,  "winner": 0},
            ],
        ],
        "winner": "The Ballerz",
        "created": "Jan 20",
    },
]

# ── Bracket geometry ──────────────────────────────────────────────────────────

_CARD_H    = 82
_CARD_W    = 224
_V_GAP     = 10
_SLOT_BASE = _CARD_H + _V_GAP
_CONN_W    = 52


def _slot_h(r: int) -> int:                   return _SLOT_BASE * (2 ** r)
def _card_y(m: int, r: int) -> int:           return m * _slot_h(r) + (_slot_h(r) - _CARD_H) // 2
def _card_cy(m: int, r: int) -> int:          return _card_y(m, r) + _CARD_H // 2
def _bracket_h(n: int) -> int:                return (n // 2) * _SLOT_BASE


def _round_label(r: int, total: int) -> str:
    if r == total - 1: return "FINAL"
    if r == total - 2: return "SEMIFINALS"
    if r == total - 3: return "QUARTERFINALS"
    return f"ROUND {r + 1}"


# ── Bracket connector ─────────────────────────────────────────────────────────

class _Connector(QWidget):
    def __init__(self, n_left: int, bh: int, left_r: int, parent=None):
        super().__init__(parent)
        self._n, self._ri = n_left, left_r
        self.setFixedSize(_CONN_W, bh)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)
        p.setPen(QPen(QColor("#2d3352"), 1))
        mx = _CONN_W // 2
        for i in range(0, self._n, 2):
            top, bot = _card_cy(i, self._ri), _card_cy(i + 1, self._ri)
            mid = (top + bot) // 2
            p.drawLine(0, top, mx, top);  p.drawLine(0, bot, mx, bot)
            p.drawLine(mx, top, mx, bot); p.drawLine(mx, mid, _CONN_W, mid)
        p.end()


# ── Roster popup dialog ───────────────────────────────────────────────────────

class _RosterDialog(QDialog):
    def __init__(self, team_name: str, roster: list, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setFixedWidth(280)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 10px;
            }}
        """)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # Header
        hdr = QFrame()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet(f"""
            QFrame {{
                background-color: {_rgba(COLORS['accent_primary'], 25)};
                border-bottom: 1px solid {COLORS['border_dark']};
                border-radius: 10px 10px 0 0;
            }}
        """)
        hlo = QHBoxLayout(hdr)
        hlo.setContentsMargins(16, 0, 12, 0)

        name_lbl = QLabel(team_name)
        name_lbl.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        hlo.addWidget(name_lbl, stretch=1)

        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: none;
                color: {COLORS['text_muted']}; font-size: 18px; border-radius: 4px;
            }}
            QPushButton:hover {{ color: {COLORS['text_primary']}; background: {_rgba(COLORS['bg_light'], 200)}; }}
        """)
        close_btn.clicked.connect(self.accept)
        hlo.addWidget(close_btn)
        lo.addWidget(hdr)

        # Roster list
        body = QWidget()
        body.setStyleSheet("background: transparent;")
        blo = QVBoxLayout(body)
        blo.setContentsMargins(16, 12, 16, 16)
        blo.setSpacing(6)

        if roster:
            sub = QLabel(f"{len(roster)} player{'s' if len(roster) != 1 else ''}")
            sub.setStyleSheet(f"font-size: 10px; font-weight: bold; letter-spacing: 1px; color: {COLORS['text_muted']}; background: transparent;")
            blo.addWidget(sub)
            blo.addSpacing(4)
            for i, player in enumerate(roster, 1):
                row = QFrame()
                row.setFixedHeight(34)
                row.setStyleSheet(f"""
                    QFrame {{
                        background-color: {_rgba(COLORS['bg_dark'], 180)};
                        border-radius: 5px; border: none;
                    }}
                """)
                rlo = QHBoxLayout(row)
                rlo.setContentsMargins(10, 0, 10, 0)
                idx_lbl = QLabel(str(i))
                idx_lbl.setFixedWidth(18)
                idx_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
                rlo.addWidget(idx_lbl)
                p_lbl = QLabel(player)
                p_lbl.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {COLORS['text_primary']}; background: transparent;")
                rlo.addWidget(p_lbl, stretch=1)
                blo.addWidget(row)
        else:
            empty = QLabel("No roster drafted yet")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; background: transparent; padding: 16px 0;")
            blo.addWidget(empty)

        lo.addWidget(body)


# ── Match card ────────────────────────────────────────────────────────────────

class _MatchCard(QFrame):
    def __init__(self, match: dict, is_active: bool = False,
                 on_team_click: Optional[Callable] = None, parent=None):
        super().__init__(parent)
        self.setFixedSize(_CARD_W, _CARD_H)

        t1, t2 = match["team1"], match["team2"]
        s1, s2 = match.get("score1"), match.get("score2")
        w      = match.get("winner")
        done   = w is not None

        if is_active:
            border, bg = COLORS["accent_primary"], _rgba(COLORS["accent_primary"], 12)
        elif done:
            border, bg = COLORS["border_dark"], COLORS["bg_medium"]
        else:
            border, bg = _rgba(COLORS["border_dark"], 120), _rgba(COLORS["bg_medium"], 160)

        self.setStyleSheet(f"QFrame {{ background-color: {bg}; border: 1px solid {border}; border-radius: 6px; }}")

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background-color: {COLORS['border_dark']}; border: none;")

        lo.addWidget(self._row(t1, s1, w == 0, done and w != 0, on_team_click))
        lo.addWidget(div)
        lo.addWidget(self._row(t2, s2, w == 1, done and w != 1, on_team_click))

    def _row(self, name, score, winner, loser, on_team_click):
        row = QFrame()
        row.setFixedHeight(_CARD_H // 2)
        if winner:
            row.setStyleSheet(f"background-color: {_rgba(COLORS['accent_primary'], 22)}; border: none;")
            nc, sc, fw = COLORS["text_primary"],  COLORS["accent_primary"],  "700"
        elif loser:
            row.setStyleSheet("background-color: transparent; border: none;")
            nc, sc, fw = COLORS["text_muted"],    COLORS["text_muted"],      "400"
        else:
            row.setStyleSheet("background-color: transparent; border: none;")
            nc, sc, fw = COLORS["text_primary"],  COLORS["text_secondary"],  "400"

        rlo = QHBoxLayout(row)
        rlo.setContentsMargins(10, 0, 10, 0)
        rlo.setSpacing(6)

        dot = QLabel("●" if winner else " ")
        dot.setFixedWidth(10)
        dot.setStyleSheet(f"font-size: 7px; color: {COLORS['accent_primary']}; background: transparent; border: none;")
        rlo.addWidget(dot)

        # Team name — clickable if callback provided and name is not TBD
        if on_team_click and name != "TBD":
            nl = QPushButton(name)
            nl.setFlat(True)
            nl.setCursor(Qt.PointingHandCursor)
            nl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            nl.setStyleSheet(f"""
                QPushButton {{
                    font-size: 12px; font-weight: {fw}; color: {nc};
                    background: transparent; border: none;
                    text-align: left; padding: 0;
                }}
                QPushButton:hover {{ color: {COLORS['accent_primary']}; text-decoration: underline; }}
            """)
            nl.clicked.connect(lambda _, n=name: on_team_click(n))
        else:
            nl = QLabel(name)
            nl.setAttribute(Qt.WA_TransparentForMouseEvents)
            nl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            nl.setStyleSheet(f"font-size: 12px; font-weight: {fw}; color: {nc}; background: transparent; border: none;")

        rlo.addWidget(nl, stretch=1)

        sl = QLabel(str(score) if score is not None else "—")
        sl.setFixedWidth(22)
        sl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sl.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {sc}; background: transparent; border: none;")
        sl.setAttribute(Qt.WA_TransparentForMouseEvents)
        rlo.addWidget(sl)

        return row


# ── Bracket round column ──────────────────────────────────────────────────────

class _RoundCol(QWidget):
    _TITLE_H = 36

    def __init__(self, title, matches, r_idx, bh, cur_round,
                 on_team_click=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(_CARD_W, bh + self._TITLE_H)
        self.setStyleSheet("background: transparent;")

        lbl = QLabel(title, self)
        lbl.setGeometry(0, 0, _CARD_W, self._TITLE_H - 4)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"font-size: 9px; font-weight: bold; letter-spacing: 1.8px; color: {COLORS['text_muted']}; background: transparent;")

        for i, match in enumerate(matches):
            is_active = (r_idx == cur_round and match.get("winner") is None)
            card = _MatchCard(match, is_active=is_active, on_team_click=on_team_click, parent=self)
            card.move(0, self._TITLE_H + _card_y(i, r_idx))


# ── Bracket scroll view ───────────────────────────────────────────────────────

class _BracketView(QScrollArea):
    def __init__(self, tourney: dict, on_team_click: Optional[Callable] = None, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidgetResizable(False)
        self.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {COLORS['bg_dark']}; }}
            QScrollBar:horizontal, QScrollBar:vertical {{
                background: transparent; border: none; width: 6px; height: 6px;
            }}
            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
                background: rgba(255,255,255,40); border-radius: 3px;
                min-width: 20px; min-height: 20px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
            QScrollBar::add-line:vertical,   QScrollBar::sub-line:vertical {{
                width: 0px; height: 0px;
            }}
        """)

        rounds    = tourney["rounds"]
        n_teams   = tourney["teams_count"]
        cur_round = tourney.get("current_round", 0)
        n_rounds  = len(rounds)
        bh        = _bracket_h(n_teams)
        title_h   = _RoundCol._TITLE_H
        pad       = 48

        total_w = pad + n_rounds * _CARD_W + max(0, n_rounds - 1) * _CONN_W + pad
        total_h = title_h + bh + 32

        c = QWidget()
        c.setFixedSize(total_w, total_h)
        c.setStyleSheet(f"background-color: {COLORS['bg_dark']};")

        x = pad
        for r_idx, matches in enumerate(rounds):
            col = _RoundCol(_round_label(r_idx, n_rounds), matches, r_idx,
                            bh, cur_round, on_team_click=on_team_click, parent=c)
            col.move(x, 16)
            x += _CARD_W
            if r_idx < n_rounds - 1:
                conn = _Connector(len(matches), bh, r_idx, c)
                conn.move(x, 16 + title_h)
                x += _CONN_W

        self.setWidget(c)


# ── Tournament hub (active / complete) ────────────────────────────────────────

class _HubView(QWidget):
    def __init__(self, tourney: dict, parent=None):
        super().__init__(parent)
        self._tourney = tourney
        self.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        lo.addWidget(self._header())
        lo.addWidget(self._content(), stretch=1)
        lo.addWidget(self._footer())

    def _on_team_click(self, team_name: str):
        rosters = self._tourney.get("rosters", {})
        dlg = _RosterDialog(team_name, rosters.get(team_name, []), self)
        dlg.adjustSize()
        center = self.mapToGlobal(self.rect().center())
        dlg.move(center.x() - dlg.width() // 2, center.y() - dlg.height() // 2)
        dlg.exec()

    def _header(self) -> QFrame:
        t = self._tourney
        h = QFrame()
        h.setFixedHeight(90)
        h.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QHBoxLayout(h)
        lo.setContentsMargins(28, 0, 24, 0)
        lo.setSpacing(16)

        info = QVBoxLayout()
        info.setSpacing(5)
        name_lbl = QLabel(t["name"])
        name_lbl.setStyleSheet(f"font-size: 21px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        info.addWidget(name_lbl)
        parts = [t["format"], f"{t['teams_count']} Teams", f"{t['draft_mode']} Draft", t.get("created", "")]
        sub = QLabel("  ·  ".join(p for p in parts if p))
        sub.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
        info.addWidget(sub)
        lo.addLayout(info, stretch=1)

        tc, bc = _STATUS_STYLE.get(t["status"], ("#aaa", "#222"))
        pill = QLabel(t["status"].upper())
        pill.setStyleSheet(f"""
            font-size: 10px; font-weight: bold; letter-spacing: 1px;
            color: {tc}; background-color: {_rgba(bc, 255)};
            padding: 4px 12px; border-radius: 10px;
        """)
        lo.addWidget(pill)

        if t["status"] == "active":
            btn = QPushButton("  Play Next Match")
            btn.setFixedHeight(36)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_primary']};
                    color: white; border: none; border-radius: 18px;
                    font-size: 13px; font-weight: 600; padding: 0 22px;
                }}
                QPushButton:hover {{ background-color: {_rgba(COLORS['accent_primary'], 200)}; }}
            """)
            lo.addWidget(btn)

        return h

    def _content(self) -> QWidget:
        t = self._tourney
        w = QWidget()
        w.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        if t["format"] == "Single Elimination":
            lo.addWidget(_BracketView(t, on_team_click=self._on_team_click))
        else:
            ph = QLabel(f"{t['format']} view — coming soon")
            ph.setAlignment(Qt.AlignCenter)
            ph.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']};")
            lo.addWidget(ph, stretch=1)
        return w

    def _footer(self) -> QFrame:
        t = self._tourney
        f = QFrame()
        f.setFixedHeight(52)
        f.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QHBoxLayout(f)
        lo.setContentsMargins(28, 0, 24, 0)
        lo.setSpacing(12)

        hint = QLabel("Click any team name in the bracket to view their roster.")
        hint.setStyleSheet(f"font-size: 11px; color: {_rgba(COLORS['text_muted'], 160)}; background: transparent;")
        lo.addWidget(hint)
        lo.addStretch()

        if t["status"] == "complete":
            champ = QLabel(f"  {t.get('winner', '?')}  —  Tournament Champion")
            champ.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']}; background: transparent;")
            lo.addWidget(champ)
        elif t["status"] == "active":
            n_rounds  = len(t["rounds"])
            cur       = t.get("current_round", 0)
            remaining = sum(1 for m in t["rounds"][cur] if m.get("winner") is None)
            stage_lbl = QLabel(f"{_round_label(cur, n_rounds)}  ·  {remaining} match{'es' if remaining != 1 else ''} remaining")
            stage_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_secondary']}; background: transparent;")
            lo.addWidget(stage_lbl)

        return f


# ── Tournament choice card ────────────────────────────────────────────────────

class _TournamentChoiceCard(QFrame):
    """Clickable card shown during Choice-mode picks in the tournament draft."""
    clicked = Signal(object)  # emits player

    def __init__(self, player, parent=None):
        super().__init__(parent)
        self._player = player
        self.setFixedHeight(90)
        self.setMaximumWidth(230)
        self.setCursor(Qt.PointingHandCursor)
        arch  = player["Archetype_Name"]
        color = get_archetype_color(arch)
        self._ss_n = (
            f"QFrame {{ background-color: {COLORS['bg_medium']}; "
            f"border: 1px solid {COLORS['border_dark']}; border-radius: 8px; }}"
        )
        self._ss_h = (
            f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 30)}; "
            f"border: 1px solid {COLORS['accent_primary']}; border-radius: 8px; }}"
        )
        self.setStyleSheet(self._ss_n)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(14, 10, 14, 8)
        lo.setSpacing(4)

        name_lbl = QLabel(f"{player['First_Name']} {player['Last_Name']}")
        name_lbl.setStyleSheet(
            f"font-size: 13px; font-weight: 600; color: {COLORS['text_primary']}; background: transparent;"
        )
        lo.addWidget(name_lbl)

        arch_lbl = QLabel(arch)
        arch_lbl.setStyleSheet(f"font-size: 11px; color: {color}; background: transparent;")
        lo.addWidget(arch_lbl)

        lo.addStretch()

        hint = QLabel("click to pick")
        hint.setStyleSheet(
            f"font-size: 9px; color: {_rgba(COLORS['text_muted'], 140)}; background: transparent;"
        )
        lo.addWidget(hint)

        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    def enterEvent(self, _e): self.setStyleSheet(self._ss_h)
    def leaveEvent(self, _e): self.setStyleSheet(self._ss_n)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.position().toPoint()):
            self.clicked.emit(self._player)


# ── Draft phase — team roster card ────────────────────────────────────────────

class _TeamDraftCard(QFrame):
    def __init__(self, team_name: str, parent=None):
        super().__init__(parent)
        self._team   = team_name
        self._filled = 0
        self.setFixedSize(220, 192)

        self._ss_idle   = f"QFrame {{ background-color: {COLORS['bg_medium']}; border: 1px solid {COLORS['border_dark']}; border-radius: 8px; }}"
        self._ss_active = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 20)}; border: 2px solid {COLORS['accent_primary']}; border-radius: 8px; }}"
        self.setStyleSheet(self._ss_idle)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # Header
        hdr = QFrame()
        hdr.setFixedHeight(36)
        hdr.setStyleSheet(f"""
            QFrame {{
                background-color: {_rgba(COLORS['accent_primary'], 18)};
                border-bottom: 1px solid {COLORS['border_dark']};
                border-radius: 8px 8px 0 0;
            }}
        """)
        hlo = QHBoxLayout(hdr)
        hlo.setContentsMargins(10, 0, 10, 0)
        t_lbl = QLabel(team_name)
        t_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        hlo.addWidget(t_lbl)
        lo.addWidget(hdr)

        # Slots
        slots_w = QWidget()
        slots_w.setStyleSheet("background: transparent;")
        slo = QVBoxLayout(slots_w)
        slo.setContentsMargins(10, 8, 10, 8)
        slo.setSpacing(4)
        self._slots: list = []
        for i in range(4):
            lbl = QLabel(f"{i + 1}.   —")
            lbl.setFixedHeight(28)
            lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
            slo.addWidget(lbl)
            self._slots.append(lbl)
        lo.addWidget(slots_w)

    def set_roster(self, players: list):
        for i, lbl in enumerate(self._slots):
            if i < len(players):
                p = players[i]
                if isinstance(p, str):
                    name, color = p, COLORS["text_primary"]
                else:
                    name  = f"{p['First_Name']} {p['Last_Name']}"
                    color = get_archetype_color(p["Archetype_Name"])
                lbl.setText(f"{i + 1}.  {name}")
                lbl.setStyleSheet(f"font-size: 12px; color: {color}; background: transparent;")
            else:
                lbl.setText(f"{i + 1}.   —")
                lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
        self._filled = min(len(players), 4)

    def set_active(self, active: bool):
        self.setStyleSheet(self._ss_active if active else self._ss_idle)

    def is_full(self) -> bool:
        return self._filled >= 4


# ── Draft phase view ──────────────────────────────────────────────────────────

class _DraftPhaseView(QWidget):
    """
    Tournament draft — uses the main app sidebar (PlayerFinderWidget) for picking.
    Emits draft_excluded_updated so the sidebar hides already-picked players,
    and slot_filter_changed to filter the sidebar by archetype when needed.
    """
    begin_requested        = Signal()
    draft_excluded_updated = Signal(set)  # SpriteIDs of picked players → sidebar exclusion
    slot_filter_changed    = Signal(str)  # archetype name or "" for no filter
    PICKS_PER_TEAM         = 4

    def __init__(self, tourney: dict, parent=None):
        super().__init__(parent)
        self._tourney     = tourney
        self._teams       = self._get_teams()
        self._draft_order = self._build_snake_order()
        self._pick_slots  = self._gen_slots(tourney.get("draft_mode", "Normal"))
        self._pick_idx    = 0
        self._rosters: dict  = {t: [] for t in self._teams}
        self._all_players: list = []
        self._available:   list = []
        self._team_cards:  dict = {}
        self._waiting_for_pick: bool = False
        self._current_arch_restriction: Optional[str] = None  # active archetype filter
        self._choice_pool: list = []
        self._choice_cards: list = []
        self.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        self._build_ui()
        self._load_players()

    # ── State helpers ──────────────────────────────────────────────────────

    def _get_teams(self) -> list:
        teams, seen = [], set()
        for match in self._tourney["rounds"][0]:
            for name in (match["team1"], match["team2"]):
                if name not in seen and name != "TBD":
                    seen.add(name); teams.append(name)
        return teams

    def _build_snake_order(self) -> list:
        order = []
        for r in range(self.PICKS_PER_TEAM):
            order.extend(self._teams if r % 2 == 0 else list(reversed(self._teams)))
        return order

    def _current_team(self):
        return self._draft_order[self._pick_idx] if self._pick_idx < len(self._draft_order) else None

    def _total_picks(self) -> int: return len(self._draft_order)
    def _is_done(self)     -> bool: return self._pick_idx >= self._total_picks()

    def _gen_slots(self, draft_mode: str) -> list:
        """Generate a pick-slot type for each position in the full snake draft order."""
        total = self.PICKS_PER_TEAM * len(self._teams)
        if not total:
            return []
        archs = [
            "Archetype (Slayer)", "Archetype (Vigilante)", "Archetype (Medic)",
            "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)",
        ]
        if draft_mode == "Random":
            return ["Random"] * total
        if draft_mode == "Semi-Random":
            return ["Normal" if i % 2 == 0 else "Random" for i in range(total)]
        if draft_mode == "Archetypal-Random":
            return [random.choice(archs) for _ in range(total)]
        if draft_mode == "Captains":
            team_seen: set = set()
            slots = []
            for team in self._draft_order:
                slots.append("Random" if team not in team_seen else "Normal")
                team_seen.add(team)
            return slots
        if draft_mode == "Affirmative-Action":
            team_last: dict = {}
            for i, team in enumerate(self._draft_order):
                team_last[team] = i
            last_set = set(team_last.values())
            return ["Random" if i in last_set else "Normal" for i in range(total)]
        if draft_mode == "Archetype Showdown":
            team_arch = {t: random.choice(archs) for t in self._teams}
            return [team_arch[self._draft_order[i]] for i in range(total)]
        if draft_mode == "Spritopian Duos":
            shooters = ["Archetype (Slayer)", "Archetype (Vigilante)"]
            non_s    = ["Archetype (Medic)", "Archetype (Guardian)",
                        "Archetype (Engineer)", "Archetype (Director)"]
            team_arches = {t: (random.choice(shooters), random.choice(non_s)) for t in self._teams}
            team_pick_n = {t: 0 for t in self._teams}
            slots = []
            for team in self._draft_order:
                n = team_pick_n[team]
                a1, a2 = team_arches[team]
                slots.append(a1 if n % 2 == 0 else a2)
                team_pick_n[team] += 1
            return slots
        if draft_mode == "Chaos":
            options = [
                "Normal", "Random", "Choice", "Choice 3",
                "Archetype (Slayer)", "Archetype (Vigilante)", "Archetype (Medic)",
                "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)",
            ]
            return [random.choice(options) for _ in range(total)]
        if draft_mode == "Choice":
            return ["Choice"] * total
        if draft_mode == "Choice 3":
            return ["Choice 3"] * total
        return ["Normal"] * total  # Default / "Normal"

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        t  = self._tourney
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # ── Header ─────────────────────────────────────────────────────────
        hdr = QFrame()
        hdr.setFixedHeight(90)
        hdr.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        hlo = QHBoxLayout(hdr)
        hlo.setContentsMargins(28, 0, 24, 0)
        hlo.setSpacing(16)

        info = QVBoxLayout()
        info.setSpacing(5)
        name_lbl = QLabel(t["name"])
        name_lbl.setStyleSheet(f"font-size: 21px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        info.addWidget(name_lbl)

        sub_row = QHBoxLayout()
        sub_row.setSpacing(10)
        sub_lbl = QLabel(f"Pre-Tournament Draft  ·  Snake order  ·  {self.PICKS_PER_TEAM} picks per team")
        sub_lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
        sub_row.addWidget(sub_lbl)
        mode_pill = QLabel(t.get("draft_mode", "Normal"))
        mode_pill.setStyleSheet("""
            font-size: 10px; font-weight: bold; letter-spacing: 0.8px;
            color: #a78bfa; background-color: #1e0b3b;
            padding: 2px 10px; border-radius: 8px;
        """)
        sub_row.addWidget(mode_pill)
        sub_row.addStretch()
        info.addLayout(sub_row)
        hlo.addLayout(info, stretch=1)

        auto_btn = QPushButton("Auto-Draft All")
        auto_btn.setFixedHeight(36)
        auto_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_rgba(COLORS['accent_primary'], 40)};
                color: {COLORS['accent_primary']};
                border: 1px solid {_rgba(COLORS['accent_primary'], 90)};
                border-radius: 18px; font-size: 13px; font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_primary']}; color: white; }}
        """)
        auto_btn.clicked.connect(self._auto_draft_all)
        hlo.addWidget(auto_btn)
        lo.addWidget(hdr)

        # ── Choice strip (hidden until a Choice-type slot) ─────────────────
        self._choice_strip = QFrame()
        self._choice_strip.setStyleSheet(f"""
            QFrame {{
                background-color: {_rgba(COLORS['bg_medium'], 255)};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        self._choice_strip.setVisible(False)
        cs_lo = QVBoxLayout(self._choice_strip)
        cs_lo.setContentsMargins(24, 10, 24, 12)
        cs_lo.setSpacing(8)

        self._choice_header_lbl = QLabel("CHOOSE A PLAYER")
        self._choice_header_lbl.setStyleSheet(
            f"font-size: 9px; font-weight: bold; letter-spacing: 1.5px; color: {COLORS['text_muted']}; background: transparent;"
        )
        cs_lo.addWidget(self._choice_header_lbl)

        self._choice_cards_lo = QHBoxLayout()
        self._choice_cards_lo.setSpacing(10)
        cs_lo.addLayout(self._choice_cards_lo)
        lo.addWidget(self._choice_strip)

        # ── Team grid (full width) ─────────────────────────────────────────
        lo.addWidget(self._build_team_grid(), stretch=1)

        # ── Footer ─────────────────────────────────────────────────────────
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        flo = QHBoxLayout(footer)
        flo.setContentsMargins(28, 0, 24, 0)
        flo.setSpacing(16)

        self._slot_chip_lbl = QLabel("")
        self._slot_chip_lbl.setAlignment(Qt.AlignCenter)
        self._slot_chip_lbl.setStyleSheet(
            f"font-size: 10px; font-weight: bold; letter-spacing: 0.8px; "
            f"color: {COLORS['text_secondary']}; background: {COLORS['bg_light']}; "
            f"padding: 3px 10px; border-radius: 8px;"
        )
        self._slot_chip_lbl.setVisible(False)
        flo.addWidget(self._slot_chip_lbl)

        self._turn_lbl = QLabel("")
        self._turn_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_secondary']}; background: transparent;")
        flo.addWidget(self._turn_lbl)

        self._pick_hint_lbl = QLabel("")
        self._pick_hint_lbl.setStyleSheet(
            f"font-size: 11px; font-style: italic; color: {COLORS['text_muted']}; background: transparent;"
        )
        flo.addWidget(self._pick_hint_lbl)
        flo.addStretch()

        self._begin_btn = QPushButton("Begin Tournament")
        self._begin_btn.setFixedHeight(38)
        self._begin_btn.setEnabled(False)
        self._begin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white; border: none; border-radius: 19px;
                font-size: 13px; font-weight: 700; padding: 0 28px;
            }}
            QPushButton:hover {{ background-color: {_rgba(COLORS['accent_primary'], 200)}; }}
            QPushButton:disabled {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_muted']};
            }}
        """)
        self._begin_btn.clicked.connect(self.begin_requested)
        flo.addWidget(self._begin_btn)
        lo.addWidget(footer)

    def _build_team_grid(self) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {COLORS['bg_dark']}; }}
            QScrollBar:vertical {{ width: 6px; background: transparent; border: none; }}
            QScrollBar::handle:vertical {{ background: rgba(255,255,255,40); border-radius: 3px; min-height: 20px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)
        grid_w = QWidget()
        grid_w.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        grid = QGridLayout(grid_w)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)

        cols = 4 if len(self._teams) >= 8 else 2
        for i, team in enumerate(self._teams):
            card = _TeamDraftCard(team)
            self._team_cards[team] = card
            grid.addWidget(card, i // cols, i % cols)

        scroll.setWidget(grid_w)
        return scroll

    # ── Player loading ─────────────────────────────────────────────────────

    def _load_players(self):
        try:
            premier_ids = _get_premier_player_ids()
            raw = [p for p in get_app_state().players
                   if premier_ids is None or p["SpriteID"] in premier_ids]
            self._all_players = sorted(
                raw,
                key=lambda p: (p["Archetype_Name"], p["Last_Name"], p["First_Name"])
            )
        except Exception:
            self._all_players = []
        self._available = list(self._all_players)
        self._refresh_ui()
        self._process_current_slot()

    # ── Slot processing ─────────────────────────────────────────────────────

    def _process_current_slot(self):
        """Handle the current pick slot: auto-pick or wait for sidebar selection."""
        if self._is_done():
            self._waiting_for_pick = False
            self._choice_strip.setVisible(False)
            self.slot_filter_changed.emit("")
            self._refresh_ui()
            return

        slot_type = self._pick_slots[self._pick_idx]

        if slot_type == "Normal":
            self._current_arch_restriction = None
            self._waiting_for_pick = True
            self._choice_strip.setVisible(False)
            self.slot_filter_changed.emit("")

        elif slot_type == "Random":
            self._current_arch_restriction = None
            self._waiting_for_pick = False
            self._choice_strip.setVisible(False)
            self.slot_filter_changed.emit("")
            self._refresh_ui()  # show "RANDOM" chip before auto-pick fires
            self._auto_pick_random()
            return  # _pick_player will recurse to next slot

        elif slot_type in ("Choice", "Choice 3"):
            self._current_arch_restriction = None
            n = 3 if slot_type == "Choice 3" else 2
            pool = list(self._available)
            if pool:
                choices = random.sample(pool, min(n, len(pool)))
                self._show_choices(choices)
            else:
                self._auto_pick_random()
                return

        elif slot_type.startswith("Archetype ("):
            arch_name = slot_type[len("Archetype ("):-1]
            if arch_name == "Random":
                arch_name = random.choice(
                    ["Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"]
                )
            arch_pool = [p for p in self._available if p["Archetype_Name"] == arch_name]
            if arch_pool:
                # Filter sidebar to this archetype — user must pick from the restriction
                self._current_arch_restriction = arch_name
                self._waiting_for_pick = True
                self._choice_strip.setVisible(False)
                self.slot_filter_changed.emit(arch_name)
            else:
                # That archetype is exhausted — fall back to free Normal pick
                self._current_arch_restriction = None
                self._waiting_for_pick = True
                self._choice_strip.setVisible(False)
                self.slot_filter_changed.emit("")

        self._refresh_ui()

    def _show_choices(self, choices: list):
        """Populate the choice strip with clickable cards."""
        while self._choice_cards_lo.count():
            item = self._choice_cards_lo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._choice_cards.clear()

        team = self._current_team()
        n = len(choices)
        self._choice_header_lbl.setText(
            f"CHOOSE 1 OF {n}  ·  {team}'s pick" if team else f"CHOOSE 1 OF {n}"
        )
        for player in choices:
            card = _TournamentChoiceCard(player)
            card.clicked.connect(self._on_choice_picked)
            self._choice_cards_lo.addWidget(card)
            self._choice_cards.append(card)
        self._choice_cards_lo.addStretch()

        self._choice_pool = list(choices)
        self._choice_strip.setVisible(True)
        self._waiting_for_pick = True

    def _on_choice_picked(self, player):
        if not self._waiting_for_pick:
            return
        if not any(p["SpriteID"] == player["SpriteID"] for p in self._choice_pool):
            return
        self._pick_player(player)

    # ── Public pick interface ───────────────────────────────────────────────

    def pick_from_sidebar(self, player):
        """Called by TournamentTab when the user selects a player in the main sidebar."""
        if not self._waiting_for_pick or self._is_done():
            return
        if self._choice_strip.isVisible():
            return  # Choice turn — must use choice cards, not free pick
        if not any(p["SpriteID"] == player["SpriteID"] for p in self._available):
            return  # Already picked
        # Enforce archetype restriction when active
        if self._current_arch_restriction:
            if player["Archetype_Name"] != self._current_arch_restriction:
                return
        self._pick_player(player)

    # ── Draft actions ──────────────────────────────────────────────────────

    def _auto_pick_random(self):
        if not self._available:
            self._refresh_ui()
            return
        self._pick_player(random.choice(self._available))

    def _pick_player(self, player):
        team = self._current_team()
        if not team or self._is_done():
            return
        self._rosters[team].append(player)
        pid = player["SpriteID"]
        self._available = [p for p in self._available if p["SpriteID"] != pid]
        self._team_cards[team].set_roster(self._rosters[team])
        self._pick_idx += 1
        self._waiting_for_pick = False
        self._current_arch_restriction = None
        self._choice_strip.setVisible(False)
        self.slot_filter_changed.emit("")  # Always reset sidebar filter after a pick

        # Notify sidebar: exclude all picked player IDs
        picked_ids = {
            p["SpriteID"]
            for team_players in self._rosters.values()
            for p in team_players
            if not isinstance(p, str)
        }
        self.draft_excluded_updated.emit(picked_ids)

        if self._is_done():
            self._flush_rosters()
            self._refresh_ui()
        else:
            self._process_current_slot()

    def _auto_draft_all(self):
        """Immediately fill all remaining picks with random players, ignoring slot types."""
        if self._all_players:
            pool = list(self._available)
            random.shuffle(pool)
            for idx in range(self._pick_idx, self._total_picks()):
                if not pool:
                    break
                team   = self._draft_order[idx]
                player = pool.pop(0)
                self._rosters[team].append(player)
                self._available = [p for p in self._available if p["SpriteID"] != player["SpriteID"]]
                self._team_cards[team].set_roster(self._rosters[team])
                self._pick_idx += 1
        else:
            names = list(_FILLER_PLAYERS)
            random.shuffle(names)
            for idx in range(self._pick_idx, self._total_picks()):
                if not names:
                    break
                team = self._draft_order[idx]
                self._rosters[team].append(names.pop(0))
                self._team_cards[team].set_roster(self._rosters[team])
                self._pick_idx += 1
        self._flush_rosters()
        self._waiting_for_pick = False
        self._current_arch_restriction = None
        self._choice_strip.setVisible(False)
        self.slot_filter_changed.emit("")
        picked_ids = {
            p["SpriteID"]
            for team_players in self._rosters.values()
            for p in team_players
            if not isinstance(p, str)
        }
        self.draft_excluded_updated.emit(picked_ids)
        self._refresh_ui()

    def _flush_rosters(self):
        """Store player names into tourney dict for bracket/hub use."""
        for team, players in self._rosters.items():
            self._tourney["rosters"][team] = [
                (f"{p['First_Name']} {p['Last_Name']}" if not isinstance(p, str) else p)
                for p in players
            ]

    # ── Slot chip helpers ───────────────────────────────────────────────────

    def _slot_chip_text(self, slot_type: str) -> str:
        if slot_type == "Normal":    return "NORMAL"
        if slot_type == "Random":    return "RANDOM"
        if slot_type == "Choice":    return "CHOICE — 2"
        if slot_type == "Choice 3":  return "CHOICE — 3"
        if slot_type.startswith("Archetype ("):
            # Use the resolved restriction name when available
            arch = self._current_arch_restriction or slot_type[len("Archetype ("):-1]
            if arch == "Random":
                arch = "?"
            return f"{arch.upper()} ONLY"
        return slot_type.upper()

    def _slot_chip_style(self, slot_type: str) -> str:
        base = "font-size: 10px; font-weight: bold; letter-spacing: 0.8px; padding: 3px 10px; border-radius: 8px;"
        if slot_type == "Random":
            return f"{base} color: #1a1a1a; background: {COLORS['accent_warning']};"
        if slot_type in ("Choice", "Choice 3"):
            return f"{base} color: #ffffff; background: #06b6d4;"
        if slot_type.startswith("Archetype ("):
            return f"{base} color: #ffffff; background: {COLORS['accent_primary']};"
        return f"{base} color: {COLORS['text_secondary']}; background: {COLORS['bg_light']};"

    def _refresh_ui(self):
        team = self._current_team()
        done = self._is_done()

        for t_name, card in self._team_cards.items():
            card.set_active(t_name == team and not done)

        if done:
            self._slot_chip_lbl.setVisible(False)
            self._turn_lbl.setText("Draft complete — all teams ready!")
            self._turn_lbl.setStyleSheet(
                f"font-size: 13px; font-weight: 600; color: {COLORS['accent_primary']}; background: transparent;"
            )
            self._pick_hint_lbl.setText("")
        elif not self._all_players:
            self._slot_chip_lbl.setVisible(False)
            self._turn_lbl.setText("No players loaded — use Auto-Draft or load player data first.")
            self._turn_lbl.setStyleSheet(
                f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;"
            )
            self._pick_hint_lbl.setText("")
        else:
            slot_type = self._pick_slots[self._pick_idx] if self._pick_idx < len(self._pick_slots) else "Normal"

            # Slot type chip
            self._slot_chip_lbl.setText(self._slot_chip_text(slot_type))
            self._slot_chip_lbl.setStyleSheet(self._slot_chip_style(slot_type))
            self._slot_chip_lbl.setVisible(True)

            self._turn_lbl.setText(f"→  {team}  ·  Pick {self._pick_idx + 1} of {self._total_picks()}")
            self._turn_lbl.setStyleSheet(
                f"font-size: 13px; color: {COLORS['text_secondary']}; background: transparent;"
            )

            # Hint text
            if slot_type == "Normal":
                self._pick_hint_lbl.setText("Click a player in the left sidebar to pick")
            elif slot_type == "Random":
                self._pick_hint_lbl.setText("Auto-picking a random player…")
            elif slot_type in ("Choice", "Choice 3"):
                self._pick_hint_lbl.setText("Choose from the cards above")
            elif slot_type.startswith("Archetype ("):
                arch = self._current_arch_restriction or ""
                if arch:
                    self._pick_hint_lbl.setText(
                        f"Pick a {arch} from the sidebar (filtered)"
                    )
                else:
                    self._pick_hint_lbl.setText("Click a player in the left sidebar to pick")
            else:
                self._pick_hint_lbl.setText("")

        self._begin_btn.setEnabled(done)


# ── Setup form ────────────────────────────────────────────────────────────────

class _SetupView(QWidget):
    create_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        self._team_edits: list = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {COLORS['bg_dark']}; }}")

        inner = QWidget()
        inner.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(inner)
        lo.setContentsMargins(72, 44, 72, 44)
        lo.setSpacing(24)

        title = QLabel("New Tournament")
        title.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        lo.addWidget(title)

        sub = QLabel("Configure your bracket — teams will draft their rosters before the first game.")
        sub.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; background: transparent;")
        sub.setWordWrap(True)
        lo.addWidget(sub)

        lo.addWidget(self._div())
        lo.addWidget(self._sec("TOURNAMENT NAME"))
        self._name_edit = self._le("e.g. Spring Invitational")
        lo.addWidget(self._name_edit)

        lo.addWidget(self._div())
        lo.addWidget(self._sec("FORMAT"))
        self._fmt_combo = self._combo(_FORMATS)
        lo.addWidget(self._fmt_combo)

        lo.addWidget(self._div())
        lo.addWidget(self._sec("NUMBER OF TEAMS"))
        self._tc_combo = self._combo([str(n) for n in _TEAM_COUNTS])
        self._tc_combo.currentIndexChanged.connect(self._rebuild_teams)
        lo.addWidget(self._tc_combo)

        lo.addWidget(self._div())
        lo.addWidget(self._sec("TEAM NAMES"))
        self._teams_container = QWidget()
        self._teams_container.setStyleSheet("background: transparent;")
        self._teams_grid = QGridLayout(self._teams_container)
        self._teams_grid.setContentsMargins(0, 0, 0, 0)
        self._teams_grid.setHorizontalSpacing(16)
        self._teams_grid.setVerticalSpacing(10)
        lo.addWidget(self._teams_container)
        self._rebuild_teams()

        lo.addWidget(self._div())
        lo.addWidget(self._sec("DRAFT MODE  (applied per match)"))
        self._draft_combo = self._combo(_DRAFT_MODES)
        self._draft_combo.setCurrentText("Chaos")
        lo.addWidget(self._draft_combo)

        lo.addWidget(self._div())

        row_w = QWidget()
        row_w.setStyleSheet("background: transparent;")
        rlo = QHBoxLayout(row_w)
        rlo.setContentsMargins(0, 0, 0, 0)
        rlo.setSpacing(32)

        lc = QVBoxLayout()
        lc.setSpacing(8)
        lc.addWidget(self._sec("MATCH FORMAT"))
        self._mf_combo = self._combo(_MATCH_FMTS)
        lc.addWidget(self._mf_combo)
        rlo.addLayout(lc)

        rc = QVBoxLayout()
        rc.setSpacing(8)
        rc.addWidget(self._sec("SEEDING"))
        self._seed_combo = self._combo(_SEEDINGS)
        rc.addWidget(self._seed_combo)
        rlo.addLayout(rc)

        rlo.addStretch()
        lo.addWidget(row_w)
        lo.addSpacing(8)

        self._create_btn = QPushButton("Create Tournament  →  Draft")
        self._create_btn.setFixedHeight(46)
        self._create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white; border: none; border-radius: 23px;
                font-size: 14px; font-weight: 700;
            }}
            QPushButton:hover {{ background-color: {_rgba(COLORS['accent_primary'], 200)}; }}
        """)
        self._create_btn.clicked.connect(self._emit)
        lo.addWidget(self._create_btn)
        lo.addStretch()

        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _sec(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; letter-spacing: 1.5px; color: {COLORS['text_muted']}; background: transparent;")
        return lbl

    def _div(self):
        d = QFrame()
        d.setFrameShape(QFrame.HLine)
        d.setFixedHeight(1)
        d.setStyleSheet(f"background-color: {COLORS['border_dark']}; border: none;")
        return d

    def _le(self, placeholder=""):
        e = QLineEdit()
        e.setPlaceholderText(placeholder)
        e.setFixedHeight(38)
        e.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px; color: {COLORS['text_primary']};
                font-size: 13px; padding: 0 12px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent_primary']}; }}
        """)
        return e

    def _combo(self, items):
        c = QComboBox()
        c.addItems(items)
        c.setFixedHeight(38)
        c.setMaxVisibleItems(len(items))
        c.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px; color: {COLORS['text_primary']};
                font-size: 13px; padding: 0 12px;
            }}
            QComboBox:focus {{ border-color: {COLORS['accent_primary']}; }}
            QComboBox::drop-down {{ border: none; width: 24px; }}
            QComboBox::down-arrow {{ image: none; width: 0px; }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                color: {COLORS['text_primary']};
                selection-background-color: {COLORS['accent_primary']};
                selection-color: white; padding: 2px;
            }}
        """)
        return c

    def _rebuild_teams(self):
        for i in reversed(range(self._teams_grid.count())):
            w = self._teams_grid.itemAt(i).widget()
            if w: w.deleteLater()
        self._team_edits.clear()
        n = _TEAM_COUNTS[self._tc_combo.currentIndex()]
        defaults = [
            "The Ballerz", "The Ringers", "Street Kings", "Ghost Squad",
            "Iron Fives",  "Concrete Cowboys", "The Snipers", "Hoops Wizards",
            "Shadow Runners", "Neon Fives", "Desert Kings", "Rim Rockers",
            "Blacktop Elite", "City Slickers", "The Playmakers", "Grind Squad",
        ]
        for i in range(n):
            e = self._le(f"Team {i + 1}")
            e.setText(defaults[i] if i < len(defaults) else f"Team {i + 1}")
            self._teams_grid.addWidget(e, i // 2, i % 2)
            self._team_edits.append(e)

    def _emit(self):
        self.create_requested.emit({
            "name":         self._name_edit.text().strip() or "New Tournament",
            "format":       self._fmt_combo.currentText(),
            "teams_count":  _TEAM_COUNTS[self._tc_combo.currentIndex()],
            "teams":        [e.text().strip() or f"Team {i+1}" for i, e in enumerate(self._team_edits)],
            "draft_mode":   self._draft_combo.currentText(),
            "match_format": self._mf_combo.currentText(),
            "seeding":      self._seed_combo.currentText(),
        })


# ── Sidebar item ──────────────────────────────────────────────────────────────

class _TourneyItem(QFrame):
    clicked          = Signal(str)
    delete_requested = Signal(str)

    def __init__(self, t: dict, parent=None):
        super().__init__(parent)
        self._id       = t["id"]
        self._selected = False
        self.setFixedHeight(62)
        self.setCursor(Qt.PointingHandCursor)

        self._ss_n = "QFrame { background-color: transparent; border: none; border-radius: 6px; }"
        self._ss_h = f"QFrame {{ background-color: {_rgba(COLORS['bg_light'], 200)}; border: none; border-radius: 6px; }}"
        self._ss_s = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 28)}; border-left: 3px solid {COLORS['accent_primary']}; border-radius: 6px; }}"
        self.setStyleSheet(self._ss_n)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 8, 10, 8)
        outer.setSpacing(3)

        # Row 1: name + delete button
        r1 = QHBoxLayout()
        r1.setSpacing(6)

        self._name_lbl = QLabel(t["name"])
        self._name_lbl.setMinimumWidth(0)
        self._name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['text_primary']}; background: transparent;")
        r1.addWidget(self._name_lbl, stretch=1)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(22, 22)
        del_btn.setStyleSheet(f"""
            QPushButton {{
                background: {_rgba(COLORS['accent_danger'], 35)};
                border: 1px solid {_rgba(COLORS['accent_danger'], 100)};
                color: {COLORS['accent_danger']}; font-size: 11px;
                font-weight: bold; border-radius: 5px;
            }}
            QPushButton:hover {{
                background: {COLORS['accent_danger']}; color: white;
                border-color: {COLORS['accent_danger']};
            }}
        """)
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self._id))
        r1.addWidget(del_btn)
        outer.addLayout(r1)

        # Row 2: subtitle + status pill
        r2 = QHBoxLayout()
        r2.setSpacing(8)

        date = t.get("created", "")
        sub_lbl = QLabel(f"{t['format']}  ·  {t['teams_count']} teams" + (f"  ·  {date}" if date else ""))
        sub_lbl.setMinimumWidth(0)
        sub_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        r2.addWidget(sub_lbl, stretch=1)

        status = t["status"]
        tc, bc = _STATUS_STYLE.get(status, ("#aaa", "#222"))
        status_text = {"setup": "SETUP", "active": "ACTIVE", "complete": "COMPLETE"}.get(status, status.upper())
        pill = QLabel(status_text)
        pill.setFixedWidth(70)
        pill.setAlignment(Qt.AlignCenter)
        pill.setStyleSheet(f"""
            font-size: 9px; font-weight: bold; letter-spacing: 0.6px;
            color: {tc}; background-color: {_rgba(bc, 255)};
            padding: 2px 0; border-radius: 8px;
        """)
        r2.addWidget(pill)
        outer.addLayout(r2)

        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    @property
    def tourney_id(self): return self._id

    def set_selected(self, sel: bool):
        self._selected = sel
        self.setStyleSheet(self._ss_s if sel else self._ss_n)

    def enterEvent(self, _e):
        if not self._selected: self.setStyleSheet(self._ss_h)

    def leaveEvent(self, _e):
        if not self._selected: self.setStyleSheet(self._ss_n)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit(self._id)


# ── Main tournament tab ───────────────────────────────────────────────────────

class TournamentTab(QWidget):
    # Signals wired by MainWindow to the PlayerFinderWidget during active drafts
    draft_excluded_updated = Signal(set)   # forward to player_finder.set_draft_excluded
    slot_filter_changed    = Signal(str)   # forward to player_finder.set_slot_archetype

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data:         list                      = list(_FILLER)
        self._sel_id:       Optional[str]             = None
        self._t_items:      list                      = []
        self._active_draft: Optional[_DraftPhaseView] = None
        self._build_ui()
        self._populate_sidebar()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        lo.addWidget(self._build_sidebar())
        self._main = QStackedWidget()
        self._main.addWidget(self._empty_state())
        lo.addWidget(self._main, stretch=1)

    def _build_sidebar(self) -> QFrame:
        side = QFrame()
        side.setFixedWidth(320)
        side.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-right: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QVBoxLayout(side)
        lo.setContentsMargins(10, 16, 10, 12)
        lo.setSpacing(10)

        hdr = QLabel("TOURNAMENTS")
        hdr.setStyleSheet(f"font-size: 10px; font-weight: bold; letter-spacing: 1.5px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(hdr)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background-color: {COLORS['border_dark']}; border: none;")
        lo.addWidget(div)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._list_c = QWidget()
        self._list_c.setStyleSheet("background: transparent;")
        self._list_lo = QVBoxLayout(self._list_c)
        self._list_lo.setContentsMargins(0, 0, 0, 0)
        self._list_lo.setSpacing(3)
        self._list_lo.addStretch()

        scroll.setWidget(self._list_c)
        lo.addWidget(scroll, stretch=1)

        new_btn = QPushButton("+ New Tournament")
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_rgba(COLORS['accent_primary'], 40)};
                color: {COLORS['accent_primary']};
                border: 1px solid {_rgba(COLORS['accent_primary'], 80)};
                border-radius: 8px; font-size: 12px; font-weight: 600; padding: 9px 0;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_primary']}; color: white; }}
        """)
        new_btn.clicked.connect(self._on_new)
        lo.addWidget(new_btn)
        return side

    def _empty_state(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(w)
        lo.setAlignment(Qt.AlignCenter)
        lo.setSpacing(10)
        t = QLabel("Tournaments")
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        lo.addWidget(t)
        d = QLabel("Run brackets, draft rosters, and crown a champion.\n\nSelect a tournament or create a new one.")
        d.setAlignment(Qt.AlignCenter)
        d.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(d)
        return w

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _populate_sidebar(self):
        for item in self._t_items:
            self._list_lo.removeWidget(item)
            item.deleteLater()
        self._t_items.clear()

        for i, t in enumerate(self._data):
            item = _TourneyItem(t)
            item.clicked.connect(self._select)
            item.delete_requested.connect(self._on_delete)
            self._list_lo.insertWidget(i, item)
            self._t_items.append(item)

    # ── Content switching ─────────────────────────────────────────────────────

    def _swap(self, widget: QWidget):
        if self._main.count() > 1:
            old = self._main.widget(1)
            self._main.removeWidget(old)
            old.deleteLater()
        self._main.addWidget(widget)
        self._main.setCurrentIndex(1)

    def _select(self, t_id: str):
        self._sel_id = t_id
        for item in self._t_items:
            item.set_selected(item.tourney_id == t_id)
        t = next((x for x in self._data if x["id"] == t_id), None)
        if not t:
            return
        self._clear_active_draft()
        if t["status"] == "setup":
            view = _DraftPhaseView(t)
            view.begin_requested.connect(lambda: self._begin_tournament(t_id))
            view.draft_excluded_updated.connect(self.draft_excluded_updated)
            view.slot_filter_changed.connect(self.slot_filter_changed)
            self._active_draft = view
            self._swap(view)
        else:
            self._swap(_HubView(t))

    def _on_new(self):
        self._sel_id = None
        for item in self._t_items:
            item.set_selected(False)
        self._clear_active_draft()
        setup = _SetupView()
        setup.create_requested.connect(self._on_create)
        self._swap(setup)

    def _on_delete(self, t_id: str):
        if self._sel_id == t_id:
            self._clear_active_draft()
        self._data = [t for t in self._data if t["id"] != t_id]
        if self._sel_id == t_id:
            self._sel_id = None
            self._main.setCurrentIndex(0)
        self._populate_sidebar()

    def _clear_active_draft(self):
        """Stop tracking the active draft and reset sidebar state."""
        if self._active_draft is not None:
            self._active_draft = None
            self.draft_excluded_updated.emit(set())
            self.slot_filter_changed.emit("")

    def on_sidebar_pick(self, player):
        """Called by MainWindow when the user selects a player in the sidebar.
        Only acts when a draft view is visible and waiting for a Normal pick."""
        if self._active_draft is not None and self._active_draft.isVisible():
            self._active_draft.pick_from_sidebar(player)

    def _begin_tournament(self, t_id: str):
        t = next((x for x in self._data if x["id"] == t_id), None)
        if t:
            t["status"] = "active"
        self._populate_sidebar()
        self._select(t_id)

    def _on_create(self, cfg: dict):
        n     = cfg["teams_count"]
        teams = list(cfg["teams"])
        if cfg["seeding"] == "Random":
            random.shuffle(teams)

        rounds    = []
        cur_teams = teams
        while len(cur_teams) > 1:
            r = []
            for i in range(0, len(cur_teams), 2):
                r.append({
                    "team1": cur_teams[i],
                    "team2": cur_teams[i + 1] if i + 1 < len(cur_teams) else "TBD",
                    "score1": None, "score2": None, "winner": None,
                })
            rounds.append(r)
            cur_teams = ["TBD"] * (len(cur_teams) // 2)

        new_t = {
            "id":            uuid.uuid4().hex[:10],
            "name":          cfg["name"],
            "format":        cfg["format"],
            "teams_count":   n,
            "draft_mode":    cfg["draft_mode"],
            "match_format":  cfg["match_format"],
            "status":        "setup",
            "current_round": 0,
            "rounds":        rounds,
            "rosters":       {},
            "created":       "Just now",
        }
        self._data.insert(0, new_t)
        self._populate_sidebar()
        self._select(new_t["id"])
