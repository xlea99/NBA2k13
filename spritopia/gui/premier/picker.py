"""
Premier Mode Picker - Full Draft System.

Handles the complete pick/ban sequence for Premier games:
  Ban phase → Pick phase (per draft order config)
  Roll Pick animation for Random slots
  Archetype-locked slot enforcement
  Countdown timer with auto-pick on timeout
  Wild Card slot reveal
"""

import random
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer

from spritopia.gui.theme import COLORS, get_archetype_color
from spritopia.gui.app_state import get_app_state
from spritopia.gui.audio import get_audio_player
from spritopia.data_storage.data_storage import d


# ── Team identity (blue / red only) ───────────────────────────────────────────

TEAM_NAMES     = {1: "Danny",   2: "Alex"}
TEAM_SUBTITLES = {1: "Ballerz", 2: "Ringers"}
TEAM_COLORS    = {1: "#4a9eff", 2: "#ef4444"}   # blue / red


def _hex_rgba(hex_color: str, alpha: int) -> str:
    """Convert '#RRGGBB' + 0-255 alpha to 'rgba(r, g, b, alpha)' for QSS."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

RARITY_ORDER = ["Common", "Rare", "Epic", "Legendary", "Godlike"]

# Roll animation frame intervals (ms) — rapid then decelerating
_ROLL_SCHEDULE = [50]*10 + [70]*6 + [100]*4 + [150]*3 + [220]*3 + [350]*2 + [550]


# ── Draft Turn ─────────────────────────────────────────────────────────────────

@dataclass
class DraftTurn:
    team: int        # 1=Danny, 2=Alex, 0=System
    action: str      # "ban" | "random_ban" | "pick"
    pick_type: str   # "Normal" | "Random" | "Archetype (X)" | "ban"
    global_slot: int # 0..2N-1 for picks; -1 for bans
    is_auto: bool = False


# ── Turn Sequence Generator ────────────────────────────────────────────────────

def _generate_draft_turns(config: dict) -> tuple:
    N            = config["player_count"]
    draft_order  = config["draft_order"]
    bans_per_team = config.get("bans", 0)
    rand_bans    = config.get("random_bans", 0)
    pick_slots   = config.get("pick_slots", ["Normal"] * (2 * N))
    draft_lottery = config.get("draft_lottery", False)

    fp = config.get("first_pick", "Random")
    first  = 1 if fp == "Danny" else 2 if fp == "Alex" else random.choice([1, 2])
    second = 3 - first

    turns: List[DraftTurn] = []
    danny_idx = 0
    alex_idx  = 0

    def _ban(team):
        turns.append(DraftTurn(team=team, action="ban",
                               pick_type="ban", global_slot=-1))

    def _rbан():
        turns.append(DraftTurn(team=0, action="random_ban",
                               pick_type="random_ban", global_slot=-1, is_auto=True))

    def _pick(team):
        nonlocal danny_idx, alex_idx
        if team == 1:
            gs = danny_idx
            pt = pick_slots[danny_idx] if danny_idx < len(pick_slots) else "Normal"
            danny_idx += 1
        else:
            gs = N + alex_idx
            pt = pick_slots[N + alex_idx] if (N + alex_idx) < len(pick_slots) else "Normal"
            alex_idx += 1
        turns.append(DraftTurn(team=team, action="pick",
                               pick_type=pt, global_slot=gs))

    def alt_bans(n, ft):
        for i in range(n * 2):
            _ban(ft if i % 2 == 0 else 3 - ft)

    def alt_picks(n, ft):
        for i in range(n):
            _pick(ft if i % 2 == 0 else 3 - ft)

    def snake_picks(total, ft):
        if total <= 0:
            return
        half = (total + 1) // 2
        rest = total - half
        if half <= 2:
            alt_picks(half, ft)
        else:
            _pick(ft)
            for _ in range(half - 2):
                _pick(3 - ft)
            _pick(ft)
        if rest <= 2:
            alt_picks(rest, 3 - ft)
        else:
            _pick(3 - ft)
            for _ in range(rest - 2):
                _pick(ft)
            _pick(3 - ft)

    if draft_order == "Classic":
        alt_bans(bans_per_team, first)
        for _ in range(rand_bans): _rbан()
        alt_picks(2 * N, first)
    elif draft_order == "Smite":
        h1b, h2b = bans_per_team // 2, bans_per_team - bans_per_team // 2
        h1r, h2r = rand_bans // 2, rand_bans - rand_bans // 2
        alt_bans(h1b, first)
        for _ in range(h1r): _rbан()
        snake_picks(N, first)
        alt_bans(h2b, second)
        for _ in range(h2r): _rbан()
        snake_picks(N, second)
    elif draft_order == "Danny-First":
        alt_bans(bans_per_team, first)
        for _ in range(rand_bans): _rbан()
        for _ in range(N): _pick(1)
        for _ in range(N): _pick(2)
    elif draft_order == "Alex-First":
        alt_bans(bans_per_team, first)
        for _ in range(rand_bans): _rbан()
        for _ in range(N): _pick(2)
        for _ in range(N): _pick(1)
    elif draft_order == "2-4-2":
        alt_bans(bans_per_team, first)
        for _ in range(rand_bans): _rbан()
        seg1 = min(2, N); seg3 = min(2, N); seg2 = max(0, 2*N - seg1 - seg3)
        for _ in range(seg1): _pick(1)
        for _ in range(seg2): _pick(2)
        for _ in range(seg3): _pick(1)
    else:
        alt_bans(bans_per_team, first)
        for _ in range(rand_bans): _rbан()
        alt_picks(2 * N, first)

    if draft_lottery:
        idxs = [i for i, t in enumerate(turns) if t.action == "pick"]
        teams = [turns[i].team for i in idxs]; random.shuffle(teams)
        d1 = d2 = 0
        for pos, i in enumerate(idxs):
            t = teams[pos]
            if t == 1:
                turns[i].team = 1; turns[i].global_slot = d1
                pt_i = d1; turns[i].pick_type = pick_slots[pt_i] if pt_i < len(pick_slots) else "Normal"; d1 += 1
            else:
                turns[i].team = 2; turns[i].global_slot = N + d2
                pt_i = N + d2; turns[i].pick_type = pick_slots[pt_i] if pt_i < len(pick_slots) else "Normal"; d2 += 1

    return turns, first


# ── Player Pool Helper ─────────────────────────────────────────────────────────

def _arch_from_type(pick_type: str) -> str:
    """Extract archetype name from 'Archetype (Slayer)'; '' if not specific."""
    if pick_type.startswith("Archetype (") and pick_type != "Archetype (Random)":
        return pick_type[len("Archetype ("):-1]
    return ""


def _player_stat_scores(player) -> list:
    """Returns [(label, score), ...] for 6 composite stats (0-99 scale)."""
    def r(key):
        try:
            return int(player[key] or 0)
        except Exception:
            return 0
    return [
        ("ATH",    (r("SSpeed") + r("SVertical") + r("SStrength") + r("SQuick")) // 4),
        ("OFF",    (r("SShtCls") + r("SSht3PT") + r("SLayUp") + r("SDunk")) // 4),
        ("BALL",   (r("SBallHndl") + r("SPass") + r("SOffHDrib")) // 3),
        ("DEF",    (r("SBlock") + r("SSteal") + r("SOnBallD") + r("SDReb")) // 4),
        ("IQ",     (r("SOAwar") + r("SDAwar") + r("SConsis")) // 3),
        ("CLT",    (r("SPOT") + r("SHustle")) // 2),
    ]


# ── Archetype stat definitions & percentile card builder ──────────────────────

_ARCH_STAT_DEFS: Dict[str, list] = {
    "Slayer":    [("PPG",  "ppg"),        ("3PT%", "three_pt_pct"), ("TS%",  "ts_pct"),
                  ("3PTR", "three_pt_rate"), ("PCG", "points_created_per_game"), ("FG%", "fg_pct")],
    "Vigilante": [("PPG",  "ppg"),        ("DPG",  "dpg"),          ("D%",   "dunk_rate"),
                  ("TS%",  "ts_pct"),     ("RPG",  "rpg"),          ("PCG",  "points_created_per_game")],
    "Medic":     [("APG",  "apg"),        ("A/TO", "ast_to_ratio"), ("PCG",  "points_created_per_game"),
                  ("RPG",  "rpg"),        ("WIN",  "win_pct"),      ("PPG",  "ppg")],
    "Guardian":  [("BPG",  "bpg"),        ("SPG",  "spg"),          ("RPG",  "rpg"),
                  ("DRB",  "drpg"),       ("WIN",  "win_pct"),      ("EFF",  "efficiency_rating")],
    "Engineer":  [("APG",  "apg"),        ("A/TO", "ast_to_ratio"), ("BALL", "ball_time_per_game"),
                  ("PCG",  "points_created_per_game"), ("TS%", "ts_pct"), ("WIN", "win_pct")],
    "Director":  [("EFF",  "efficiency_rating"), ("GSC", "game_score_avg"), ("WIN", "win_pct"),
                  ("PPG",  "ppg"),        ("APG",  "apg"),          ("RPG",  "rpg")],
}

_DEFAULT_STAT_DEFS = [
    ("PPG", "ppg"), ("APG", "apg"), ("RPG", "rpg"),
    ("EFF", "efficiency_rating"), ("TS%", "ts_pct"), ("WIN", "win_pct"),
]


def _build_stat_cards(all_career_stats: list) -> dict:
    """
    Build percentile stat cards: {sprite_id: [(label, score_or_None), ...]}
    score is 0-99 percentile rank within archetype peers with >= 1 game.
    None means the player has no game data yet.
    """
    # Build archetype groups — only players with >= 1 game count for percentile calc
    arch_groups: Dict[str, list] = {}
    for cs in all_career_stats:
        arch = (cs.archetype or "").strip()
        if cs.games_played >= 1:
            arch_groups.setdefault(arch, []).append(cs)

    cards: Dict[int, list] = {}
    for cs in all_career_stats:
        arch = (cs.archetype or "").strip()
        stat_defs = _ARCH_STAT_DEFS.get(arch, _DEFAULT_STAT_DEFS)
        peers = arch_groups.get(arch, [])
        pill_data = []
        for label, attr in stat_defs:
            if cs.games_played < 1:
                pill_data.append((label, None))
                continue
            val = getattr(cs, attr, 0) or 0
            if len(peers) <= 1:
                score = 50
            else:
                below = sum(1 for p in peers if (getattr(p, attr, 0) or 0) < val)
                score = round(below / (len(peers) - 1) * 99)
            pill_data.append((label, score))
        cards[cs.sprite_id] = pill_data

    return cards


def _build_pick_slot_stats(all_career_stats: list) -> dict:
    """
    Build compact stat lines for filled pick slots.
    Returns {sprite_id: [(label, value_str), ...]}
    Uses actual stat values (not percentile ranks).
    """
    total_games = max((cs.games_played for cs in all_career_stats if cs.games_played), default=1)

    def _pct(val) -> str:
        if not val: return "—"
        return f"{float(val) * 100:.0f}%"

    def _num(val, dec: int = 1) -> str:
        if val is None: return "—"
        return f"{float(val):.{dec}f}"

    result: Dict[int, list] = {}
    for cs in all_career_stats:
        if cs.games_played < 1:
            result[cs.sprite_id] = []
            continue

        arch = (cs.archetype or "").strip()
        pick_rate = f"{cs.games_played / total_games * 100:.0f}%"

        stats = [
            ("PR",   pick_rate),
            ("WIN",  _pct(cs.win_pct)),
            ("PPG",  _num(cs.ppg)),
            ("3PT",  _pct(cs.three_pt_pct)),
            ("RPG",  _num(cs.rpg)),
            ("STL",  _num(cs.spg)),
        ]

        # One arch-specific extra stat
        if arch == "Slayer":
            stats.append(("TS%",  _pct(cs.ts_pct)))
        elif arch == "Vigilante":
            stats.append(("DPG",  _num(cs.dpg)))
        elif arch in ("Medic", "Engineer"):
            stats.append(("APG",  _num(cs.apg)))
        elif arch == "Guardian":
            stats.append(("BPG",  _num(cs.bpg)))
        elif arch == "Director":
            stats.append(("EFF",  _num(cs.efficiency_rating)))

        result[cs.sprite_id] = stats

    return result


def _get_pool(config: dict, picked_ids: set, banned_ids: set,
              arch_filter: str = "", eligible_ids: Optional[set] = None) -> list:
    rarity_cap = config.get("rarity_cap")
    allowed_rarities = None
    if rarity_cap and rarity_cap in RARITY_ORDER:
        allowed_rarities = set(RARITY_ORDER[:RARITY_ORDER.index(rarity_cap) + 1])

    pool = []
    for sid, player in d.players.items():
        if sid in picked_ids or sid in banned_ids:
            continue
        if eligible_ids is not None and sid not in eligible_ids:
            continue
        if allowed_rarities and (player["Rarity"] or "Common") not in allowed_rarities:
            continue
        if arch_filter:
            if (player["Archetype_Name"] or "").lower() != arch_filter.lower():
                continue
        pool.append(player)
    return pool


# ── Timeline ───────────────────────────────────────────────────────────────────

class _TurnChip(QFrame):
    def __init__(self, turn: DraftTurn, label: str, parent=None):
        super().__init__(parent)
        self._turn = turn
        self.setFixedSize(34, 34)
        self._lbl = QLabel(label, self)
        self._lbl.setAlignment(Qt.AlignCenter)
        self._lbl.setGeometry(0, 0, 34, 34)
        self.set_state("upcoming")

    def set_state(self, state: str):
        if self._turn.team == 0:
            team_color = COLORS["accent_warning"]
        else:
            team_color = TEAM_COLORS.get(self._turn.team, COLORS["accent_primary"])

        if state == "done":
            bg, border, fg, size = COLORS["bg_light"], COLORS["border_dark"], COLORS["text_muted"], "9px"
        elif state == "active":
            bg, border, fg, size = team_color, team_color, "#ffffff", "11px"
        else:
            # Upcoming: solid dark variant of the team color so it reads clearly
            if self._turn.team == 1:
                bg, border = "#1e3355", "#2d4f80"
            elif self._turn.team == 2:
                bg, border = "#3d1515", "#6e2222"
            else:
                bg, border = "#3d2e10", "#6e5222"
            fg, size = COLORS["text_muted"], "10px"

        self.setStyleSheet(f"""
            QFrame {{ background-color: {bg}; border: 1px solid {border}; border-radius: 5px; }}
        """)
        self._lbl.setStyleSheet(f"font-size: {size}; font-weight: bold; color: {fg};")


class TimelineWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._chips: List[_TurnChip] = []
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        lo = QVBoxLayout(self)
        lo.setContentsMargins(12, 6, 12, 6)
        lo.setSpacing(4)

        hdr = QLabel("DRAFT ORDER")
        hdr.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {COLORS['text_muted']}; letter-spacing: 1px;")
        lo.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.setFixedHeight(46)

        self._chip_w = QWidget()
        self._chip_w.setStyleSheet("background: transparent;")
        self._row = QHBoxLayout(self._chip_w)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(4)
        self._row.addStretch()

        scroll.setWidget(self._chip_w)
        lo.addWidget(scroll)

    def load(self, turns: List[DraftTurn]):
        while self._row.count():
            item = self._row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._chips.clear()

        pick_nums = {1: 0, 2: 0}
        for turn in turns:
            if turn.action == "random_ban":
                label = "RB"
            elif turn.action == "ban":
                label = "B"
            else:
                pick_nums[turn.team] += 1
                label = str(pick_nums[turn.team])
            chip = _TurnChip(turn, label)
            self._chips.append(chip)
            self._row.addWidget(chip)
        self._row.addStretch()

    def highlight(self, idx: int):
        for i, chip in enumerate(self._chips):
            chip.set_state("done" if i < idx else "active" if i == idx else "upcoming")


# ── Team Draft Panel ───────────────────────────────────────────────────────────

class _DraftSlot(QFrame):
    def __init__(self, num: int, team: int, parent=None):
        super().__init__(parent)
        self._num = num
        self._team = team
        self._player = None
        self._is_active: bool = False
        self._active_pick_type: str = ""
        self._stat_data: dict = {}
        self.setFixedHeight(90)
        self.setStyleSheet("QFrame { border: none; background: transparent; }")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._lo = QVBoxLayout(self)
        self._lo.setContentsMargins(0, 0, 0, 0)
        self._show_empty()

    def _clear(self):
        while self._lo.count():
            item = self._lo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_empty(self, active: bool = False, pick_type: str = ""):
        self._clear()
        tc = TEAM_COLORS[self._team]
        if active:
            style = (f"background-color: {_hex_rgba(tc, 45)}; "
                     f"border: 1px solid {_hex_rgba(tc, 150)}; border-radius: 6px;")
        else:
            style = f"background-color: {COLORS['bg_light']}; border: 1px solid {COLORS['border_dark']}; border-radius: 6px;"

        c = QFrame()
        c.setStyleSheet(f"QFrame {{ {style} }}")
        row = QHBoxLayout(c)
        row.setContentsMargins(10, 0, 10, 0)

        lbl = QLabel(f"Pick {self._num}")
        lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        row.addWidget(lbl)

        if active and pick_type and pick_type not in ("Normal",):
            row.addStretch()
            if pick_type == "Random":
                tag_text = "RANDOM"
            elif pick_type == "Choice":
                tag_text = "2-WAY"
            elif pick_type == "Choice 3":
                tag_text = "3-WAY"
            elif pick_type == "Archetype (Random)":
                tag_text = "ANY ARCH"
            elif pick_type.startswith("Archetype ("):
                tag_text = _arch_from_type(pick_type).upper()
            else:
                tag_text = ""
            if tag_text:
                tag = QLabel(tag_text)
                tag.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {tc}; padding: 1px 5px;")
                row.addWidget(tag)

        self._lo.addWidget(c)

    def fill(self, player, wild_card: bool = False):
        self._clear()
        self._player = player

        tc = TEAM_COLORS[self._team]
        arch = str(player["Archetype_Name"] or "")
        arch_color = get_archetype_color(arch) if arch else tc
        first = player["First_Name"] or ""
        last  = player["Last_Name"] or ""
        name  = (f"★ " if wild_card else "") + (f"{first} {last}".strip() or "Unknown")

        c = QFrame()
        c.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-left: 3px solid {arch_color};
                border-radius: 6px;
            }}
        """)
        lo = QVBoxLayout(c)
        lo.setContentsMargins(10, 10, 10, 8)
        lo.setSpacing(5)

        # Row 1: player name + optional WILD badge
        name_row = QHBoxLayout()
        name_row.setSpacing(6)
        n_lbl = QLabel(name)
        n_lbl.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {COLORS['text_primary']};")
        name_row.addWidget(n_lbl, stretch=1)
        if wild_card:
            wc = QLabel("WILD")
            wc.setStyleSheet(f"""
                font-size: 8px; font-weight: bold;
                color: {COLORS['accent_warning']};
                background-color: {_hex_rgba(COLORS['accent_warning'], 34)};
                padding: 1px 4px; border-radius: 3px;
            """)
            name_row.addWidget(wc)
        lo.addLayout(name_row)

        # Row 2: archetype
        a_lbl = QLabel(arch or "—")
        a_lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {arch_color};")
        lo.addWidget(a_lbl)

        # Row 3: game stats
        slot_stats = self._stat_data.get(player["SpriteID"], [])
        if slot_stats:
            stat_row = QHBoxLayout()
            stat_row.setSpacing(12)
            stat_row.setContentsMargins(0, 0, 0, 0)
            for label, val_str in slot_stats:
                s_lbl = QLabel(f"{label} {val_str}")
                s_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")
                stat_row.addWidget(s_lbl)
            stat_row.addStretch()
            lo.addLayout(stat_row)

        self._lo.addWidget(c)

    def fill_slam(self, player, wild_card: bool = False):
        """Fill the slot then flash a bright slam effect that settles to normal."""
        self.fill(player, wild_card)
        tc = TEAM_COLORS[self._team]
        arch = str(player["Archetype_Name"] or "")
        arch_color = get_archetype_color(arch) if arch else tc
        inner = self._lo.itemAt(0)
        if not inner or not inner.widget():
            return
        w = inner.widget()
        # Stage 1: bright flash
        w.setStyleSheet(f"""
            QFrame {{
                background-color: {_hex_rgba(tc, 85)};
                border: 2px solid {tc};
                border-left: 4px solid {arch_color};
                border-radius: 6px;
            }}
        """)
        # Stage 2: settle to normal after 260ms
        normal = f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border_dark']};
                border-left: 3px solid {arch_color};
                border-radius: 6px;
            }}
        """
        QTimer.singleShot(260, lambda: w.setStyleSheet(normal) if w and not w.isHidden() else None)

    def preview(self, player):
        """Ghost-preview a pending player in this slot (not yet confirmed)."""
        if self._player:
            return  # Already filled — don't override
        self._clear()
        tc = TEAM_COLORS[self._team]
        arch = str(player["Archetype_Name"] or "")
        arch_color = get_archetype_color(arch) if arch else tc
        first = player["First_Name"] or ""
        last  = player["Last_Name"]  or ""

        c = QFrame()
        c.setStyleSheet(f"""
            QFrame {{
                background-color: {_hex_rgba(tc, 35)};
                border: 1px dashed {_hex_rgba(tc, 150)};
                border-left: 3px solid {_hex_rgba(arch_color, 150)};
                border-radius: 6px;
            }}
        """)
        lo = QVBoxLayout(c)
        lo.setContentsMargins(10, 10, 10, 8)
        lo.setSpacing(5)

        # Row 1: name + "selecting…" hint
        name_row = QHBoxLayout()
        name_row.setSpacing(6)
        n_lbl = QLabel(f"{first} {last}".strip() or "Unknown")
        n_lbl.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {_hex_rgba(COLORS['text_primary'], 160)};")
        name_row.addWidget(n_lbl, stretch=1)
        hint = QLabel("selecting…")
        hint.setStyleSheet(f"font-size: 9px; color: {_hex_rgba(tc, 200)}; font-style: italic;")
        name_row.addWidget(hint)
        lo.addLayout(name_row)

        # Row 2: archetype
        a_lbl = QLabel(arch or "—")
        a_lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {_hex_rgba(arch_color, 150)};")
        lo.addWidget(a_lbl)

        # Row 3: game stats (ghost alpha)
        slot_stats = self._stat_data.get(player["SpriteID"], [])
        if slot_stats:
            stat_row = QHBoxLayout()
            stat_row.setSpacing(12)
            stat_row.setContentsMargins(0, 0, 0, 0)
            for label, val_str in slot_stats:
                s_lbl = QLabel(f"{label} {val_str}")
                s_lbl.setStyleSheet(f"font-size: 11px; color: {_hex_rgba(COLORS['text_secondary'], 120)};")
                stat_row.addWidget(s_lbl)
            stat_row.addStretch()
            lo.addLayout(stat_row)

        self._lo.addWidget(c)

    def clear_preview(self):
        """Remove ghost preview — return to active empty state."""
        if not self._player:
            self._show_empty(active=self._is_active, pick_type=self._active_pick_type)

    def set_active(self, pick_type: str = ""):
        self._is_active = True
        self._active_pick_type = pick_type
        self._show_empty(active=True, pick_type=pick_type)

    def set_inactive(self):
        self._is_active = False
        self._active_pick_type = ""
        if not self._player:
            self._show_empty()

    def set_stat_data(self, stats: dict):
        self._stat_data = stats


class TeamDraftPanel(QFrame):
    def __init__(self, team: int, n: int, parent=None):
        super().__init__(parent)
        self._team = team
        self._slots: List[_DraftSlot] = []
        tc = TEAM_COLORS[team]
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-top: 3px solid {tc};
                border-radius: 10px;
            }}
        """)
        lo = QVBoxLayout(self)
        lo.setContentsMargins(14, 12, 14, 12)
        lo.setSpacing(6)

        # Header
        row = QHBoxLayout()
        name_lbl = QLabel(TEAM_NAMES[team])
        name_lbl.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {tc};")
        row.addWidget(name_lbl)
        row.addStretch()
        sub = QLabel(TEAM_SUBTITLES[team])
        sub.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        row.addWidget(sub)
        lo.addLayout(row)

        for i in range(n):
            slot = _DraftSlot(i + 1, team)
            self._slots.append(slot)
            lo.addWidget(slot)

        lo.addStretch()

    def activate_slot(self, team_slot: int, pick_type: str):
        for i, s in enumerate(self._slots):
            if i == team_slot:
                s.set_active(pick_type)
            else:
                s.set_inactive()

    def deactivate_all(self):
        for s in self._slots:
            s.set_inactive()

    def fill_slot(self, team_slot: int, player, wild_card: bool = False):
        if 0 <= team_slot < len(self._slots):
            self._slots[team_slot].fill(player, wild_card=wild_card)

    def fill_slot_slam(self, team_slot: int, player, wild_card: bool = False):
        if 0 <= team_slot < len(self._slots):
            self._slots[team_slot].fill_slam(player, wild_card=wild_card)

    def preview_slot(self, team_slot: int, player):
        if 0 <= team_slot < len(self._slots):
            self._slots[team_slot].preview(player)

    def clear_slot_preview(self, team_slot: int):
        if 0 <= team_slot < len(self._slots):
            self._slots[team_slot].clear_preview()

    def set_slot_stats(self, stats: dict):
        for slot in self._slots:
            slot.set_stat_data(stats)


# ── Ban Pool ───────────────────────────────────────────────────────────────────

class BanPoolWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(10, 8, 10, 8)
        lo.setSpacing(4)

        hdr = QLabel("BANNED")
        hdr.setStyleSheet(f"font-size: 8px; font-weight: bold; color: {COLORS['accent_danger']}; letter-spacing: 1px;")
        lo.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._list_w = QWidget()
        self._list_w.setStyleSheet("background: transparent;")
        self._list_lo = QVBoxLayout(self._list_w)
        self._list_lo.setContentsMargins(0, 0, 0, 0)
        self._list_lo.setSpacing(3)

        self._empty = QLabel("No bans yet")
        self._empty.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']}; font-style: italic;")
        self._list_lo.addWidget(self._empty)
        self._list_lo.addStretch()

        scroll.setWidget(self._list_w)
        lo.addWidget(scroll, stretch=1)

    def add_ban(self, player, is_auto: bool = False):
        if self._empty.isVisible():
            self._empty.hide()
        first = player["First_Name"] or ""
        last  = player["Last_Name"] or ""
        arch  = player["Archetype_Name"] or ""
        name  = f"{first} {last}".strip()
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 2, 0, 2)
        rl.setSpacing(6)

        dot = QLabel("●")
        dot.setStyleSheet(f"font-size: 9px; color: {COLORS['accent_danger']};")
        dot.setFixedWidth(12)
        rl.addWidget(dot)

        prefix = "⚙ " if is_auto else ""
        name_lbl = QLabel(f"{prefix}{name}")
        name_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_primary']}; font-weight: 500;")
        rl.addWidget(name_lbl, stretch=1)

        arch_lbl = QLabel(arch)
        arch_lbl.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']};")
        rl.addWidget(arch_lbl)

        # Insert before the trailing stretch (last item)
        self._list_lo.insertWidget(self._list_lo.count() - 1, row)

    def reset(self):
        while self._list_lo.count():
            item = self._list_lo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._empty = QLabel("No bans yet")
        self._empty.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']}; font-style: italic;")
        self._list_lo.addWidget(self._empty)
        self._list_lo.addStretch()


# ── Choice Card ────────────────────────────────────────────────────────────────

class _ChoiceCard(QFrame):
    """Clickable player card for Choice draft mode. Emits clicked(player) on press."""

    clicked = Signal(object)

    def __init__(self, player, stat_cards: dict, team: int, parent=None):
        super().__init__(parent)
        self._player = player
        tc         = TEAM_COLORS[team]
        arch       = str(player["Archetype_Name"] or "")
        arch_color = get_archetype_color(arch) if arch else tc
        first = player["First_Name"] or ""
        last  = player["Last_Name"]  or ""
        rar   = player["Rarity"] or "Common"

        self._normal_ss = f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 2px solid {COLORS['border_dark']};
                border-left: 4px solid {arch_color};
                border-radius: 8px;
            }}
        """
        self._hover_ss = f"""
            QFrame {{
                background-color: {_hex_rgba(tc, 35)};
                border: 2px solid {tc};
                border-left: 4px solid {arch_color};
                border-radius: 8px;
            }}
        """
        self._press_ss = f"""
            QFrame {{
                background-color: {_hex_rgba(tc, 70)};
                border: 2px solid {tc};
                border-left: 4px solid {arch_color};
                border-radius: 8px;
            }}
        """
        self.setStyleSheet(self._normal_ss)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(12, 10, 12, 10)
        lo.setSpacing(3)

        def _tlbl(text, style):
            l = QLabel(text)
            l.setStyleSheet(style)
            l.setAttribute(Qt.WA_TransparentForMouseEvents)
            return l

        lo.addWidget(_tlbl(
            f"{first} {last}".strip() or "Unknown",
            f"font-size: 13px; font-weight: 700; color: {COLORS['text_primary']};"
        ))
        lo.addWidget(_tlbl(
            f"{arch}  ·  {rar}",
            f"font-size: 10px; color: {COLORS['text_secondary']};"
        ))

        # Stat pills
        sid   = player["SpriteID"]
        pills = stat_cards.get(sid)
        if pills:
            pill_w = QWidget()
            pill_w.setAttribute(Qt.WA_TransparentForMouseEvents)
            pill_w.setStyleSheet("background: transparent;")
            pl = QHBoxLayout(pill_w)
            pl.setContentsMargins(0, 2, 0, 0)
            pl.setSpacing(6)
            for label, val in pills[:4]:
                if val is None:
                    vc, vt = COLORS["text_muted"], "—"
                elif val >= 75:
                    vc, vt = COLORS["accent_success"], str(val)
                elif val >= 45:
                    vc, vt = COLORS["accent_warning"], str(val)
                else:
                    vc, vt = COLORS["accent_danger"], str(val)
                pl_lbl = QLabel(f"{label} {vt}")
                pl_lbl.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {vc};")
                pl_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
                pl.addWidget(pl_lbl)
            pl.addStretch()
            lo.addWidget(pill_w)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setStyleSheet(self._press_ss)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setStyleSheet(self._hover_ss)
            self.clicked.emit(self._player)
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.setStyleSheet(self._hover_ss)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self._normal_ss)
        super().leaveEvent(event)


# ── Action Bar ─────────────────────────────────────────────────────────────────

class ActionBar(QFrame):
    """
    Context-sensitive bottom strip. Rebuilt on each turn.
    Manages roll pick animation and per-turn countdown display.
    """

    confirm_pick = Signal()
    confirm_ban  = Signal()
    roll_pick    = Signal()
    load_game    = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sel_lbl: Optional[QLabel]         = None
        self._confirm_btn: Optional[QPushButton] = None
        self._content: Optional[QWidget]         = None
        self._roll_timer = QTimer(self)
        self._roll_timer.timeout.connect(self._roll_tick)
        self._roll_pool: list = []
        self._roll_target = None
        self._roll_idx: int  = 0
        self._roll_cb = None
        self._stat_cards: dict = {}

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        self.setMinimumHeight(160)
        self.setMaximumHeight(200)
        self._outer = QVBoxLayout(self)
        self._outer.setContentsMargins(24, 0, 24, 0)
        self._outer.setSpacing(0)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _clear(self):
        if self._roll_timer.isActive():
            self._roll_timer.stop()
        if self._content:
            self._content.deleteLater()
            self._content = None
        # Reset tracked references so they're never stale
        self._sel_lbl     = None
        self._confirm_btn = None

    def set_stat_cards(self, cards: dict):
        """Store pre-built percentile stat cards for use in _rebuild_stats."""
        self._stat_cards = cards

    def _add(self, widget: QWidget):
        self._content = widget
        self._outer.addWidget(widget, stretch=1)

    def _btn(self, text: str, color: str, slot) -> QPushButton:
        b = QPushButton(text)
        b.setFixedHeight(38)
        b.setMinimumWidth(130)
        b.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; color: white;
                border: none; border-radius: 6px;
                font-size: 13px; font-weight: bold; padding: 0 18px;
            }}
            QPushButton:hover    {{ background-color: {_hex_rgba(color, 204)}; }}
            QPushButton:pressed  {{ background-color: {_hex_rgba(color, 153)}; }}
            QPushButton:disabled {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_muted']};
            }}
        """)
        b.clicked.connect(slot)
        return b

    # ── Public API ────────────────────────────────────────────────────────────

    def show_turn(self, turn: DraftTurn, pending_player=None, time_limit: Optional[int] = None):
        self._clear()

        tc = TEAM_COLORS.get(turn.team, COLORS["accent_warning"]) if turn.team != 0 else COLORS["accent_warning"]

        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 10, 0, 8)
        lo.setSpacing(6)

        # ── Row 1: who / type ─────────────────────────────────────────────────
        top = QHBoxLayout()
        top.setSpacing(8)

        if turn.team == 0:
            whose = "SYSTEM"
        else:
            whose = f"{TEAM_NAMES[turn.team].upper()}'S TURN"
        whose_lbl = QLabel(whose)
        whose_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {tc};")
        top.addWidget(whose_lbl)

        sep = QLabel("·")
        sep.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
        top.addWidget(sep)

        if turn.action in ("ban", "random_ban"):
            type_text  = "BAN"
            type_color = COLORS["accent_danger"]
        elif turn.pick_type == "Random":
            type_text  = "RANDOM PICK"
            type_color = tc
        elif turn.pick_type.startswith("Archetype ("):
            arch = _arch_from_type(turn.pick_type)
            type_text  = f"{arch.upper()} PICK" if arch else "ARCHETYPE PICK"
            type_color = tc
        elif turn.pick_type in ("Choice", "Choice 3"):
            n = 2 if turn.pick_type == "Choice" else 3
            type_text  = f"{n}-WAY CHOICE"
            type_color = tc
        else:
            type_text  = "PICK"
            type_color = tc

        type_lbl = QLabel(type_text)
        type_lbl.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {type_color};")
        top.addWidget(type_lbl)
        top.addStretch()
        lo.addLayout(top)

        # ── Row 2: selection area + button ────────────────────────────────────
        bot = QHBoxLayout()
        bot.setSpacing(16)

        if turn.action == "random_ban":
            lbl = QLabel("Selecting a random player to ban…")
            lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-style: italic;")
            bot.addWidget(lbl, stretch=1)

        elif turn.pick_type == "Random":
            lbl = QLabel("Press Roll — destiny picks your player.")
            lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-style: italic;")
            bot.addWidget(lbl, stretch=1)
            roll_btn = self._btn("🎲  Roll Pick", tc, self.roll_pick)
            bot.addWidget(roll_btn)

        elif turn.action == "ban":
            info_col = QVBoxLayout()
            info_col.setSpacing(6)
            self._sel_lbl = QLabel("← Select a player on the left to ban")
            self._sel_lbl.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
            info_col.addWidget(self._sel_lbl)
            bot.addLayout(info_col, stretch=1)
            btn = self._btn("Confirm Ban", COLORS["accent_danger"], self.confirm_ban)
            btn.setEnabled(pending_player is not None)
            self._confirm_btn = btn
            bot.addWidget(btn)

        else:  # Normal / Archetype pick
            info_col = QVBoxLayout()
            info_col.setSpacing(6)
            self._sel_lbl = QLabel("← Select a player on the left to pick")
            self._sel_lbl.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
            info_col.addWidget(self._sel_lbl)
            bot.addLayout(info_col, stretch=1)
            btn = self._btn("Confirm Pick", tc, self.confirm_pick)
            btn.setEnabled(pending_player is not None)
            self._confirm_btn = btn
            bot.addWidget(btn)

        if pending_player and self._sel_lbl:
            self._update_sel_label(pending_player)

        lo.addLayout(bot, stretch=1)
        self._add(w)

    def show_choice(self, players: list, turn: "DraftTurn", on_pick):
        """Display N clickable choice cards for a Choice-mode pick turn."""
        self._clear()
        tc = TEAM_COLORS.get(turn.team, COLORS["accent_warning"])
        n  = len(players)

        w  = QWidget()
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 10, 0, 8)
        lo.setSpacing(6)

        # Row 1: who / type label
        top = QHBoxLayout()
        top.setSpacing(8)
        whose_lbl = QLabel(f"{TEAM_NAMES[turn.team].upper()}'S TURN")
        whose_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {tc};")
        top.addWidget(whose_lbl)
        sep = QLabel("·")
        sep.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
        top.addWidget(sep)
        type_lbl = QLabel(f"{n}-WAY CHOICE")
        type_lbl.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {tc};")
        top.addWidget(type_lbl)
        top.addStretch()
        lo.addLayout(top)

        # Row 2: clickable cards side by side
        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)
        for player in players:
            card = _ChoiceCard(player, self._stat_cards, turn.team)
            card.clicked.connect(on_pick)
            cards_row.addWidget(card)
        cards_row.addStretch()
        lo.addLayout(cards_row, stretch=1)

        self._add(w)

    def update_selection(self, player):
        if self._sel_lbl is not None:
            self._update_sel_label(player)
        if self._confirm_btn is not None:
            self._confirm_btn.setEnabled(player is not None)

    def _update_sel_label(self, player):
        if self._sel_lbl is None:
            return
        if not player:
            self._sel_lbl.setText("← Select a player on the left")
            self._sel_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; font-style: italic;")
            return
        first = player["First_Name"] or ""
        last  = player["Last_Name"]  or ""
        arch  = player["Archetype_Name"] or ""
        rar   = player["Rarity"] or ""
        arch_color = get_archetype_color(arch) if arch else COLORS["text_secondary"]
        rar_colors = {"Common": "#94a3b8", "Rare": "#60a5fa", "Epic": "#c084fc",
                      "Legendary": "#fbbf24", "Godlike": "#f87171"}
        rar_color = rar_colors.get(rar, COLORS["text_secondary"])
        self._sel_lbl.setText(
            f'<span style="font-size:15px; font-weight:700; color:{COLORS["text_primary"]}">'
            f'{first} {last}</span>'
            f'  <span style="font-size:12px; color:{arch_color}">{arch}</span>'
            f'  <span style="font-size:11px; color:{rar_color}">· {rar}</span>'
        )
        self._sel_lbl.setTextFormat(Qt.RichText)

    def show_error(self, msg: str):
        if self._sel_lbl is not None:
            self._sel_lbl.setText(f"⚠  {msg}")
            self._sel_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['accent_danger']}; font-weight: 500;")
            QTimer.singleShot(2200, lambda: (
                self._update_sel_label(None) if self._sel_lbl and self._sel_lbl.text().startswith("⚠") else None
            ))

    # ── Roll animation ────────────────────────────────────────────────────────

    def show_roll(self, pool: list, target, on_complete):
        self._clear()
        self._roll_pool   = pool
        self._roll_target = target
        self._roll_idx    = 0
        self._roll_cb     = on_complete

        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 4, 0, 4)
        lo.setSpacing(2)

        top_lbl = QLabel("🎲  ROLLING…")
        top_lbl.setAlignment(Qt.AlignCenter)
        top_lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {COLORS['accent_warning']}; letter-spacing: 2px;")
        lo.addWidget(top_lbl)

        self._roll_name_lbl = QLabel("?????")
        self._roll_name_lbl.setAlignment(Qt.AlignCenter)
        self._roll_name_lbl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        lo.addWidget(self._roll_name_lbl)

        self._roll_sub_lbl = QLabel("")
        self._roll_sub_lbl.setAlignment(Qt.AlignCenter)
        self._roll_sub_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")
        lo.addWidget(self._roll_sub_lbl)

        self._add(w)
        self._roll_tick()

    def _roll_tick(self):
        if self._roll_idx >= len(_ROLL_SCHEDULE):
            self._roll_timer.stop()
            self._show_roll_result()
            return

        interval = _ROLL_SCHEDULE[self._roll_idx]
        candidate = self._roll_target if self._roll_idx >= len(_ROLL_SCHEDULE) - 3 else random.choice(self._roll_pool)

        if self._roll_name_lbl:
            first = candidate["First_Name"] or ""
            last  = candidate["Last_Name"] or ""
            self._roll_name_lbl.setText(f"{first} {last}".strip() or "???")
            arch = candidate["Archetype_Name"] or ""
            rar  = candidate["Rarity"] or ""
            self._roll_sub_lbl.setText(f"{arch}  ·  {rar}")

        self._roll_idx += 1
        self._roll_timer.start(interval)

    def _show_roll_result(self):
        p = self._roll_target
        if not p:
            return
        first = p["First_Name"] or ""
        last  = p["Last_Name"] or ""
        arch  = p["Archetype_Name"] or ""
        rar   = p["Rarity"] or ""

        self._clear()
        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 4, 0, 4)
        lo.setSpacing(2)

        top = QLabel("🎯  LOCKED IN")
        top.setAlignment(Qt.AlignCenter)
        top.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {COLORS['accent_warning']}; letter-spacing: 2px;")
        lo.addWidget(top)

        name_lbl = QLabel(f"{first} {last}".strip() or "???")
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_primary']};")
        lo.addWidget(name_lbl)

        sub = QLabel(f"{arch}  ·  {rar}")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")
        lo.addWidget(sub)

        self._add(w)
        cb = self._roll_cb
        QTimer.singleShot(1200, lambda: cb() if cb else None)

    # ── Draft complete ─────────────────────────────────────────────────────────

    def show_complete(self, has_wild_card: bool = False):
        self._clear()
        w = QWidget()
        lo = QHBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(16)

        msg_text = "🃏  Wild Card swaps applied — draft complete." if has_wild_card else "✓  Draft complete — all picks locked."
        msg = QLabel(msg_text)
        msg.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {COLORS['accent_success']};")
        lo.addWidget(msg, stretch=1)

        btn = QPushButton("Start Game  →")
        btn.setFixedHeight(40)
        btn.setMinimumWidth(150)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']}; color: white;
                border: none; border-radius: 6px;
                font-size: 14px; font-weight: bold; padding: 0 20px;
            }}
            QPushButton:hover   {{ background-color: #0ea572; }}
            QPushButton:pressed {{ background-color: #0b8a5a; }}
        """)
        btn.clicked.connect(self.load_game)
        lo.addWidget(btn)
        self._add(w)


# ── Premier Picker Widget ──────────────────────────────────────────────────────

class PremierPickerWidget(QWidget):
    load_requested      = Signal()
    slot_filter_changed = Signal(str)   # archetype name or "" to clear
    excluded_updated    = Signal(set)   # picked_ids | banned_ids after each pick/ban

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config: dict = {}
        self._turns: List[DraftTurn] = []
        self._current_idx: int = 0
        self._picks: Dict[int, Any] = {}
        self._banned_players: list = []
        self._banned_ids: set = set()
        self._picked_ids: set = set()
        self._pending: Any = None
        self._n: int = 4

        # Draft active flag — prevents stale async callbacks after backing out
        self._active: bool = False

        # Eligible player pool (computed at draft start)
        self._eligible_ids: Optional[set] = None   # None = all players eligible

        # Percentile stat cards: {sprite_id: [(label, score_or_None), ...]}
        self._stat_cards: dict = {}

        # Choice mode: players presented for the current pick turn
        self._choice_pool: list = []

        # Formatted stat lines for confirmed pick slots: {sprite_id: [(label, val_str), ...]}
        self._pick_slot_stats: dict = {}

        # Countdown timer state
        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._on_countdown_tick)
        self._time_remaining: int = 0

        # Sub-widgets (populated in start_draft)
        self._danny_panel:   Optional[TeamDraftPanel] = None
        self._alex_panel:    Optional[TeamDraftPanel] = None
        self._timeline:      Optional[TimelineWidget] = None
        self._ban_pool:      Optional[BanPoolWidget]  = None
        self._action_bar:    Optional[ActionBar]      = None
        self._body_widget:   Optional[QWidget]        = None
        self._timer_banner:  Optional[QLabel]         = None

        self._setup_shell()

    # ── Shell (persistent outer frame) ────────────────────────────────────────

    def _setup_shell(self):
        self._outer_lo = QVBoxLayout(self)
        self._outer_lo.setContentsMargins(0, 0, 0, 0)
        self._outer_lo.setSpacing(0)

        # Header bar
        hdr = QFrame()
        hdr.setFixedHeight(44)
        hdr.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20, 0, 20, 0)
        self._title_lbl = QLabel("Premier Draft")
        self._title_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['text_primary']};")
        hl.addWidget(self._title_lbl)
        hl.addStretch()
        self._mod_lbl = QLabel("")
        self._mod_lbl.setStyleSheet(f"font-size: 10px; color: {COLORS['text_muted']};")
        hl.addWidget(self._mod_lbl)
        self._outer_lo.addWidget(hdr)

        # Body placeholder
        self._placeholder = QLabel("Waiting for match to start…")
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 15px;")
        self._outer_lo.addWidget(self._placeholder, stretch=1)

        # Action bar (always at bottom)
        self._action_bar = ActionBar()
        self._action_bar.confirm_pick.connect(self._on_confirm_pick)
        self._action_bar.confirm_ban.connect(self._on_confirm_ban)
        self._action_bar.roll_pick.connect(self._on_roll_pick)
        self._action_bar.load_game.connect(self.load_requested)
        self._outer_lo.addWidget(self._action_bar)

    # ── Public API ─────────────────────────────────────────────────────────────

    def _build_eligible_pool(self):
        """
        Compute self._eligible_ids (Optional[set]) and pre-populate
        self._banned_ids with exile-mode pre-bans.
        Also builds self._stat_cards for percentile display in the action bar.
        """
        config = self._config
        RARITY_ORDER_L = ["Common", "Rare", "Epic", "Legendary", "Godlike"]
        player_set = config.get("player_set", "Standard")
        eligible: Optional[set] = None
        pre_banned: set = set()

        # Always load stats engine for Standard, veterans-only, or exile mode
        stats_engine = None
        if config.get("veterans_only") or config.get("exile_mode") or player_set == "Standard":
            try:
                if not hasattr(d, "stats") or not d.stats.get("Raw"):
                    d.statsDB_Open()
                    d.statsDB_DownloadRaw()
                raw_stats = d.stats.get("Raw", {})
                premier_raw = {
                    gid: ginfo for gid, ginfo in raw_stats.items()
                    if "Premier" in (ginfo.get("LoadedRoster") or "")
                }
                if premier_raw:
                    from spritopia.gui.stats.stats_engine import StatsEngine
                    stats_engine = StatsEngine(premier_raw, d.players)
            except Exception as e:
                print(f"[Picker] Stats engine load failed: {e}")

        # Build percentile stat cards (action bar) and slot stat lines (pick slots)
        if stats_engine:
            try:
                all_cs = stats_engine.get_all_career_stats()
                self._stat_cards      = _build_stat_cards(all_cs)
                self._pick_slot_stats = _build_pick_slot_stats(all_cs)
            except Exception as e:
                print(f"[Picker] Stat card build failed: {e}")
                self._stat_cards      = {}
                self._pick_slot_stats = {}
        else:
            self._stat_cards      = {}
            self._pick_slot_stats = {}

        # Standard player set: restrict pool to players with >= 1 Premier game
        if player_set == "Standard" and stats_engine and not config.get("veterans_only"):
            standard_ids = {
                cs.sprite_id
                for cs in stats_engine.get_all_career_stats()
                if cs.games_played >= 1
            }
            eligible = standard_ids if eligible is None else (eligible & standard_ids)

        if config.get("veterans_only") and stats_engine:
            eligible = {
                cs.sprite_id
                for cs in stats_engine.get_all_career_stats()
                if cs.games_played >= 20
            }

        rarity_cap = config.get("rarity_cap")
        if rarity_cap and rarity_cap in RARITY_ORDER_L:
            cap_idx = RARITY_ORDER_L.index(rarity_cap)
            allowed = set(RARITY_ORDER_L[:cap_idx + 1])
            rarity_ids = {
                p["SpriteID"] for p in d.players.values()
                if (p["Rarity"] or "Common") in allowed
            }
            eligible = rarity_ids if eligible is None else (eligible & rarity_ids)

        if config.get("exile_mode") and stats_engine:
            games = stats_engine.get_games()
            if games:
                for slot_info in games[0].player_slots.values():
                    if slot_info.get("IsActive"):
                        sid = slot_info.get("SpriteID", -1)
                        if sid is not None and sid >= 0:
                            pre_banned.add(sid)

        self._eligible_ids = eligible
        # Merge exile pre-bans into banned set (silently — don't show in ban pool)
        self._banned_ids = pre_banned.copy()

    def stop_draft(self):
        """Stop all timers and disable async callbacks (called when backing out)."""
        self._active = False
        self._countdown_timer.stop()
        if self._action_bar:
            self._action_bar._roll_timer.stop()
            self._action_bar._roll_cb = None

    def start_draft(self, config: dict):
        self._active  = True
        self._config  = config
        self._n       = config["player_count"]
        self._turns, _ = _generate_draft_turns(config)
        self._current_idx    = 0
        self._picks          = {}
        self._banned_players = []
        self._banned_ids     = set()
        self._picked_ids     = set()
        self._pending           = None
        self._choice_pool       = []
        self._pick_slot_stats   = {}

        self._build_eligible_pool()   # sets _eligible_ids, _stat_cards, _pick_slot_stats, pre-populates _banned_ids
        self._countdown_timer.stop()
        self._rebuild_body()
        self._update_header()
        self._action_bar.set_stat_cards(self._stat_cards)
        self._danny_panel.set_slot_stats(self._pick_slot_stats)
        self._alex_panel.set_slot_stats(self._pick_slot_stats)

        app_state = get_app_state()
        try:
            app_state.selected_player_changed.disconnect(self._on_sidebar_changed)
        except RuntimeError:
            pass
        app_state.selected_player_changed.connect(self._on_sidebar_changed)
        app_state.clear_all_picker_slots()

        if config.get("draft_content") == "Random Fast":
            self._fast_random_all()
        else:
            self._process_turn()

    def get_teams(self) -> tuple:
        danny = [self._picks[i] for i in range(self._n) if i in self._picks]
        alex  = [self._picks[self._n + i] for i in range(self._n) if (self._n + i) in self._picks]
        return danny, alex

    # ── Body rebuild ──────────────────────────────────────────────────────────

    def _rebuild_body(self):
        if self._placeholder:
            self._outer_lo.removeWidget(self._placeholder)
            self._placeholder.deleteLater()
            self._placeholder = None
        if self._body_widget:
            self._outer_lo.removeWidget(self._body_widget)
            self._body_widget.deleteLater()

        body = QWidget()
        lo = QVBoxLayout(body)
        lo.setContentsMargins(18, 14, 18, 10)
        lo.setSpacing(10)

        # Timeline
        self._timeline = TimelineWidget()
        self._timeline.load(self._turns)
        lo.addWidget(self._timeline)

        # Three columns: Danny | Middle (timer + bans) | Alex
        cols = QHBoxLayout()
        cols.setSpacing(14)

        self._danny_panel = TeamDraftPanel(team=1, n=self._n)
        cols.addWidget(self._danny_panel, stretch=1)

        # Middle column: big timer banner on top, ban pool below
        mid = QVBoxLayout()
        mid.setSpacing(8)
        mid.setContentsMargins(0, 0, 0, 0)

        self._timer_banner = QLabel("—")
        self._timer_banner.setAlignment(Qt.AlignCenter)
        self._timer_banner.setFixedHeight(80)
        self._timer_banner.setFixedWidth(160)
        self._timer_banner.setStyleSheet(f"""
            QLabel {{
                font-size: 48px;
                font-weight: bold;
                color: {COLORS['text_muted']};
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 10px;
            }}
        """)
        mid.addWidget(self._timer_banner)

        self._ban_pool = BanPoolWidget()
        mid.addWidget(self._ban_pool, stretch=1)

        cols.addLayout(mid)

        self._alex_panel = TeamDraftPanel(team=2, n=self._n)
        cols.addWidget(self._alex_panel, stretch=1)

        lo.addLayout(cols, stretch=1)

        self._body_widget = body
        self._outer_lo.insertWidget(self._outer_lo.count() - 1, body, stretch=1)

    def _update_header(self):
        c = self._config
        parts = [c.get("draft_content", "Normal"), c.get("draft_order", "Classic"),
                 c.get("player_set", "Standard"), f"{self._n}v{self._n}"]
        self._title_lbl.setText("  ·  ".join(parts))

        mods = []
        if c.get("rarity_cap"):     mods.append(f"Cap: {c['rarity_cap']}")
        if c.get("veterans_only"):  mods.append("Veterans Only")
        if c.get("exile_mode"):     mods.append("Exile")
        if c.get("archetype_mirror"): mods.append("Mirror")
        if c.get("wild_card_slot"): mods.append("Wild Card")
        if c.get("draft_lottery"):  mods.append("Lottery")
        self._mod_lbl.setText("  ·  ".join(mods))

    # ── Turn management ────────────────────────────────────────────────────────

    def _current_turn(self) -> Optional[DraftTurn]:
        if self._current_idx < len(self._turns):
            return self._turns[self._current_idx]
        return None

    def _set_timer_banner(self, seconds: Optional[int], team: int = 0):
        """Update the large central timer banner."""
        if self._timer_banner is None:
            return
        tc = TEAM_COLORS.get(team, COLORS["text_muted"]) if team != 0 else COLORS["accent_warning"]
        if seconds is None:
            self._timer_banner.setText("—")
            self._timer_banner.setStyleSheet(f"""
                QLabel {{
                    font-size: 48px; font-weight: bold;
                    color: {COLORS['text_muted']};
                    background-color: {COLORS['bg_medium']};
                    border: 1px solid {COLORS['border_dark']};
                    border-radius: 10px;
                }}
            """)
        else:
            if seconds <= 5:
                color = COLORS["accent_danger"]
            elif seconds <= 10:
                color = COLORS["accent_warning"]
            else:
                color = "#22c55e"  # Green — full time remaining
            self._timer_banner.setText(str(seconds))
            self._timer_banner.setStyleSheet(f"""
                QLabel {{
                    font-size: 48px; font-weight: bold;
                    color: {color};
                    background-color: {_hex_rgba(color, 24)};
                    border: 2px solid {_hex_rgba(color, 102)};
                    border-radius: 10px;
                }}
            """)

    def _process_turn(self):
        if not self._active:
            return
        self._countdown_timer.stop()
        turn = self._current_turn()
        if not turn:
            self._on_draft_complete()
            return

        self._timeline.highlight(self._current_idx)

        time_limit = self._config.get("pick_time")  # seconds or None

        # Activate correct team slot
        N = self._n
        if turn.action == "pick":
            arch = _arch_from_type(turn.pick_type)
            self.slot_filter_changed.emit(arch)
            if turn.team == 1:
                self._danny_panel.activate_slot(turn.global_slot, turn.pick_type)
                self._alex_panel.deactivate_all()
            else:
                self._alex_panel.activate_slot(turn.global_slot - N, turn.pick_type)
                self._danny_panel.deactivate_all()
        else:
            self.slot_filter_changed.emit("")
            self._danny_panel.deactivate_all()
            self._alex_panel.deactivate_all()

        # Auto-execute random bans
        if turn.action == "random_ban":
            self._set_timer_banner(None)
            QTimer.singleShot(800, self._auto_random_ban)
            return

        # Choice mode: draw N fresh random players and show clickable cards
        if turn.action == "pick" and turn.pick_type in ("Choice", "Choice 3"):
            n_choices = 2 if turn.pick_type == "Choice" else 3
            pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                             eligible_ids=self._eligible_ids)
            n_avail = min(n_choices, len(pool))
            self._choice_pool = random.sample(pool, n_avail) if n_avail > 0 else []
            if self._choice_pool:
                self._action_bar.show_choice(
                    self._choice_pool, turn,
                    lambda p: self._on_choice_pick(p, turn)
                )
                if time_limit:
                    self._time_remaining = time_limit
                    self._set_timer_banner(time_limit, turn.team)
                    self._countdown_timer.start()
                else:
                    self._set_timer_banner(None)
            else:
                self._set_timer_banner(None)
                QTimer.singleShot(300, self._advance)
            return

        self._action_bar.show_turn(turn, pending_player=self._pending, time_limit=time_limit)

        # Start countdown for human turns
        if time_limit:
            self._time_remaining = time_limit
            self._set_timer_banner(time_limit, turn.team)
            self._countdown_timer.start()
        else:
            self._set_timer_banner(None)

    def _advance(self):
        if not self._active:
            return
        self._countdown_timer.stop()
        self._set_timer_banner(None)
        self._pending = None
        self._current_idx += 1
        QTimer.singleShot(160, self._process_turn)

    # ── Countdown ─────────────────────────────────────────────────────────────

    def _on_countdown_tick(self):
        if not self._active:
            return
        self._time_remaining -= 1
        turn = self._current_turn()
        team = turn.team if turn else 0
        self._set_timer_banner(self._time_remaining, team)
        if self._time_remaining <= 0:
            self._countdown_timer.stop()
            self._auto_timeout()

    def _auto_timeout(self):
        """Time ran out — auto-execute the current turn."""
        turn = self._current_turn()
        if not turn:
            return
        if turn.action == "ban":
            pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                             eligible_ids=self._eligible_ids)
            if pool:
                self._execute_ban(random.choice(pool), is_auto=True)
            else:
                self._advance()
        elif turn.action == "pick":
            # For Choice turns, auto-pick from the already-presented pool
            if turn.pick_type in ("Choice", "Choice 3") and self._choice_pool:
                valid = [p for p in self._choice_pool
                         if p["SpriteID"] not in self._picked_ids
                         and p["SpriteID"] not in self._banned_ids]
                if valid:
                    self._execute_pick(turn, random.choice(valid))
                    return
            arch = _arch_from_type(turn.pick_type)
            pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                             arch_filter=arch, eligible_ids=self._eligible_ids)
            if not pool:
                pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                                 eligible_ids=self._eligible_ids)
            if pool:
                self._execute_pick(turn, random.choice(pool))
            else:
                self._advance()

    # ── Action handlers ────────────────────────────────────────────────────────

    def _on_sidebar_changed(self, player):
        self._pending = player
        self._action_bar.update_selection(player)

        # Mirror the selection into the active pick slot as a ghost preview
        turn = self._current_turn()
        if turn and turn.action == "pick" and self._danny_panel and self._alex_panel:
            N = self._n
            if turn.team == 1:
                ts = turn.global_slot
                if player:
                    self._danny_panel.preview_slot(ts, player)
                else:
                    self._danny_panel.clear_slot_preview(ts)
            else:
                ts = turn.global_slot - N
                if player:
                    self._alex_panel.preview_slot(ts, player)
                else:
                    self._alex_panel.clear_slot_preview(ts)

    def _on_choice_pick(self, player, turn: DraftTurn):
        """Handle player selection from a Choice card."""
        if not self._active:
            return
        if self._current_turn() is not turn:
            return  # Turn already advanced (double-click guard)
        sid = player["SpriteID"]
        if sid in self._picked_ids or sid in self._banned_ids:
            return
        self._execute_pick(turn, player)

    def _on_confirm_pick(self):
        player = self._pending or get_app_state().selected_player
        turn   = self._current_turn()
        if not player or not turn or turn.action != "pick":
            return

        sid = player["SpriteID"]
        if sid in self._picked_ids or sid in self._banned_ids:
            self._action_bar.show_error("Player already used in this draft")
            return

        # Archetype restriction check
        arch = _arch_from_type(turn.pick_type)
        if arch and (player["Archetype_Name"] or "").lower() != arch.lower():
            self._action_bar.show_error(f"Must select a {arch}")
            return

        # Archetype Mirror check
        if self._config.get("archetype_mirror") and turn.team == 2:
            mirror_slot = turn.global_slot - self._n
            if mirror_slot in self._picks:
                req = self._picks[mirror_slot]["Archetype_Name"] or ""
                got = player["Archetype_Name"] or ""
                if req and got.lower() != req.lower():
                    self._action_bar.show_error(f"Mirror: must pick a {req}")
                    return

        self._execute_pick(turn, player)

    def _on_confirm_ban(self):
        player = self._pending or get_app_state().selected_player
        turn   = self._current_turn()
        if not player or not turn or turn.action != "ban":
            return

        sid = player["SpriteID"]
        if sid in self._picked_ids or sid in self._banned_ids:
            self._action_bar.show_error("Player already used in this draft")
            return

        self._execute_ban(player)

    def _on_roll_pick(self):
        turn = self._current_turn()
        if not turn or turn.pick_type != "Random":
            return
        pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                         eligible_ids=self._eligible_ids)
        if not pool:
            self._action_bar.show_error("No eligible players left!")
            return
        self._countdown_timer.stop()
        self._set_timer_banner(None)
        target = random.choice(pool)
        self._action_bar.show_roll(pool, target,
                                   on_complete=lambda: self._execute_pick(turn, target))

    def _auto_random_ban(self):
        if not self._active:
            return
        pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                         eligible_ids=self._eligible_ids)
        if pool:
            self._execute_ban(random.choice(pool), is_auto=True)
        else:
            self._advance()

    # ── Execution ──────────────────────────────────────────────────────────────

    def _execute_pick(self, turn: DraftTurn, player):
        if not self._active:
            return
        self._picked_ids.add(player["SpriteID"])
        self._picks[turn.global_slot] = player

        N = self._n
        if turn.global_slot < N:
            self._danny_panel.fill_slot_slam(turn.global_slot, player)
        else:
            self._alex_panel.fill_slot_slam(turn.global_slot - N, player)

        self.excluded_updated.emit(self._picked_ids | self._banned_ids)
        try:
            get_audio_player().play_click()
        except Exception:
            pass
        self._advance()

    def _execute_ban(self, player, is_auto: bool = False):
        if not self._active:
            return
        self._banned_ids.add(player["SpriteID"])
        self._banned_players.append(player)
        self._ban_pool.add_ban(player, is_auto=is_auto)
        self.excluded_updated.emit(self._picked_ids | self._banned_ids)
        try:
            get_audio_player().play_click()
        except Exception:
            pass
        self._advance()

    # ── Random Fast ────────────────────────────────────────────────────────────

    def _fast_random_all(self):
        """Assign all picks randomly in one pass — no per-pick animation or waiting."""
        N = self._n
        pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                         eligible_ids=self._eligible_ids)

        pick_turns = [t for t in self._turns if t.action == "pick"]
        need = len(pick_turns)
        sample = random.sample(pool, min(need, len(pool)))

        for turn, player in zip(pick_turns, sample):
            self._picked_ids.add(player["SpriteID"])
            self._picks[turn.global_slot] = player
            if turn.global_slot < N:
                self._danny_panel.fill_slot_slam(turn.global_slot, player)
            else:
                self._alex_panel.fill_slot_slam(turn.global_slot - N, player)

        self._current_idx = len(self._turns)
        self.excluded_updated.emit(self._picked_ids | self._banned_ids)
        self._timeline.highlight(self._current_idx)
        QTimer.singleShot(400, self._on_draft_complete)

    # ── Draft complete ─────────────────────────────────────────────────────────

    def _on_draft_complete(self):
        self._danny_panel.deactivate_all()
        self._alex_panel.deactivate_all()
        self.slot_filter_changed.emit("")
        self._timeline.highlight(len(self._turns))

        has_wild = self._config.get("wild_card_slot", False)
        if has_wild:
            self._apply_wild_card()

        self._action_bar.show_complete(has_wild_card=has_wild)

        # Sync to app state for the load handler
        app_state = get_app_state()
        for gs, player in self._picks.items():
            app_state.set_picker_slot(gs, player)

    def _apply_wild_card(self):
        N = self._n
        for team, slot_range in [(1, range(N)), (2, range(N, 2 * N))]:
            filled = [gs for gs in slot_range if gs in self._picks]
            if not filled:
                continue
            swap_gs = random.choice(filled)
            pool = _get_pool(self._config, self._picked_ids, self._banned_ids,
                             eligible_ids=self._eligible_ids)
            if not pool:
                continue
            old = self._picks[swap_gs]
            new_p = random.choice(pool)
            self._picked_ids.discard(old["SpriteID"])
            self._picked_ids.add(new_p["SpriteID"])
            self._picks[swap_gs] = new_p
            if swap_gs < N:
                self._danny_panel.fill_slot(swap_gs, new_p, wild_card=True)
            else:
                self._alex_panel.fill_slot(swap_gs - N, new_p, wild_card=True)
