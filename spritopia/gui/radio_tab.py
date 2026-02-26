"""
Spotify-inspired radio browser tab.

Browse view  — searchable artist list + track list.
Playlist view — create/edit/save named playlists, play them via the Radio singleton.
"""

import json
import os
import re
import uuid
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QFrame, QScrollArea, QSizePolicy, QPushButton, QStackedWidget,
)
from PySide6.QtCore import Qt, QTimer, Signal

from spritopia.gui.theme import COLORS

# Playlists are stored next to the existing stations / songs data
_PLAYLIST_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "music", "playlists")
)

# ── Station display config ────────────────────────────────────────────────────

_STATION_META = {
    "nba":    ("NBA",    "#4a9eff"),
    "saloon": ("Saloon", "#f59e0b"),
    "trench": ("Trench", "#a78bfa"),
}

_STATION_ORDER = ["nba", "saloon", "trench"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def _rgba(hex_color: str, alpha: int) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _fmt_ms(ms: int) -> str:
    s = max(0, int(ms)) // 1000
    return f"{s // 60}:{s % 60:02d}"


_SPLIT_RE    = re.compile(r'\s*\(|\s*,\s*|\s+and\s+', re.IGNORECASE)
_FEATURE_RE  = re.compile(r'\(\s*(?:ft\.?|feat\.?|featuring|performed\s+by|with)\s+(.+?)\s*\)', re.IGNORECASE)
_AND_COMMA_RE = re.compile(r'\s*,\s*|\s+and\s+(?!the\b)', re.IGNORECASE)


def _primary_artist(artist: str) -> str:
    if not artist:
        return "Unknown Artist"
    return _SPLIT_RE.split(artist, maxsplit=1)[0].strip() or "Unknown Artist"


def _all_artists(artist: str) -> list:
    """Return every credited artist name from an artist field string.

    Handles: "A and B", "A, B", "A (ft. B, C)", "A (Performed by B)", etc.
    Ignores non-credit parentheticals like "(Produced by X)".
    """
    if not artist:
        return ["Unknown Artist"]

    # Main credited artists (everything before the first parenthesis)
    main_part = re.split(r'\s*\(', artist, maxsplit=1)[0].strip()
    main_names = _AND_COMMA_RE.split(main_part) if main_part else []

    # Feature / performed-by parentheticals
    feature_names = []
    for m in _FEATURE_RE.finditer(artist):
        feature_names.extend(_AND_COMMA_RE.split(m.group(1)))

    result, seen = [], set()
    for name in main_names + feature_names:
        name = name.strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            result.append(name)

    return result if result else ["Unknown Artist"]


def _nav_button_ss() -> str:
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {COLORS['text_secondary']};
            border: none;
            padding: 6px 18px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {_rgba(COLORS['bg_light'], 200)};
            color: {COLORS['text_primary']};
        }}
        QPushButton:checked {{
            background-color: {COLORS['accent_primary']};
            color: white;
        }}
    """


def _scroll_ss(bg: str) -> str:
    return f"""
        QScrollArea {{ border: none; background-color: {bg}; }}
        QScrollBar:vertical {{
            width: 6px; background: transparent; border: none;
        }}
        QScrollBar::handle:vertical {{
            background: rgba(255,255,255,50);
            border-radius: 3px; min-height: 20px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """


# ── Browse: song row ──────────────────────────────────────────────────────────

class _SongRow(QFrame):
    clicked = Signal(str)

    def __init__(self, song: dict, station_ids: list, index: int, parent=None):
        super().__init__(parent)
        self._song_id    = song["id"]
        self._is_playing = False
        self._index      = index

        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)

        self._normal_ss = "QFrame { background-color: transparent; border: none; border-radius: 4px; }"
        self._hover_ss  = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 18)}; border: none; border-radius: 4px; }}"
        self._play_ss   = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 30)}; border: none; border-left: 3px solid {COLORS['accent_primary']}; border-radius: 4px; }}"
        self.setStyleSheet(self._normal_ss)

        lo = QHBoxLayout(self)
        lo.setContentsMargins(8, 0, 12, 0)
        lo.setSpacing(0)

        self._idx_lbl = QLabel(str(index))
        self._idx_lbl.setFixedWidth(36)
        self._idx_lbl.setAlignment(Qt.AlignCenter)
        self._idx_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(self._idx_lbl)

        self._name_lbl = QLabel(song.get("name", "Unknown"))
        self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
        self._name_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lo.addWidget(self._name_lbl, stretch=1)

        lo.addSpacing(12)

        artist_lbl = QLabel(_primary_artist(song.get("artist") or ""))
        artist_lbl.setFixedWidth(160)
        artist_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        artist_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(artist_lbl)

        lo.addSpacing(12)

        for sid in [s for s in _STATION_ORDER if s in station_ids]:
            label, color = _STATION_META[sid]
            badge = QLabel(label)
            badge.setStyleSheet(f"""
                font-size: 9px; font-weight: bold; color: {color};
                background-color: {_rgba(color, 28)}; padding: 1px 6px;
                border-radius: 3px; border: 1px solid {_rgba(color, 70)};
            """)
            lo.addWidget(badge)
            lo.addSpacing(5)

        lo.addSpacing(8)

        dur_lbl = QLabel(_fmt_ms(song.get("length", 0)))
        dur_lbl.setFixedWidth(40)
        dur_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dur_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(dur_lbl)

        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    @property
    def song_id(self) -> str:
        return self._song_id

    def set_playing(self, playing: bool):
        if playing == self._is_playing:
            return
        self._is_playing = playing
        if playing:
            self._idx_lbl.setText("♪")
            self._idx_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['accent_primary']}; background: transparent;")
            self._name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['accent_primary']}; background: transparent;")
            self.setStyleSheet(self._play_ss)
        else:
            self._idx_lbl.setText(str(self._index))
            self._idx_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
            self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
            self.setStyleSheet(self._normal_ss)

    def enterEvent(self, event):
        if not self._is_playing:
            self.setStyleSheet(self._hover_ss)

    def leaveEvent(self, event):
        if not self._is_playing:
            self.setStyleSheet(self._normal_ss)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setStyleSheet(self._play_ss)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit(self._song_id)
            elif not self._is_playing:
                self.setStyleSheet(self._normal_ss)


# ── Browse: artist sidebar item ───────────────────────────────────────────────

class _ArtistItem(QFrame):
    clicked = Signal(object)

    def __init__(self, display_name: str, artist: Optional[str], count: int, parent=None):
        super().__init__(parent)
        self._artist   = artist
        self._selected = False

        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)

        self._normal_ss = "QFrame { background-color: transparent; border: none; border-radius: 4px; }"
        self._hover_ss  = f"QFrame {{ background-color: {_rgba(COLORS['bg_light'], 200)}; border: none; border-radius: 4px; }}"
        self._sel_ss    = f"QFrame {{ background-color: {COLORS['accent_primary']}; border: none; border-radius: 4px; }}"
        self.setStyleSheet(self._normal_ss)

        lo = QHBoxLayout(self)
        lo.setContentsMargins(10, 0, 10, 0)
        lo.setSpacing(8)

        self._name_lbl = QLabel(display_name)
        self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
        lo.addWidget(self._name_lbl, stretch=1)

        self._count_lbl = QLabel(str(count))
        self._count_lbl.setAlignment(Qt.AlignCenter)
        self._count_lbl.setStyleSheet(f"""
            font-size: 10px; font-weight: 600;
            color: {COLORS['text_muted']};
            background-color: {_rgba(COLORS['bg_dark'], 180)};
            padding: 1px 7px; border-radius: 8px;
        """)
        lo.addWidget(self._count_lbl)

        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    @property
    def artist(self) -> Optional[str]:
        return self._artist

    def set_selected(self, selected: bool):
        self._selected = selected
        if selected:
            self.setStyleSheet(self._sel_ss)
            self._name_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: white; background: transparent;")
            self._count_lbl.setStyleSheet("font-size: 10px; font-weight: 600; color: white; background-color: rgba(255,255,255,40); padding: 1px 7px; border-radius: 8px;")
        else:
            self.setStyleSheet(self._normal_ss)
            self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
            self._count_lbl.setStyleSheet(f"font-size: 10px; font-weight: 600; color: {COLORS['text_muted']}; background-color: {_rgba(COLORS['bg_dark'], 180)}; padding: 1px 7px; border-radius: 8px;")

    def enterEvent(self, event):
        if not self._selected:
            self.setStyleSheet(self._hover_ss)

    def leaveEvent(self, event):
        if not self._selected:
            self.setStyleSheet(self._normal_ss)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit(self._artist)


# ── Playlist: sidebar item ────────────────────────────────────────────────────

class _PlaylistItem(QFrame):
    clicked          = Signal(str)
    delete_requested = Signal(str)

    def __init__(self, pl_id: str, name: str, count: int, parent=None):
        super().__init__(parent)
        self._pl_id    = pl_id
        self._selected = False

        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)

        self._normal_ss = "QFrame { background-color: transparent; border: none; border-radius: 4px; }"
        self._hover_ss  = f"QFrame {{ background-color: {_rgba(COLORS['bg_light'], 200)}; border: none; border-radius: 4px; }}"
        self._sel_ss    = f"QFrame {{ background-color: {COLORS['accent_primary']}; border: none; border-radius: 4px; }}"
        self.setStyleSheet(self._normal_ss)

        lo = QHBoxLayout(self)
        lo.setContentsMargins(10, 0, 6, 0)
        lo.setSpacing(6)

        self._name_lbl = QLabel(name)
        self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
        lo.addWidget(self._name_lbl, stretch=1)

        self._count_lbl = QLabel(str(count))
        self._count_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(self._count_lbl)

        del_btn = QPushButton("×")
        del_btn.setFixedSize(20, 20)
        del_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: none;
                color: {COLORS['text_muted']}; font-size: 14px;
                border-radius: 3px;
            }}
            QPushButton:hover {{ color: {COLORS['accent_danger']}; background: {_rgba(COLORS['accent_danger'], 30)}; }}
        """)
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self._pl_id))
        lo.addWidget(del_btn)

        # Labels pass through, button does not
        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    @property
    def pl_id(self) -> str:
        return self._pl_id

    def set_selected(self, selected: bool):
        self._selected = selected
        if selected:
            self.setStyleSheet(self._sel_ss)
            self._name_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: white; background: transparent;")
            self._count_lbl.setStyleSheet("font-size: 11px; color: rgba(255,255,255,180); background: transparent;")
        else:
            self.setStyleSheet(self._normal_ss)
            self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
            self._count_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")

    def enterEvent(self, event):
        if not self._selected:
            self.setStyleSheet(self._hover_ss)

    def leaveEvent(self, event):
        if not self._selected:
            self.setStyleSheet(self._normal_ss)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit(self._pl_id)


# ── Playlist: song row inside the editor ─────────────────────────────────────

class _PlaylistSongRow(QFrame):
    play_requested   = Signal(str)
    remove_requested = Signal(str)

    def __init__(self, song: dict, index: int, parent=None):
        super().__init__(parent)
        self._song_id    = song["id"]
        self._is_playing = False
        self._index      = index

        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)

        self._normal_ss = "QFrame { background-color: transparent; border: none; border-radius: 4px; }"
        self._hover_ss  = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 18)}; border: none; border-radius: 4px; }}"
        self._play_ss   = f"QFrame {{ background-color: {_rgba(COLORS['accent_primary'], 30)}; border: none; border-left: 3px solid {COLORS['accent_primary']}; border-radius: 4px; }}"
        self.setStyleSheet(self._normal_ss)

        lo = QHBoxLayout(self)
        lo.setContentsMargins(8, 0, 8, 0)
        lo.setSpacing(0)

        self._idx_lbl = QLabel(str(index))
        self._idx_lbl.setFixedWidth(32)
        self._idx_lbl.setAlignment(Qt.AlignCenter)
        self._idx_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(self._idx_lbl)

        self._name_lbl = QLabel(song.get("name", "Unknown"))
        self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
        self._name_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lo.addWidget(self._name_lbl, stretch=1)

        lo.addSpacing(8)

        artist_text = _primary_artist(song.get("artist") or "")
        art_lbl = QLabel(artist_text)
        art_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        art_lbl.setFixedWidth(140)
        art_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lo.addWidget(art_lbl)

        lo.addSpacing(12)

        dur_lbl = QLabel(_fmt_ms(song.get("length", 0)))
        dur_lbl.setFixedWidth(36)
        dur_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dur_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        lo.addWidget(dur_lbl)

        lo.addSpacing(8)

        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(20, 20)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: none;
                color: {COLORS['text_muted']}; font-size: 14px; border-radius: 3px;
            }}
            QPushButton:hover {{ color: {COLORS['accent_danger']}; background: {_rgba(COLORS['accent_danger'], 30)}; }}
        """)
        remove_btn.clicked.connect(lambda: self.remove_requested.emit(self._song_id))
        lo.addWidget(remove_btn)

        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents)

    @property
    def song_id(self) -> str:
        return self._song_id

    def set_playing(self, playing: bool):
        if playing == self._is_playing:
            return
        self._is_playing = playing
        if playing:
            self._idx_lbl.setText("♪")
            self._idx_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['accent_primary']}; background: transparent;")
            self._name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['accent_primary']}; background: transparent;")
            self.setStyleSheet(self._play_ss)
        else:
            self._idx_lbl.setText(str(self._index))
            self._idx_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
            self._name_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text_primary']}; background: transparent;")
            self.setStyleSheet(self._normal_ss)

    def enterEvent(self, event):
        if not self._is_playing:
            self.setStyleSheet(self._hover_ss)

    def leaveEvent(self, event):
        if not self._is_playing:
            self.setStyleSheet(self._normal_ss)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setStyleSheet(self._play_ss)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.play_requested.emit(self._song_id)
            elif not self._is_playing:
                self.setStyleSheet(self._normal_ss)


# ── Playlist: add-song search result row ─────────────────────────────────────

class _AddSongRow(QFrame):
    add_requested = Signal(str)

    def __init__(self, song: dict, parent=None):
        super().__init__(parent)
        self._song_id = song["id"]

        self.setFixedHeight(36)

        self.setStyleSheet("QFrame { background-color: transparent; border: none; }")

        lo = QHBoxLayout(self)
        lo.setContentsMargins(8, 0, 8, 0)
        lo.setSpacing(8)

        name_lbl = QLabel(song.get("name", "Unknown"))
        name_lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_primary']}; background: transparent;")
        name_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lo.addWidget(name_lbl, stretch=1)

        artist_text = _primary_artist(song.get("artist") or "")
        art_lbl = QLabel(artist_text)
        art_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent;")
        art_lbl.setFixedWidth(120)
        art_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lo.addWidget(art_lbl)

        add_btn = QPushButton("+")
        add_btn.setFixedSize(22, 22)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {_rgba(COLORS['accent_primary'], 40)}; border: none;
                color: {COLORS['accent_primary']}; font-size: 16px; font-weight: bold;
                border-radius: 3px;
            }}
            QPushButton:hover {{ background: {COLORS['accent_primary']}; color: white; }}
        """)
        add_btn.clicked.connect(lambda: self.add_requested.emit(self._song_id))
        lo.addWidget(add_btn)


# ── Playlist view ─────────────────────────────────────────────────────────────

class PlaylistView(QWidget):
    """Full playlist management: create, edit, save, play."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._radio          = None
        self._catalog_songs: list = []
        self._catalog_map:   dict = {}
        self._playlists:     dict = {}
        self._selected_id:   Optional[str] = None
        self._pl_items:      list = []
        self._song_rows:     list = []
        self._result_rows:   list = []

        # Playlist-mode playback state
        self._pl_mode:        bool          = False
        self._pl_order:       list          = []   # song IDs in current play order
        self._pl_set:         set           = set()
        self._pl_index:       int           = 0
        self._pl_last_active: Optional[str] = None
        self._pl_shuffle:     bool          = False

        self._build_ui()

    def setup(self, radio, catalog_songs: list):
        self._radio         = radio
        self._catalog_songs = catalog_songs
        self._catalog_map   = {s["id"]: s for s in catalog_songs}
        self._load_playlists()
        self._populate_pl_sidebar()

    def refresh_playing(self, active_id: Optional[str]):
        for row in self._song_rows:
            row.set_playing(row.song_id == active_id)

        if not self._pl_mode:
            return
        if active_id == self._pl_last_active:
            return
        if not active_id or active_id not in self._pl_set:
            # Only exit playlist mode if we had already been tracking a song.
            # When _pl_last_active is None we're still waiting for the queued
            # song to become active — don't cancel playlist mode prematurely.
            if self._pl_last_active is not None:
                self._pl_mode = False
            return

        new_index            = self._pl_order.index(active_id)
        self._pl_index       = new_index
        self._pl_last_active = active_id

        # Push the next song to the front of the queue so skip and natural
        # progression both land on the correct playlist song
        n = len(self._pl_order)
        if n > 1:
            self._radio.enqueueSong(
                self._pl_order[(new_index + 1) % n], placeAtFront=True
            )

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        lo.addWidget(self._build_sidebar())
        lo.addWidget(self._build_editor_area(), stretch=1)

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-right: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QVBoxLayout(sidebar)
        lo.setContentsMargins(12, 16, 12, 12)
        lo.setSpacing(10)

        hdr = QLabel("PLAYLISTS")
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

        self._pl_container = QWidget()
        self._pl_container.setStyleSheet("background: transparent;")
        self._pl_lo = QVBoxLayout(self._pl_container)
        self._pl_lo.setContentsMargins(0, 0, 0, 0)
        self._pl_lo.setSpacing(2)
        self._pl_lo.addStretch()

        scroll.setWidget(self._pl_container)
        lo.addWidget(scroll, stretch=1)

        new_btn = QPushButton("+ New Playlist")
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_rgba(COLORS['accent_primary'], 40)};
                color: {COLORS['accent_primary']};
                border: 1px solid {_rgba(COLORS['accent_primary'], 80)};
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                padding: 7px 0;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_primary']};
                color: white;
            }}
        """)
        new_btn.clicked.connect(self._new_playlist)
        lo.addWidget(new_btn)

        return sidebar

    def _build_editor_area(self) -> QStackedWidget:
        self._editor_stack = QStackedWidget()
        self._editor_stack.addWidget(self._build_empty_state())  # index 0
        self._editor_stack.addWidget(self._build_editor())       # index 1
        return self._editor_stack

    def _build_empty_state(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(w)
        lo.setAlignment(Qt.AlignCenter)
        lo.setSpacing(8)
        lbl = QLabel("Select a playlist or create one")
        lbl.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']};")
        lbl.setAlignment(Qt.AlignCenter)
        lo.addWidget(lbl)
        return w

    def _build_editor(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        hdr_lo = QHBoxLayout(header)
        hdr_lo.setContentsMargins(28, 0, 24, 0)
        hdr_lo.setSpacing(16)

        name_col = QVBoxLayout()
        name_col.setSpacing(3)

        self._name_edit = QLineEdit()
        self._name_edit.setStyleSheet(f"""
            QLineEdit {{
                background: transparent; border: none;
                font-size: 22px; font-weight: 700;
                color: {COLORS['text_primary']};
                padding: 0;
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {COLORS['accent_primary']};
            }}
        """)
        self._name_edit.editingFinished.connect(self._on_rename)
        name_col.addWidget(self._name_edit)

        self._pl_sub = QLabel("")
        self._pl_sub.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
        name_col.addWidget(self._pl_sub)

        hdr_lo.addLayout(name_col, stretch=1)

        self._shuffle_btn = QPushButton("⇄  Shuffle")
        self._shuffle_btn.setFixedHeight(36)
        self._shuffle_btn.setCheckable(True)
        self._shuffle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_muted']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 18px; font-size: 13px; font-weight: 600;
                padding: 0 18px;
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
                border-color: {COLORS['text_secondary']};
            }}
            QPushButton:checked {{
                background-color: {_rgba(COLORS['accent_primary'], 40)};
                color: {COLORS['accent_primary']};
                border: 1px solid {_rgba(COLORS['accent_primary'], 120)};
            }}
        """)
        self._shuffle_btn.clicked.connect(self._on_shuffle_toggle)
        hdr_lo.addWidget(self._shuffle_btn)

        play_btn = QPushButton("▶  Play All")
        play_btn.setFixedHeight(36)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white; border: none; border-radius: 18px;
                font-size: 13px; font-weight: 600;
                padding: 0 22px;
            }}
            QPushButton:hover {{ background-color: {_rgba(COLORS['accent_primary'], 200)}; }}
            QPushButton:disabled {{ background-color: {COLORS['bg_light']}; color: {COLORS['text_muted']}; }}
        """)
        play_btn.clicked.connect(self._play_all)
        self._play_btn = play_btn
        hdr_lo.addWidget(play_btn)

        lo.addWidget(header)

        # ── Playlist song list ─────────────────────────────────────────────────
        song_scroll = QScrollArea()
        song_scroll.setWidgetResizable(True)
        song_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        song_scroll.setStyleSheet(_scroll_ss(COLORS['bg_dark']))

        self._song_container = QWidget()
        self._song_container.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        self._song_lo = QVBoxLayout(self._song_container)
        self._song_lo.setContentsMargins(8, 8, 8, 0)
        self._song_lo.setSpacing(2)
        self._song_lo.addStretch()

        song_scroll.setWidget(self._song_container)
        lo.addWidget(song_scroll, stretch=1)

        # ── Add songs section ─────────────────────────────────────────────────
        add_section = QFrame()
        add_section.setFixedHeight(200)
        add_section.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['border_dark']};
            }}
        """)
        add_lo = QVBoxLayout(add_section)
        add_lo.setContentsMargins(16, 12, 16, 12)
        add_lo.setSpacing(8)

        add_hdr = QLabel("ADD SONGS")
        add_hdr.setStyleSheet(f"font-size: 10px; font-weight: bold; letter-spacing: 1px; color: {COLORS['text_muted']}; background: transparent;")
        add_lo.addWidget(add_hdr)

        self._add_search = QLineEdit()
        self._add_search.setPlaceholderText("Search songs to add…")
        self._add_search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px; color: {COLORS['text_primary']};
                font-size: 12px; padding: 5px 10px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent_primary']}; }}
        """)
        self._add_search.textChanged.connect(self._on_add_search)
        add_lo.addWidget(self._add_search)

        results_scroll = QScrollArea()
        results_scroll.setWidgetResizable(True)
        results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        results_scroll.setStyleSheet(_scroll_ss(COLORS['bg_medium']))

        self._results_container = QWidget()
        self._results_container.setStyleSheet(f"background-color: {COLORS['bg_medium']};")
        self._results_lo = QVBoxLayout(self._results_container)
        self._results_lo.setContentsMargins(0, 0, 0, 0)
        self._results_lo.setSpacing(1)
        self._results_lo.addStretch()

        results_scroll.setWidget(self._results_container)
        add_lo.addWidget(results_scroll)

        lo.addWidget(add_section)

        return w

    # ── Persistence ───────────────────────────────────────────────────────────

    def _load_playlists(self):
        os.makedirs(_PLAYLIST_DIR, exist_ok=True)
        self._playlists = {}
        for fname in sorted(os.listdir(_PLAYLIST_DIR)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(_PLAYLIST_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                pl_id = data.get("id") or fname[:-5]
                self._playlists[pl_id] = {
                    "name":  data.get("name", "Untitled"),
                    "songs": data.get("songs", []),
                }
            except Exception:
                pass

    def _save_playlist(self, pl_id: str):
        os.makedirs(_PLAYLIST_DIR, exist_ok=True)
        pl = self._playlists.get(pl_id)
        if pl is None:
            return
        path = os.path.join(_PLAYLIST_DIR, f"{pl_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"id": pl_id, "name": pl["name"], "songs": pl["songs"]}, f, indent=2)

    def _delete_file(self, pl_id: str):
        path = os.path.join(_PLAYLIST_DIR, f"{pl_id}.json")
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    # ── Sidebar population ────────────────────────────────────────────────────

    def _populate_pl_sidebar(self):
        for item in self._pl_items:
            self._pl_lo.removeWidget(item)
            item.deleteLater()
        self._pl_items.clear()

        for i, (pl_id, pl) in enumerate(self._playlists.items()):
            item = _PlaylistItem(pl_id, pl["name"], len(pl["songs"]))
            item.clicked.connect(self._select_playlist)
            item.delete_requested.connect(self._delete_playlist)
            self._pl_lo.insertWidget(i, item)
            self._pl_items.append(item)

        # Restore selection if still valid
        if self._selected_id and self._selected_id in self._playlists:
            self._select_playlist(self._selected_id)
        else:
            self._selected_id = None
            self._editor_stack.setCurrentIndex(0)

    # ── Playlist actions ──────────────────────────────────────────────────────

    def _new_playlist(self):
        pl_id = uuid.uuid4().hex[:10]
        # Avoid name collisions
        existing_names = {pl["name"] for pl in self._playlists.values()}
        base = "New Playlist"
        name = base
        n = 2
        while name in existing_names:
            name = f"{base} {n}"
            n += 1

        self._playlists[pl_id] = {"name": name, "songs": []}
        self._save_playlist(pl_id)
        self._populate_pl_sidebar()
        self._select_playlist(pl_id)
        # Focus the name field so user can rename immediately
        self._name_edit.selectAll()
        self._name_edit.setFocus()

    def _select_playlist(self, pl_id: str):
        self._selected_id = pl_id
        for item in self._pl_items:
            item.set_selected(item.pl_id == pl_id)
        self._editor_stack.setCurrentIndex(1)
        self._refresh_editor()

    def _delete_playlist(self, pl_id: str):
        self._delete_file(pl_id)
        self._playlists.pop(pl_id, None)
        if self._selected_id == pl_id:
            self._selected_id = None
        self._populate_pl_sidebar()

    def _on_rename(self):
        if not self._selected_id:
            return
        new_name = self._name_edit.text().strip()
        if not new_name:
            new_name = "Untitled"
            self._name_edit.setText(new_name)
        self._playlists[self._selected_id]["name"] = new_name
        self._save_playlist(self._selected_id)
        # Update sidebar label
        for item in self._pl_items:
            if item.pl_id == self._selected_id:
                item._name_lbl.setText(new_name)
                break

    def _add_song(self, song_id: str):
        if not self._selected_id:
            return
        pl = self._playlists[self._selected_id]
        if song_id in pl["songs"]:
            return
        pl["songs"].append(song_id)
        self._save_playlist(self._selected_id)
        self._refresh_editor()

    def _remove_song(self, song_id: str):
        if not self._selected_id:
            return
        pl = self._playlists[self._selected_id]
        if song_id in pl["songs"]:
            pl["songs"].remove(song_id)
            self._save_playlist(self._selected_id)
            self._refresh_editor()

    def _play_all(self):
        pl = self._playlists.get(self._selected_id)
        if not pl or not pl["songs"]:
            return
        self._start_playlist_at(pl["songs"][0])

    # ── Editor refresh ────────────────────────────────────────────────────────

    def _refresh_editor(self):
        pl = self._playlists.get(self._selected_id)
        if not pl:
            return

        self._name_edit.setText(pl["name"])
        n = len(pl["songs"])
        self._pl_sub.setText(f"{n} song{'s' if n != 1 else ''}")
        self._play_btn.setEnabled(n > 0)

        # Update sidebar count
        for item in self._pl_items:
            if item.pl_id == self._selected_id:
                item._count_lbl.setText(str(n))
                break

        # Rebuild song rows
        for row in self._song_rows:
            self._song_lo.removeWidget(row)
            row.deleteLater()
        self._song_rows.clear()

        for i, song_id in enumerate(pl["songs"], start=1):
            song = self._catalog_map.get(song_id)
            if not song:
                continue
            row = _PlaylistSongRow(song, i, self._song_container)
            row.play_requested.connect(self._play_song)
            row.remove_requested.connect(self._remove_song)
            self._song_lo.insertWidget(i - 1, row)
            self._song_rows.append(row)

        # Re-run search to refresh add results with updated already-added state
        self._on_add_search(self._add_search.text())

    def _on_add_search(self, text: str):
        q = text.strip().lower()

        # Clear old results
        for row in self._result_rows:
            self._results_lo.removeWidget(row)
            row.deleteLater()
        self._result_rows.clear()

        if not q:
            return

        added = set(self._playlists.get(self._selected_id, {}).get("songs", []))
        matches = [
            s for s in self._catalog_songs
            if q in s.get("name", "").lower() or q in (s.get("artist") or "").lower()
        ][:12]  # cap at 12 results

        for i, song in enumerate(matches):
            if song["id"] in added:
                continue  # skip already-added songs
            row = _AddSongRow(song, self._results_container)
            row.add_requested.connect(self._add_song)
            self._results_lo.insertWidget(i, row)
            self._result_rows.append(row)

    def _play_song(self, song_id: str):
        self._start_playlist_at(song_id)

    def _start_playlist_at(self, song_id: str):
        """Begin playlist playback from song_id, queueing the rest in order (or shuffled)."""
        import random
        pl = self._playlists.get(self._selected_id)
        if not pl or not pl["songs"] or not self._radio:
            return

        songs = list(pl["songs"])
        if song_id not in songs:
            song_id = songs[0]

        if self._pl_shuffle:
            rest = [s for s in songs if s != song_id]
            random.shuffle(rest)
            order = [song_id] + rest
            start = 0
        else:
            order = songs
            start = order.index(song_id)

        n = len(order)
        self._pl_mode        = True
        self._pl_order       = order
        self._pl_set         = set(order)
        self._pl_index       = start
        self._pl_last_active = None  # Reset; refresh_playing enqueues next once active changes

        self._radio.setSong(song_id)
        # NOTE: We do NOT call enqueueSong here.
        # setSong() enqueues song_id at front then signals an async skip. If we
        # called enqueueSong(next_song, placeAtFront=True) right after, next_song
        # would land at position 0 BEFORE the skip fires, so the skip would pop
        # next_song instead of song_id — causing it to play the wrong track.
        # refresh_playing() handles the enqueue once the song actually becomes active.

    def _on_shuffle_toggle(self, checked: bool):
        self._pl_shuffle = checked


# ── Radio tab (top-level) ─────────────────────────────────────────────────────

class RadioTab(QWidget):
    """
    Top-level radio tab. Nav bar switches between Browse and Playlists views.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._radio = None

        # Browse catalog data
        self._all_songs:     list = []
        self._artists:       list = []
        self._artist_songs:  dict = {}   # artist_name → [song, ...]
        self._song_stations: dict = {}
        self._selected_artist: Optional[str] = None

        self._song_rows:    list = []
        self._artist_items: list = []

        self._build_ui()

        self._poll = QTimer(self)
        self._poll.timeout.connect(self._refresh_playing)
        self._poll.start(500)

    def set_radio(self, radio):
        self._radio = radio
        self._load_catalog()
        self._populate_sidebar()
        self._select_artist(None)
        self._playlist_view.setup(radio, self._all_songs)

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        lo.addWidget(self._build_nav())

        self._stack = QStackedWidget()
        browse = QWidget()
        browse_lo = QHBoxLayout(browse)
        browse_lo.setContentsMargins(0, 0, 0, 0)
        browse_lo.setSpacing(0)
        browse_lo.addWidget(self._build_sidebar())
        browse_lo.addWidget(self._build_content(), stretch=1)

        self._playlist_view = PlaylistView()

        self._stack.addWidget(browse)              # index 0
        self._stack.addWidget(self._playlist_view) # index 1
        lo.addWidget(self._stack, stretch=1)

    def _build_nav(self) -> QFrame:
        nav = QFrame()
        nav.setFixedHeight(44)
        nav.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QHBoxLayout(nav)
        lo.setContentsMargins(16, 0, 16, 0)
        lo.setSpacing(4)

        ss = _nav_button_ss()
        self._nav_browse = QPushButton("Browse")
        self._nav_browse.setCheckable(True)
        self._nav_browse.setChecked(True)
        self._nav_browse.setStyleSheet(ss)
        self._nav_browse.clicked.connect(lambda: self._switch_view("browse"))

        self._nav_playlists = QPushButton("Playlists")
        self._nav_playlists.setCheckable(True)
        self._nav_playlists.setStyleSheet(ss)
        self._nav_playlists.clicked.connect(lambda: self._switch_view("playlists"))

        lo.addWidget(self._nav_browse)
        lo.addWidget(self._nav_playlists)
        lo.addStretch()
        return nav

    def _switch_view(self, key: str):
        self._nav_browse.setChecked(key == "browse")
        self._nav_playlists.setChecked(key == "playlists")
        self._stack.setCurrentIndex(0 if key == "browse" else 1)

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-right: 1px solid {COLORS['border_dark']};
            }}
        """)
        lo = QVBoxLayout(sidebar)
        lo.setContentsMargins(12, 16, 12, 16)
        lo.setSpacing(10)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search artists…")
        self._search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px; color: {COLORS['text_primary']};
                font-size: 13px; padding: 6px 10px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent_primary']}; }}
        """)
        self._search.textChanged.connect(self._on_search)
        lo.addWidget(self._search)

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

        self._artist_container = QWidget()
        self._artist_container.setStyleSheet("background: transparent;")
        self._artist_lo = QVBoxLayout(self._artist_container)
        self._artist_lo.setContentsMargins(0, 0, 4, 0)
        self._artist_lo.setSpacing(2)
        self._artist_lo.addStretch()

        scroll.setWidget(self._artist_container)
        lo.addWidget(scroll, stretch=1)
        return sidebar

    def _build_content(self) -> QWidget:
        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        lo = QVBoxLayout(content)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        hdr_lo = QVBoxLayout(header)
        hdr_lo.setContentsMargins(28, 14, 28, 14)
        hdr_lo.setSpacing(3)

        self._hdr_title = QLabel("All Songs")
        self._hdr_title.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {COLORS['text_primary']}; background: transparent;")
        hdr_lo.addWidget(self._hdr_title)

        self._hdr_sub = QLabel("")
        self._hdr_sub.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; background: transparent;")
        hdr_lo.addWidget(self._hdr_sub)
        lo.addWidget(header)

        col_hdr = QFrame()
        col_hdr.setFixedHeight(30)
        col_hdr.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        col_lo = QHBoxLayout(col_hdr)
        col_lo.setContentsMargins(8, 0, 12, 0)
        col_lo.setSpacing(0)

        def _ch(text, width=0, align=Qt.AlignVCenter | Qt.AlignLeft):
            lbl = QLabel(text)
            lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; letter-spacing: 1px; color: {COLORS['text_muted']}; background: transparent;")
            lbl.setAlignment(align)
            if width:
                lbl.setFixedWidth(width)
                col_lo.addWidget(lbl)
            else:
                col_lo.addWidget(lbl, stretch=1)

        _ch("#", 36, Qt.AlignCenter)
        _ch("TITLE")
        _ch("ARTIST", 172, Qt.AlignRight | Qt.AlignVCenter)
        _ch("TIME", 40, Qt.AlignRight | Qt.AlignVCenter)
        lo.addWidget(col_hdr)

        song_scroll = QScrollArea()
        song_scroll.setWidgetResizable(True)
        song_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        song_scroll.setStyleSheet(_scroll_ss(COLORS['bg_dark']))

        self._song_container = QWidget()
        self._song_container.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        self._song_lo = QVBoxLayout(self._song_container)
        self._song_lo.setContentsMargins(8, 8, 8, 8)
        self._song_lo.setSpacing(2)
        self._song_lo.addStretch()

        song_scroll.setWidget(self._song_container)
        lo.addWidget(song_scroll, stretch=1)
        return content

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_catalog(self):
        catalog  = self._radio.catalog
        stations = self._radio.stations

        self._song_stations = {}
        for station_id, station in stations.items():
            for song_id in station.get("songChances", {}):
                self._song_stations.setdefault(song_id, []).append(station_id)

        nba_song_ids = set(stations.get("nba", {}).get("songChances", {}).keys())
        nba_artists  = {
            _primary_artist(catalog[sid].get("artist") or "")
            for sid in nba_song_ids if sid in catalog
        }

        self._all_songs = sorted(
            [
                s for s in catalog.values()
                if s.get("name") and _primary_artist(s.get("artist") or "") not in nba_artists
            ],
            key=lambda s: (s.get("artist", "").lower(), s.get("name", "").lower()),
        )

        # Build artist → songs map; each song appears under every credited artist
        self._artist_songs = {}
        for s in self._all_songs:
            for artist in _all_artists(s.get("artist") or ""):
                self._artist_songs.setdefault(artist, []).append(s)
        self._artists = sorted(self._artist_songs.keys(), key=str.lower)

    def _populate_sidebar(self):
        for item in self._artist_items:
            self._artist_lo.removeWidget(item)
            item.deleteLater()
        self._artist_items.clear()

        all_item = _ArtistItem("All Songs", None, len(self._all_songs))
        all_item.clicked.connect(self._select_artist)
        self._artist_lo.insertWidget(0, all_item)
        self._artist_items.append(all_item)

        for i, artist in enumerate(self._artists):
            count = len(self._artist_songs.get(artist, []))
            item = _ArtistItem(artist, artist, count)
            item.clicked.connect(self._select_artist)
            self._artist_lo.insertWidget(i + 1, item)
            self._artist_items.append(item)

    # ── Interaction ───────────────────────────────────────────────────────────

    def _select_artist(self, artist: Optional[str]):
        self._selected_artist = artist
        for item in self._artist_items:
            item.set_selected(item.artist == artist)

        if artist is None:
            songs = self._all_songs
            self._hdr_title.setText("All Songs")
        else:
            songs = self._artist_songs.get(artist, [])
            self._hdr_title.setText(artist)

        n = len(songs)
        self._hdr_sub.setText(f"{n} song{'s' if n != 1 else ''}")
        self._rebuild_songs(songs)

    def _on_search(self, text: str):
        q = text.strip().lower()
        for item in self._artist_items:
            if item.artist is None:
                item.setVisible(not q)
            else:
                item.setVisible(not q or q in (item.artist or "").lower())

    def _rebuild_songs(self, songs: list):
        for row in self._song_rows:
            self._song_lo.removeWidget(row)
            row.deleteLater()
        self._song_rows.clear()

        for i, song in enumerate(songs, start=1):
            station_ids = self._song_stations.get(song["id"], [])
            row = _SongRow(song, station_ids, i, self._song_container)
            row.clicked.connect(self._play_song)
            self._song_lo.insertWidget(i - 1, row)
            self._song_rows.append(row)

        self._refresh_playing()

    def _play_song(self, song_id: str):
        if self._radio:
            self._radio.setSong(song_id)
        self._refresh_playing()

    def _refresh_playing(self):
        if not self._radio:
            return
        try:
            active = self._radio._Radio__activeSong
        except Exception:
            active = None

        for row in self._song_rows:
            row.set_playing(row.song_id == active)

        self._playlist_view.refresh_playing(active)
