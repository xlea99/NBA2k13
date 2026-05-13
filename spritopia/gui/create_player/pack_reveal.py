"""
Pack Reveal Widget.

Animated reveal of newly created players, similar to card pack openings.
Shows rarity with dramatic sound effects and visual flair.
"""

import math

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGridLayout, QProgressBar, QApplication,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPixmap, QPainter, QColor

from spritopia.players.players import Player
from spritopia.players import archetypes
from spritopia.gui.theme import COLORS, get_rarity_style, get_archetype_style
from spritopia.gui.audio import get_audio_player
from spritopia.common.paths import paths

_CARD_W = 300
_CARD_H = 440


class IconWithTooltip(QLabel):
    """A label that displays an image with a rich tooltip."""

    def __init__(self, size: int = 48, parent=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)

    def set_image(self, image_path: str):
        if image_path:
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                self.setPixmap(pixmap.scaled(
                    self._size, self._size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
                return
        self.setText("?")
        self.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 20px; font-weight: bold;")

    def set_tooltip_content(self, title: str, description: str):
        tip = f"<b>{title}</b>"
        if description:
            body = description[:300] + "..." if len(description) > 300 else description
            tip += f"<br/><br/>{body}"
        self.setToolTip(tip)


class StatMiniBar(QWidget):
    """A compact stat bar for the card."""

    def __init__(self, label: str, value: int = 0, parent=None):
        super().__init__(parent)
        self._setup_ui(label, value)

    def _setup_ui(self, label: str, value: int):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 1, 0, 1)
        layout.setSpacing(4)

        self.name_label = QLabel(label[:10])
        self.name_label.setFixedWidth(70)
        self.name_label.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 10px;")
        layout.addWidget(self.name_label)

        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(7)
        self.bar.setMaximum(99)
        self.bar.setValue(value)
        layout.addWidget(self.bar, stretch=1)

        self.value_label = QLabel(str(value))
        self.value_label.setFixedWidth(24)
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value_label.setStyleSheet("font-weight: bold; font-size: 10px;")
        layout.addWidget(self.value_label)

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
                border-radius: 3px; border: none;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        self.value_label.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 10px;")


class RevealCard(QFrame):
    """
    A single player card that flips open on click.

    The flip is simulated by capturing front/back pixmaps via grab(),
    then animating a horizontal squish transform between them.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player = None
        self._revealed = False
        self._flipping = False
        self._rarity = "Common"
        self._rarity_style: dict = {}
        self._back_px: QPixmap | None = None
        self._front_px: QPixmap | None = None
        self._overlay: QLabel | None = None
        self._flip_val = 0.0
        self._anim: QPropertyAnimation | None = None
        self._setup_ui()

    # ── Animated property ─────────────────────────────────────────────────

    def _get_flip(self) -> float:
        return self._flip_val

    def _set_flip(self, val: float):
        self._flip_val = val
        self._paint_flip(val)

    flipProgress = Property(float, _get_flip, _set_flip)

    # ── UI construction ───────────────────────────────────────────────────

    def _setup_ui(self):
        self.setFixedSize(_CARD_W, _CARD_H)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self._apply_base_style()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 14, 20, 14)
        outer.setSpacing(0)

        # ── Back face (unrevealed) ─────────────────────────────────────────
        self.unrevealed_container = QWidget()
        self.unrevealed_container.setStyleSheet("background: transparent;")
        ul = QVBoxLayout(self.unrevealed_container)
        ul.setAlignment(Qt.AlignCenter)

        q = QLabel("?")
        q.setStyleSheet(
            f"font-size: 120px; font-weight: bold; color: {COLORS['text_muted']};")
        q.setAlignment(Qt.AlignCenter)
        ul.addWidget(q)

        hint = QLabel("Click to reveal")
        hint.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
        hint.setAlignment(Qt.AlignCenter)
        ul.addWidget(hint)

        outer.addWidget(self.unrevealed_container)

        # ── Front face (revealed) ──────────────────────────────────────────
        self.revealed_container = QWidget()
        self.revealed_container.setStyleSheet("background: transparent;")
        self.revealed_container.hide()
        rv = QVBoxLayout(self.revealed_container)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(0)

        # Rarity banner
        self.rarity_banner = QLabel("COMMON")
        self.rarity_banner.setAlignment(Qt.AlignCenter)
        self.rarity_banner.setFixedHeight(28)
        self.rarity_banner.setStyleSheet(f"""
            background-color: {COLORS['rarity_common']};
            color: white; font-size: 12px; font-weight: bold;
            letter-spacing: 2px; border-radius: 4px;
        """)
        rv.addWidget(self.rarity_banner)
        rv.addSpacing(7)

        # Archetype (left) + Position (right)
        arch_row = QHBoxLayout()
        arch_row.setSpacing(6)
        self.archetype_label = QLabel("Slayer")
        self.archetype_label.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {COLORS['arch_slayer']};")
        arch_row.addWidget(self.archetype_label, stretch=1)
        self.position_label = QLabel("SG")
        self.position_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.position_label.setStyleSheet(
            f"font-size: 12px; color: {COLORS['text_muted']}; font-weight: bold;")
        arch_row.addWidget(self.position_label)
        rv.addLayout(arch_row)
        rv.addSpacing(3)

        # Player name
        self.name_label = QLabel("Player Name")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLORS['text_primary']};")
        rv.addWidget(self.name_label)
        rv.addSpacing(7)

        rv.addWidget(self._make_sep())
        rv.addSpacing(7)

        # Faction row: centered [icon + name]
        faction_row = QHBoxLayout()
        faction_row.setSpacing(10)
        faction_row.addStretch()

        self.faction_icon = IconWithTooltip(size=42)
        self.faction_icon.setStyleSheet(
            f"background-color: {COLORS['bg_light']}; border-radius: 6px;")
        faction_row.addWidget(self.faction_icon, alignment=Qt.AlignVCenter)

        ftext = QVBoxLayout()
        ftext.setSpacing(1)
        fhdr = QLabel("FACTION")
        fhdr.setStyleSheet(
            f"font-size: 8px; color: {COLORS['text_muted']}; "
            f"font-weight: bold; letter-spacing: 1px;")
        ftext.addWidget(fhdr)
        self.faction_name_label = QLabel("—")
        self.faction_name_label.setStyleSheet(
            f"font-size: 11px; color: {COLORS['text_secondary']};")
        ftext.addWidget(self.faction_name_label)
        faction_row.addLayout(ftext)

        faction_row.addStretch()
        rv.addLayout(faction_row)
        rv.addSpacing(7)

        rv.addWidget(self._make_sep())
        rv.addSpacing(5)

        # Stats header + 6 bars
        shdr = QLabel("KEY ATTRIBUTES")
        shdr.setStyleSheet(
            f"font-size: 8px; color: {COLORS['text_muted']}; "
            f"font-weight: bold; letter-spacing: 1px;")
        rv.addWidget(shdr)
        rv.addSpacing(3)

        self.stat_bars: list[StatMiniBar] = []
        for _ in range(6):
            bar = StatMiniBar("---", 0)
            bar.hide()
            self.stat_bars.append(bar)
            rv.addWidget(bar)

        rv.addSpacing(7)
        rv.addWidget(self._make_sep())
        rv.addSpacing(7)

        # Artifact row: [icon] [name col]
        artifact_row = QHBoxLayout()
        artifact_row.setSpacing(8)

        self.artifact_icon = IconWithTooltip(size=42)
        self.artifact_icon.setStyleSheet(
            f"background-color: {COLORS['bg_light']}; border-radius: 6px;")
        artifact_row.addWidget(self.artifact_icon, alignment=Qt.AlignVCenter)

        atext = QVBoxLayout()
        atext.setSpacing(1)
        ahdr = QLabel("ARTIFACT")
        ahdr.setStyleSheet(
            f"font-size: 8px; color: {COLORS['text_muted']}; "
            f"font-weight: bold; letter-spacing: 1px;")
        atext.addWidget(ahdr)
        self.artifact_name_label = QLabel("—")
        self.artifact_name_label.setWordWrap(True)
        self.artifact_name_label.setStyleSheet(
            f"font-size: 11px; color: {COLORS['text_secondary']};")
        atext.addWidget(self.artifact_name_label)
        artifact_row.addLayout(atext, stretch=1)

        rv.addLayout(artifact_row)

        outer.addWidget(self.revealed_container)

    @staticmethod
    def _make_sep() -> QFrame:
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {COLORS['border_dark']}; border: none;")
        return sep

    # ── Styling helpers ───────────────────────────────────────────────────

    def _apply_base_style(self):
        self.setStyleSheet(f"""
            RevealCard {{
                background-color: {COLORS['bg_card']};
                border: none;
                border-radius: 16px;
            }}
            QLabel {{ background: transparent; border: none; }}
        """)

    def _apply_rarity_style(self):
        rs = self._rarity_style
        if self._rarity.lower() == "godlike":
            self.setStyleSheet(f"""
                RevealCard {{
                    background-color: {rs['bg']};
                    border: 3px solid {rs['glow']};
                    border-radius: 16px;
                }}
                QLabel {{ background: transparent; border: none; }}
            """)
        else:
            self.setStyleSheet(f"""
                RevealCard {{
                    background-color: {COLORS['bg_card']};
                    border: 3px solid {rs['color']};
                    border-radius: 16px;
                }}
                QLabel {{ background: transparent; border: none; }}
            """)

    # ── Player data ───────────────────────────────────────────────────────

    def set_player(self, player: Player):
        self._player = player
        self._revealed = False
        self._flipping = False
        # Pre-load rarity color so hover glow works before reveal
        rs = get_rarity_style(player["Rarity"] or "Common")
        self._hover_glow_color = QColor(rs.get("glow") or rs["color"])
        self.unrevealed_container.show()
        self.revealed_container.hide()
        self.setCursor(Qt.PointingHandCursor)
        self._apply_base_style()
        self.setGraphicsEffect(None)

    def enterEvent(self, event):
        if not self._revealed and not self._flipping:
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(28)
            glow.setOffset(0, 0)
            glow.setColor(self._hover_glow_color)
            self.setGraphicsEffect(glow)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self._revealed and not self._flipping:
            self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def _populate_revealed_content(self):
        """Fill all front-face widgets from player data."""
        rarity = self._player["Rarity"] or "Common"
        self._rarity = rarity
        self._rarity_style = get_rarity_style(rarity)
        rs = self._rarity_style
        rarity_color = rs['color']

        archetype = self._player["Archetype"]
        archetype_name = str(archetype) if archetype else "Unknown"
        archetype_style = get_archetype_style(archetype_name)

        first = self._player["First_Name"] or ""
        last = self._player["Last_Name"] or ""
        name = f"{first} {last}".strip() or "Unknown"

        faction = self._player["Faction"] or "No Faction"

        if archetype:
            pos = getattr(archetype, 'inGamePositionString', 'N/A')
            pos2 = getattr(archetype, 'inGameSecondaryPositionString', '')
            position = f"{pos}/{pos2}" if pos2 and pos2 != "None" else pos
        else:
            position = "N/A"

        # Rarity banner
        self.rarity_banner.setText(rarity.upper())
        if rarity.lower() == "godlike":
            self.rarity_banner.setStyleSheet(f"""
                background-color: {rs['bg']}; color: {rs['text']};
                font-size: 12px; font-weight: bold;
                letter-spacing: 2px; border-radius: 4px;
                border: 1px solid {rs['glow']};
            """)
        else:
            self.rarity_banner.setStyleSheet(f"""
                background-color: {rs['bg']}; color: {rarity_color};
                font-size: 12px; font-weight: bold;
                letter-spacing: 2px; border-radius: 4px;
            """)

        self.archetype_label.setText(archetype_name)
        self.archetype_label.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {archetype_style['color']};")
        self.name_label.setText(name)
        self.position_label.setText(position)

        # Faction icon + name
        self.faction_name_label.setText(
            faction if len(faction) <= 18 else faction[:15] + "...")
        self.faction_icon.set_image(
            str(paths["graphics"] / "FactionIcons" / f"{faction}.png"))
        try:
            from spritopia.players import factions as _factions
            info = _factions.dbDict["Factions"].get(faction, {})
            self.faction_icon.set_tooltip_content(faction, info.get("Description", ""))
        except Exception:
            self.faction_icon.set_tooltip_content(faction, "")

        # Stat bars (up to 6 most important attributes)
        if archetype and hasattr(archetype, 'attributeImportance'):
            attrs = archetype.attributeImportance[:6]
            for i, attr in enumerate(attrs):
                value = self._player[attr] or 0
                label = archetypes.MAPPED_ATTRIBUTES.get(attr, attr)
                self.stat_bars[i].name_label.setText(label[:10])
                self.stat_bars[i].bar.setValue(value)
                self.stat_bars[i].value_label.setText(str(value))
                self.stat_bars[i]._update_color(value)
                self.stat_bars[i].show()
            for i in range(len(attrs), 6):
                self.stat_bars[i].hide()
        else:
            for bar in self.stat_bars:
                bar.hide()

        # Artifact
        pmods = self._player.pmods if hasattr(self._player, 'pmods') else []
        if pmods:
            pmod = pmods[0]
            artifact_name = pmod.get("Name", "Unknown")
            artifact_desc = pmod.get("Description", "")
            artifact_image = pmod.get("Image", "")
            display = artifact_name if len(artifact_name) <= 40 else artifact_name[:37] + "..."
            self.artifact_name_label.setText(display)
            self.artifact_name_label.setToolTip(
                f"<b>{artifact_name}</b><br/><br/>{artifact_desc[:300]}" if artifact_desc else f"<b>{artifact_name}</b>")
            self.artifact_icon.show()
            if artifact_image:
                self.artifact_icon.set_image(str(paths["graphics"] / artifact_image))
            else:
                self.artifact_icon.setText("?")
            self.artifact_icon.set_tooltip_content(artifact_name, artifact_desc)
        else:
            self.artifact_name_label.setText("None")
            self.artifact_icon.setText("—")
            self.artifact_icon.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-size: 16px; "
                f"background-color: {COLORS['bg_light']}; border-radius: 6px;")

    # ── Flip animation ────────────────────────────────────────────────────

    def _paint_flip(self, val: float):
        """Draw a horizontally-squished frame onto the overlay."""
        if self._overlay is None:
            return
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        scale = abs(math.cos(val * math.pi))
        source = self._back_px if val < 0.5 else self._front_px
        if source is None or source.isNull():
            return

        result = QPixmap(w, h)
        result.fill(QColor(0, 0, 0, 0))
        painter = QPainter(result)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        if scale > 0.001:
            painter.translate(w * (1.0 - scale) / 2.0, 0)
            painter.scale(scale, 1.0)
        painter.drawPixmap(0, 0, source)
        painter.end()

        self._overlay.setPixmap(result)

    def reveal(self):
        """Flip the card open with animation."""
        if self._revealed or self._flipping or self._player is None:
            return

        self._revealed = True
        self._flipping = True
        self.setCursor(Qt.ArrowCursor)

        # Clear hover glow so it isn't baked into the captured pixmap
        self.setGraphicsEffect(None)

        # Capture back face (current unrevealed state)
        self._back_px = self.grab()

        # Populate front-face content (still hidden)
        self._populate_revealed_content()

        # Temporarily show front face to capture it as a pixmap
        self.unrevealed_container.hide()
        self.revealed_container.show()
        self._apply_rarity_style()
        QApplication.processEvents()
        self._front_px = self.grab()

        # Revert to back face for animation start
        self.revealed_container.hide()
        self.unrevealed_container.show()
        self._apply_base_style()

        # Transparent overlay label drawn over the card during animation
        self._overlay = QLabel(self)
        self._overlay.setGeometry(0, 0, _CARD_W, _CARD_H)
        self._overlay.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._overlay.raise_()
        self._overlay.show()

        # Play reveal sound at the midpoint of the flip
        QTimer.singleShot(250, lambda: get_audio_player().play_rarity_reveal(self._rarity))

        # Animate
        self._flip_val = 0.0
        self._anim = QPropertyAnimation(self, b"flipProgress")
        self._anim.setDuration(500)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.InOutSine)
        self._anim.finished.connect(self._finish_flip)
        self._anim.start()

    def _finish_flip(self):
        self._flipping = False
        if self._overlay:
            self._overlay.hide()
            self._overlay.deleteLater()
            self._overlay = None
        self.unrevealed_container.hide()
        self.revealed_container.show()
        self._apply_rarity_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._revealed and not self._flipping:
            self.reveal()
        super().mousePressEvent(event)

    def is_revealed(self) -> bool:
        return self._revealed

    def get_player(self) -> Player:
        return self._player


class PackRevealWidget(QWidget):
    """
    Pack reveal experience for newly created players.
    Shows cards that can be clicked to reveal, with dramatic flip effects.
    """

    finished = Signal()
    reveal_all_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._players = []
        self._cards: list[RevealCard] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        self.title = QLabel("Reveal Your Players!")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.reveal_all_btn = QPushButton("Reveal All")
        self.reveal_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_secondary']};
                color: white; border: none;
                padding: 10px 20px; font-size: 14px;
                font-weight: bold; border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: #6d28d9; }}
        """)
        self.reveal_all_btn.clicked.connect(self._reveal_all)
        header_layout.addWidget(self.reveal_all_btn)
        layout.addLayout(header_layout)

        # Subtitle
        self.subtitle = QLabel("Click each card to reveal your new player")
        self.subtitle.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(self.subtitle)

        # Scrollable card grid
        self.cards_scroll_area = QScrollArea()
        self.cards_scroll_area.setWidgetResizable(True)
        self.cards_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cards_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cards_scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollArea > QWidget > QWidget { background-color: transparent; }
        """)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setAlignment(Qt.AlignCenter)

        self.cards_scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.cards_scroll_area, stretch=1)

        # Continue button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white; border: none;
                padding: 14px 32px; font-size: 16px;
                font-weight: bold; border-radius: 8px;
            }}
            QPushButton:hover {{ background-color: #0ea572; }}
            QPushButton:disabled {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_muted']};
            }}
        """)
        self.continue_btn.clicked.connect(self._on_continue)
        bottom_layout.addWidget(self.continue_btn)
        bottom_layout.addStretch()
        layout.addLayout(bottom_layout)

    def set_players(self, players: list):
        self._players = players

        # Clear existing cards
        self._cards.clear()
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cards_per_row = min(4, max(1, len(players)))

        for i, player in enumerate(players):
            card = RevealCard()
            card.set_player(player)
            self._cards.append(card)
            self.cards_layout.addWidget(card, i // cards_per_row, i % cards_per_row)

        count = len(players)
        self.title.setText(f"Reveal Your Player{'s' if count != 1 else ''}!")
        self.subtitle.setText(
            f"Click each card to reveal ({count} player{'s' if count != 1 else ''})")

        self.reveal_all_btn.setEnabled(True)
        self.continue_btn.setEnabled(False)

    def _reveal_all(self):
        self.reveal_all_btn.setEnabled(False)
        for i, card in enumerate(self._cards):
            if not card.is_revealed():
                QTimer.singleShot(i * 500, card.reveal)
        QTimer.singleShot(len(self._cards) * 500 + 600, self._check_all_revealed)

    def _check_all_revealed(self):
        if all(card.is_revealed() for card in self._cards):
            self.continue_btn.setEnabled(True)
            self.subtitle.setText("All players revealed! Click Continue to proceed.")

    def _on_continue(self):
        self.finished.emit()

    def get_revealed_players(self) -> list:
        return [card.get_player() for card in self._cards if card.is_revealed()]

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        QTimer.singleShot(100, self._check_all_revealed)
