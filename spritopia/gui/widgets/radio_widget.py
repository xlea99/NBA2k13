"""
Radio Widget - Compact music player for the Spritopia radio system.

Displays current song, provides playback controls, and allows station switching.
Features Spotify-style scrolling text and seekable progress bar.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QSlider, QSizePolicy, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import QFont, QPainter, QFontMetrics, QColor

from spritopia.gui.theme import COLORS


class MarqueeLabel(QWidget):
    """
    A label that scrolls horizontally when text is too long to fit.
    Spotify-style smooth scrolling with pause at ends.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._offset = 0.0
        self._text_width = 0
        self._paused_at_start = True
        self._pause_counter = 0
        self._scroll_speed = 0.8
        self._pause_duration = 80  # Frames to pause at each end
        self._gap = 60  # Gap between repeated text

        self._font = QFont()
        self._font.setPointSize(11)
        self._color = QColor(COLORS['text_primary'])
        self._is_bold = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_scroll)
        self._timer.start(25)  # 40fps

        # Ensure we have a minimum size
        self.setMinimumHeight(20)

    def setText(self, text: str):
        if text != self._text:
            self._text = text
            self._offset = 0.0
            self._paused_at_start = True
            self._pause_counter = 0
            self._calculate_text_width()
            self.update()

    def text(self) -> str:
        return self._text

    def setFont(self, font: QFont):
        self._font = font
        self._calculate_text_width()
        self.update()

    def setColor(self, color: str):
        self._color = QColor(color)
        self.update()

    def setBold(self, bold: bool):
        self._is_bold = bold
        self._font.setBold(bold)
        self._calculate_text_width()
        self.update()

    def setPointSize(self, size: int):
        self._font.setPointSize(size)
        self._calculate_text_width()
        self.update()

    def _calculate_text_width(self):
        fm = QFontMetrics(self._font)
        self._text_width = fm.horizontalAdvance(self._text)

    def _needs_scroll(self) -> bool:
        return self._text_width > self.width() - 4  # Small margin

    def _update_scroll(self):
        if not self._text or not self._needs_scroll():
            if self._offset != 0:
                self._offset = 0
                self.update()
            return

        if self._paused_at_start:
            self._pause_counter += 1
            if self._pause_counter >= self._pause_duration:
                self._paused_at_start = False
                self._pause_counter = 0
            return

        # Scroll
        self._offset += self._scroll_speed

        # Check if we've scrolled past the text + gap
        scroll_reset_point = self._text_width + self._gap
        if self._offset >= scroll_reset_point:
            self._offset = 0
            self._paused_at_start = True

        self.update()

    def paintEvent(self, event):
        if not self._text:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(self._font)
        painter.setPen(self._color)

        # Get font metrics for vertical centering
        fm = QFontMetrics(self._font)
        text_height = fm.height()
        y = (self.height() + fm.ascent() - fm.descent()) // 2

        if self._needs_scroll():
            # Draw scrolling text
            x = int(-self._offset)
            painter.drawText(x, y, self._text)

            # Draw repeated text for seamless loop
            x2 = x + self._text_width + self._gap
            if x2 < self.width():
                painter.drawText(x2, y, self._text)
        else:
            # Static text, left aligned
            painter.drawText(2, y, self._text)

        painter.end()


class SeekableProgressBar(QWidget):
    """
    A clickable/draggable progress bar for seeking through the song.
    """

    seeked = Signal(int)  # Emits position in milliseconds

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._maximum = 100
        self._is_dragging = False
        self._handle_radius = 5
        self._padding = 6  # Padding on left/right for handle
        self.setFixedHeight(14)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)

    def setValue(self, value: int):
        if not self._is_dragging:
            self._value = max(0, min(value, self._maximum))
            self.update()

    def setMaximum(self, maximum: int):
        self._maximum = max(1, maximum)
        self.update()

    def _get_track_rect(self) -> QRect:
        """Get the rectangle for the track (accounting for handle padding)."""
        return QRect(
            self._padding,
            (self.height() - 4) // 2,
            self.width() - (self._padding * 2),
            4
        )

    def _get_position_from_x(self, x: int) -> int:
        """Convert x position to value."""
        track = self._get_track_rect()
        relative_x = x - track.left()
        ratio = max(0, min(1, relative_x / track.width()))
        return int(ratio * self._maximum)

    def _get_x_from_value(self) -> int:
        """Convert value to x position."""
        track = self._get_track_rect()
        if self._maximum <= 0:
            return track.left()
        ratio = self._value / self._maximum
        return int(track.left() + ratio * track.width())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._value = self._get_position_from_x(event.pos().x())
            self.update()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self._value = self._get_position_from_x(event.pos().x())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._is_dragging:
            self._is_dragging = False
            pos = self._get_position_from_x(event.pos().x())
            self._value = pos
            self.seeked.emit(pos)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track = self._get_track_rect()

        # Background track with subtle inset
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 80))
        painter.drawRoundedRect(track, 2, 2)

        # Progress fill with gradient
        if self._maximum > 0:
            fill_width = int((self._value / self._maximum) * track.width())
            if fill_width > 0:
                fill_rect = QRect(track.left(), track.top(), fill_width, track.height())
                painter.setBrush(QColor(COLORS['accent_primary']))
                painter.drawRoundedRect(fill_rect, 2, 2)

        # Handle/knob with subtle glow effect
        handle_x = self._get_x_from_value()
        handle_y = self.height() // 2

        # Glow
        painter.setBrush(QColor(COLORS['accent_primary']))
        painter.setOpacity(0.3)
        painter.drawEllipse(
            handle_x - self._handle_radius - 2,
            handle_y - self._handle_radius - 2,
            (self._handle_radius + 2) * 2,
            (self._handle_radius + 2) * 2
        )

        # Main handle
        painter.setOpacity(1.0)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(
            handle_x - self._handle_radius,
            handle_y - self._handle_radius,
            self._handle_radius * 2,
            self._handle_radius * 2
        )

        painter.end()


class HeaderRadioWidget(QFrame):
    """
    Compact radio widget designed to fit in the header bar.
    Features scrolling text and seekable progress bar with a polished embossed look.

    Layout:
    - Song info (title/artist) on left
    - Playback controls (prev/play/next) with progress bar below in center
    - Station selector with volume slider below on right
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._radio = None
        self._is_playing = True
        self._current_song_length = 0
        self._setup_ui()

        # Update timer for song info
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_display)
        self._update_timer.start(250)  # Update every 250ms

    def _setup_ui(self):
        # Embossed container style - subtle inset effect
        self.setStyleSheet(f"""
            HeaderRadioWidget {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {COLORS['bg_dark']},
                    stop: 0.1 {COLORS['bg_light']},
                    stop: 0.9 {COLORS['bg_light']},
                    stop: 1 {COLORS['bg_dark']}
                );
                border: 1px solid {COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(14)

        # LEFT: Song info with marquee in a subtle card
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                border: none;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(1)
        info_layout.setContentsMargins(10, 3, 10, 3)

        # Song title (scrolling)
        self.song_label = MarqueeLabel()
        self.song_label.setFixedWidth(160)
        self.song_label.setFixedHeight(18)
        self.song_label.setBold(True)
        self.song_label.setPointSize(11)
        self.song_label.setText("Loading...")
        info_layout.addWidget(self.song_label)

        # Artist (scrolling)
        self.artist_label = MarqueeLabel()
        self.artist_label.setFixedWidth(160)
        self.artist_label.setFixedHeight(14)
        self.artist_label.setColor(COLORS['text_muted'])
        self.artist_label.setPointSize(8)
        self.artist_label.setText("")
        info_layout.addWidget(self.artist_label)

        layout.addWidget(info_frame)

        # CENTER: Controls + Progress bar stacked vertically
        controls_column = QVBoxLayout()
        controls_column.setSpacing(3)
        controls_column.setContentsMargins(0, 0, 0, 0)

        # Playback controls row
        controls_row = QHBoxLayout()
        controls_row.setSpacing(2)
        controls_row.setAlignment(Qt.AlignCenter)

        # Previous button
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setFixedSize(26, 24)
        self.prev_btn.setStyleSheet(self._control_btn_style())
        self.prev_btn.clicked.connect(self._on_previous)
        self.prev_btn.setToolTip("Previous")
        controls_row.addWidget(self.prev_btn)

        # Play/Pause button - larger and more prominent
        self.play_btn = QPushButton("⏸")
        self.play_btn.setFixedSize(30, 24)
        self.play_btn.setStyleSheet(self._play_btn_style())
        self.play_btn.clicked.connect(self._on_play_pause)
        self.play_btn.setToolTip("Play/Pause")
        controls_row.addWidget(self.play_btn)

        # Next button
        self.next_btn = QPushButton("⏭")
        self.next_btn.setFixedSize(26, 24)
        self.next_btn.setStyleSheet(self._control_btn_style())
        self.next_btn.clicked.connect(self._on_next)
        self.next_btn.setToolTip("Next")
        controls_row.addWidget(self.next_btn)

        controls_column.addLayout(controls_row)

        # Progress bar + time below controls
        progress_row = QHBoxLayout()
        progress_row.setSpacing(6)
        progress_row.setContentsMargins(0, 0, 0, 0)

        self.current_time = QLabel("0:00")
        self.current_time.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']}; font-family: monospace;")
        self.current_time.setFixedWidth(28)
        self.current_time.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        progress_row.addWidget(self.current_time)

        # Seekable progress bar
        self.progress_bar = SeekableProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.seeked.connect(self._on_seek)
        progress_row.addWidget(self.progress_bar)

        self.total_time = QLabel("0:00")
        self.total_time.setStyleSheet(f"font-size: 9px; color: {COLORS['text_muted']}; font-family: monospace;")
        self.total_time.setFixedWidth(28)
        self.total_time.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        progress_row.addWidget(self.total_time)

        controls_column.addLayout(progress_row)

        layout.addLayout(controls_column)

        # Subtle vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-width: 1px;")
        separator.setFixedHeight(32)
        layout.addWidget(separator)

        # RIGHT: Station selector + Volume
        right_column = QVBoxLayout()
        right_column.setSpacing(4)
        right_column.setContentsMargins(0, 2, 0, 2)

        # Station selector with icon
        station_row = QHBoxLayout()
        station_row.setSpacing(2)
        station_row.setContentsMargins(0, 0, 0, 0)

        station_icon = QLabel("📻")
        station_icon.setStyleSheet(f"font-size: 11px;")
        station_icon.setFixedWidth(16)
        station_row.addWidget(station_icon)

        self.station_combo = QComboBox()
        self.station_combo.setFixedWidth(90)
        self.station_combo.setFixedHeight(18)
        self.station_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                padding: 1px 6px;
                font-size: 10px;
                color: {COLORS['text_primary']};
            }}
            QComboBox:hover {{
                border-color: {COLORS['accent_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 14px;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                selection-background-color: {COLORS['accent_primary']};
            }}
        """)
        self.station_combo.currentIndexChanged.connect(self._on_station_changed)
        station_row.addWidget(self.station_combo)

        right_column.addLayout(station_row)

        # Volume slider with icon
        volume_row = QHBoxLayout()
        volume_row.setSpacing(2)
        volume_row.setContentsMargins(0, 0, 0, 0)

        volume_icon = QLabel("🔊")
        volume_icon.setStyleSheet(f"font-size: 10px;")
        volume_icon.setFixedWidth(16)
        volume_row.addWidget(volume_icon)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedWidth(78)
        self.volume_slider.setFixedHeight(14)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: rgba(255, 255, 255, 0.12);
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['accent_primary']};
                width: 10px;
                margin: -3px 0;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal:hover {{
                background: #5aadff;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['accent_primary']};
                border-radius: 2px;
            }}
        """)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        self.volume_slider.setToolTip("Volume")
        volume_row.addWidget(self.volume_slider)

        right_column.addLayout(volume_row)

        layout.addLayout(right_column)

    def _control_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.05);
                color: {COLORS['text_secondary']};
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 0px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
                background-color: rgba(255, 255, 255, 0.1);
                border-color: {COLORS['border_light']};
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """

    def _play_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5aadff,
                    stop: 1 {COLORS['accent_primary']}
                );
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0px;
                font-size: 17px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #6bb8ff,
                    stop: 1 #5aadff
                );
            }}
            QPushButton:pressed {{
                background: {COLORS['accent_primary']};
            }}
        """

    def set_radio(self, radio):
        """Connect to a Radio instance."""
        self._radio = radio
        self._populate_stations()
        self._update_display()
        # Sync volume slider to actual radio volume
        if radio:
            self.volume_slider.setValue(100)
            radio.volume(100)

    def _populate_stations(self):
        if not self._radio:
            return

        self.station_combo.blockSignals(True)
        self.station_combo.clear()

        for station_id, station_info in self._radio.stations.items():
            self.station_combo.addItem(station_info['name'], station_id)

        if self._radio.currentStation:
            idx = self.station_combo.findData(self._radio.currentStation)
            if idx >= 0:
                self.station_combo.setCurrentIndex(idx)

        self.station_combo.blockSignals(False)

    def _format_time(self, ms: int) -> str:
        """Format milliseconds as M:SS."""
        seconds = int(ms / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

    def _update_display(self):
        if not self._radio:
            return

        try:
            if self._radio._Radio__activeSong:
                song_id = self._radio._Radio__activeSong
                song_info = self._radio.catalog.get(song_id, {})

                song_name = song_info.get('name', 'Unknown')
                artist = song_info.get('artist', 'Unknown Artist')
                length_ms = song_info.get('length', 0)
                self._current_song_length = length_ms

                self.song_label.setText(song_name)
                self.artist_label.setText(artist)

                # Update progress
                current_ms = self._radio._Radio__player.get_time()
                if current_ms < 0:
                    current_ms = 0

                self.progress_bar.setMaximum(length_ms)
                self.progress_bar.setValue(current_ms)

                self.current_time.setText(self._format_time(current_ms))
                self.total_time.setText(self._format_time(length_ms))
            else:
                self.song_label.setText("No song playing")
                self.artist_label.setText("")
                self.current_time.setText("--:--")
                self.total_time.setText("--:--")
                self.progress_bar.setValue(0)

            # Sync play/pause button with actual radio state
            actually_playing = self._radio._Radio__player.is_playing()
            if actually_playing != self._is_playing:
                self._is_playing = actually_playing
                self.play_btn.setText("⏸" if actually_playing else "▶")

            # Sync station combo
            if self._radio.currentStation:
                current_idx = self.station_combo.findData(self._radio.currentStation)
                if current_idx >= 0 and current_idx != self.station_combo.currentIndex():
                    self.station_combo.blockSignals(True)
                    self.station_combo.setCurrentIndex(current_idx)
                    self.station_combo.blockSignals(False)

        except Exception:
            pass

    def _on_play_pause(self):
        if not self._radio:
            return

        if self._is_playing:
            self._radio.pause()
            self.play_btn.setText("▶")  # Play symbol
            self._is_playing = False
        else:
            self._radio.play()
            self.play_btn.setText("⏸")  # Pause symbol
            self._is_playing = True

    def _on_next(self):
        if self._radio:
            self._radio.next()

    def _on_previous(self):
        if self._radio:
            self._radio.previous()

    def _on_station_changed(self, index):
        if not self._radio:
            return

        station_id = self.station_combo.currentData()
        if station_id and station_id != self._radio.currentStation:
            self._radio.station(station_id)

    def _on_volume_changed(self, value):
        if self._radio:
            self._radio.volume(value)

    def _on_seek(self, position_ms: int):
        """Handle seek from progress bar."""
        if self._radio:
            # Convert to timestamp string format for the radio
            seconds = position_ms // 1000
            minutes = seconds // 60
            secs = seconds % 60
            timestamp = f"{minutes}:{secs:02d}"
            try:
                self._radio.timestamp(timestamp)
            except Exception:
                pass


# Keep the old RadioWidget for backwards compatibility
class RadioWidget(HeaderRadioWidget):
    """Alias for HeaderRadioWidget."""
    pass


class CompactRadioWidget(QFrame):
    """
    Even more compact radio widget for tight spaces.
    Just shows song name and basic controls.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._radio = None
        self._is_playing = True
        self._setup_ui()

        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_display)
        self._update_timer.start(500)

    def _setup_ui(self):
        self.setStyleSheet(f"""
            CompactRadioWidget {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 6px;
            }}
        """)
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        self.play_btn = QPushButton("\u23F8")  # Unicode: Pause symbol
        self.play_btn.setFixedSize(28, 28)
        self.play_btn.setFont(QFont("Segoe UI Symbol", 10))
        self.play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background-color: #3b8bdb;
            }}
        """)
        self.play_btn.clicked.connect(self._on_play_pause)
        layout.addWidget(self.play_btn)

        self.song_label = QLabel("Loading...")
        self.song_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_primary']};")
        layout.addWidget(self.song_label, stretch=1)

        self.next_btn = QPushButton("\u23ED")  # Unicode: Next track symbol
        self.next_btn.setFixedSize(24, 24)
        self.next_btn.setFont(QFont("Segoe UI Symbol", 10))
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: none;
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
            }}
        """)
        self.next_btn.clicked.connect(self._on_next)
        layout.addWidget(self.next_btn)

    def set_radio(self, radio):
        self._radio = radio
        self._update_display()

    def _update_display(self):
        if not self._radio:
            return

        try:
            if self._radio._Radio__activeSong:
                song_id = self._radio._Radio__activeSong
                song_info = self._radio.catalog.get(song_id, {})
                song_name = song_info.get('name', 'Unknown')
                artist = song_info.get('artist', '')

                display = f"{song_name}"
                if artist:
                    display += f" - {artist}"

                if len(display) > 40:
                    display = display[:37] + "..."

                self.song_label.setText(display)
            else:
                self.song_label.setText("No song")
        except Exception:
            pass

    def _on_play_pause(self):
        if not self._radio:
            return

        if self._is_playing:
            self._radio.pause()
            self.play_btn.setText("\u25B6")  # Unicode: Play symbol
            self._is_playing = False
        else:
            self._radio.play()
            self.play_btn.setText("\u23F8")  # Unicode: Pause symbol
            self._is_playing = True

    def _on_next(self):
        if self._radio:
            self._radio.next()
