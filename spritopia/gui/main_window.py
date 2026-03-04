"""
Main Window for Spritopia GUI.

The main application window containing:
- Header: Branding (left), Radio (center), Save button (right)
- Left sidebar: Player Finder (persistent)
- Top: Game mode tabs (Premier, Gauntlet, League)
- Main content: Changes based on current mode and selection
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTabWidget, QStackedWidget, QSplitter, QLabel, QMessageBox, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from spritopia.gui.theme import STYLESHEET, COLORS
from spritopia.gui.app_state import get_app_state
from spritopia.gui.audio import get_audio_player
from spritopia.gui.widgets.player_finder import PlayerFinderWidget
from spritopia.gui.widgets.radio_widget import HeaderRadioWidget
from spritopia.gui.radio_tab import RadioTab
from spritopia.gui.tournament_tab import TournamentTab
from spritopia.gui.premier.play import PlayWidget
from spritopia.gui.premier.home import PremierHomeWidget
from spritopia.gui.create_player.create_player_page import CreatePlayerPage
from spritopia.gui.save_manager import SaveButton, get_save_manager
from spritopia.gui.stats import StatsCenterWidget

from spritopia.data_storage.data_storage import d
from spritopia.common.logger import log


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spritopia")
        self.setMinimumSize(1280, 720)

        # Apply theme
        self.setStyleSheet(STYLESHEET)

        self._radio = None
        self._tracker_bridge = None
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()
        self._init_radio()
        self._init_tracker_bridge()

        self.showMaximized()

    def _setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main vertical layout (header + content)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Header bar with branding, radio, and save button
        header = self._create_header()
        outer_layout.addWidget(header)

        # Main content area with splitter for sidebar + content
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_dark']};
                width: 1px;
            }}
        """)

        # Left sidebar: Player Finder
        self.player_finder = PlayerFinderWidget()
        splitter.addWidget(self.player_finder)

        # Right side: Mode tabs + content
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Game mode tabs
        self.mode_tabs = QTabWidget()
        self.mode_tabs.setTabPosition(QTabWidget.North)
        self.mode_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 14px 32px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:disabled {{
                color: {COLORS['text_muted']};
            }}
        """)

        # Premier tab with sub-navigation
        self.premier_widget = self._create_premier_widget()
        self.mode_tabs.addTab(self.premier_widget, "Premier")

        # Gauntlet tab (placeholder, disabled for now)
        gauntlet_placeholder = self._create_placeholder("Gauntlet", "Coming soon...")
        self.mode_tabs.addTab(gauntlet_placeholder, "Gauntlet")
        self.mode_tabs.setTabEnabled(1, False)

        # League tab (placeholder, disabled for now)
        league_placeholder = self._create_placeholder("League", "Coming soon...")
        self.mode_tabs.addTab(league_placeholder, "League")
        self.mode_tabs.setTabEnabled(2, False)

        # Tournaments tab
        self.tournament_tab = TournamentTab()
        self.mode_tabs.addTab(self.tournament_tab, "Tournaments")

        # Radio tab
        self.radio_tab = RadioTab()
        self.mode_tabs.addTab(self.radio_tab, "Radio")

        right_layout.addWidget(self.mode_tabs)
        splitter.addWidget(right_container)

        # Set initial splitter sizes (sidebar: 350px, content: rest)
        splitter.setSizes([350, 1570])
        splitter.setStretchFactor(0, 0)  # Sidebar doesn't stretch
        splitter.setStretchFactor(1, 1)  # Content stretches

        main_layout.addWidget(splitter)
        outer_layout.addWidget(main_container, stretch=1)

    def _create_header(self) -> QWidget:
        """Create the header bar with branding (left), radio (center), save (right)."""
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(16)

        # LEFT: Logo/Title
        branding = QHBoxLayout()
        branding.setSpacing(12)

        title = QLabel("SPRITOPIA")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {COLORS['accent_primary']};
            letter-spacing: 3px;
        """)
        branding.addWidget(title)

        subtitle = QLabel("NBA 2K13")
        subtitle.setStyleSheet(f"""
            font-size: 10px;
            color: {COLORS['text_muted']};
            padding-top: 6px;
        """)
        branding.addWidget(subtitle)

        layout.addLayout(branding)

        # Spacer
        layout.addStretch()

        # Vertical divider 1 (between branding and radio)
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.VLine)
        divider1.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-width: 1px;")
        divider1.setFixedHeight(36)
        layout.addWidget(divider1)

        layout.addStretch()

        # CENTER: Radio widget
        self.radio_widget = HeaderRadioWidget()
        layout.addWidget(self.radio_widget)

        # Spacer
        layout.addStretch()

        # Vertical divider 2 (between radio and save)
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.VLine)
        divider2.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-width: 1px;")
        divider2.setFixedHeight(36)
        layout.addWidget(divider2)

        layout.addStretch()

        # RIGHT: Save button
        self.save_button = SaveButton()
        layout.addWidget(self.save_button)

        return header

    def _create_premier_widget(self) -> QWidget:
        """Create the Premier mode widget with sub-navigation."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sub-navigation bar
        subnav = QWidget()
        subnav.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_medium']};
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
        """)
        subnav_layout = QHBoxLayout(subnav)
        subnav_layout.setContentsMargins(16, 8, 16, 8)
        subnav_layout.setSpacing(8)

        # Sub-nav buttons
        self.premier_nav_buttons = {}
        nav_items = [
            ("home", "Home"),
            ("play", "Play"),
            ("create", "Create Player"),
            ("stats", "Stats"),
        ]

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['text_secondary']};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_primary']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['accent_primary']};
                    color: white;
                }}
            """)
            btn.clicked.connect(lambda checked, k=key: self._on_premier_nav(k))
            subnav_layout.addWidget(btn)
            self.premier_nav_buttons[key] = btn

        subnav_layout.addStretch()
        layout.addWidget(subnav)

        # Stacked widget for content
        self.premier_stack = QStackedWidget()

        # Home page
        self.premier_home = PremierHomeWidget()
        self.premier_home.open_picker.connect(lambda: self._on_premier_nav("play"))
        self.premier_home.open_create_player.connect(lambda: self._on_premier_nav("create"))
        self.premier_home.open_stats.connect(lambda: self._on_premier_nav("stats"))
        self.premier_stack.addWidget(self.premier_home)

        # Play page (setup + picker)
        self.play_widget = PlayWidget()
        self.play_widget.match_started.connect(self._on_match_started)
        self.play_widget.match_ended.connect(self._on_match_ended)
        self.play_widget.slot_filter_changed.connect(self._on_slot_filter_changed)
        self.play_widget.excluded_updated.connect(self._on_draft_excluded_updated)
        self.premier_stack.addWidget(self.play_widget)

        # Create player page
        self.create_player_page = CreatePlayerPage()
        self.create_player_page.players_created.connect(self._on_players_created)
        self.premier_stack.addWidget(self.create_player_page)

        # Stats page
        self.stats_center = StatsCenterWidget()
        self.stats_center.player_selected_external.connect(self._on_stats_player_selected)
        self.premier_stack.addWidget(self.stats_center)

        layout.addWidget(self.premier_stack)

        # Set initial nav state
        self.premier_nav_buttons["home"].setChecked(True)

        return container

    def _create_placeholder(self, title: str, description: str) -> QWidget:
        """Create a placeholder widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        return widget

    def _on_premier_nav(self, key: str):
        """Handle Premier sub-navigation."""
        # Update button states
        for btn_key, btn in self.premier_nav_buttons.items():
            btn.setChecked(btn_key == key)

        # Switch page
        page_map = {
            "home": 0,
            "play": 1,
            "create": 2,
            "stats": 3,
        }
        if key in page_map:
            self.premier_stack.setCurrentIndex(page_map[key])

    def _connect_signals(self):
        """Connect signals between components."""
        # Save manager signals
        save_manager = get_save_manager()
        save_manager.save_started.connect(self._on_save_started)
        save_manager.save_completed.connect(self._on_save_completed)

        # Tournament draft ↔ sidebar
        self.tournament_tab.draft_excluded_updated.connect(self._on_tournament_draft_excluded)
        self.tournament_tab.slot_filter_changed.connect(self._on_tournament_slot_filter)
        self.player_finder.player_selected.connect(self.tournament_tab.on_sidebar_pick)

    def _load_initial_data(self):
        """Load initial data from the database."""
        try:
            # Open databases
            d.playersDB_Open()
            d.playersDB_DownloadPlayers()

            # Load players into app state
            app_state = get_app_state()
            players = list(d.players.values())
            app_state.set_players(players)

            # Update player finder
            self.player_finder.set_players(players)

            log.info(f"Loaded {len(players)} players")
        except Exception as e:
            log.error(f"Failed to load initial data: {e}")
            QMessageBox.warning(
                self,
                "Data Load Error",
                f"Failed to load player data: {e}\n\nThe application may not function correctly."
            )

    def _init_radio(self):
        """Initialize the radio system."""
        try:
            # Import radio - note: it auto-starts playing
            from spritopia.utilities.radio import r as radio
            self._radio = radio
            self.radio_widget.set_radio(radio)
            self.radio_tab.set_radio(radio)
            log.info("Radio initialized")
        except Exception as e:
            log.warning(f"Failed to initialize radio: {e}")

    def _init_tracker_bridge(self):
        """Initialize the tracker bridge for 2K13 integration."""
        try:
            from spritopia.gui.tracker_bridge import get_tracker_bridge
            self._tracker_bridge = get_tracker_bridge()
            self._tracker_bridge.connection_changed.connect(self._on_tracker_connection_changed)
            log.info("Tracker bridge initialized")
        except Exception as e:
            self._tracker_bridge = None
            log.warning(f"Failed to initialize tracker bridge: {e}")

    def _on_save_started(self):
        """Handle save process starting - disable UI."""
        self.setEnabled(False)

    def _on_save_completed(self):
        """Handle save process completing - re-enable UI."""
        self.setEnabled(True)

    def _on_tracker_connection_changed(self, connected):
        """Log tracker connection state changes."""
        if connected:
            log.info("Connected to NBA 2K13")
        else:
            log.info("Disconnected from NBA 2K13")

    def _on_players_created(self, players: list):
        """Handle newly created players."""
        # Update the player finder with new players
        self.player_finder.set_players(list(get_app_state().players))

        # Log success
        names = [f"{p['First_Name']} {p['Last_Name']}" for p in players]
        log.info(f"Created {len(players)} new players: {names}")

    def _on_match_started(self, config: dict):
        """Push game-mode constraints from match setup into the player finder."""
        self.player_finder.set_game_constraints(config)

    def _on_match_ended(self):
        """Clear game-mode constraints when returning to setup."""
        self.player_finder.clear_game_constraints()

    def _on_draft_excluded_updated(self, ids: set):
        """Remove picked/banned players from the sidebar search during a draft."""
        self.player_finder.set_draft_excluded(ids)

    def _on_slot_filter_changed(self, archetype: str):
        """Apply or clear the active pick slot's archetype restriction on the finder."""
        self.player_finder.set_slot_archetype(archetype or None)

    def _on_tournament_draft_excluded(self, ids: set):
        """Hide already-picked players from the sidebar during a tournament draft."""
        self.player_finder.set_draft_excluded(ids)

    def _on_tournament_slot_filter(self, archetype: str):
        """Apply or clear an archetype filter on the sidebar for tournament draft slots."""
        self.player_finder.set_slot_archetype(archetype or None)

    def _on_stats_player_selected(self, sprite_id: int):
        """Handle player selection from stats center - select in player finder."""
        self.player_finder.select_player_by_id(sprite_id)

    def closeEvent(self, event):
        """Handle window close."""
        # Check for pending changes
        save_manager = get_save_manager()
        if save_manager.has_pending_changes:
            reply = QMessageBox.warning(
                self,
                "Unsaved Changes",
                f"You have {save_manager.pending_count} unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                save_manager.execute_all(self)
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return

        # Cleanup
        try:
            get_audio_player().stop()
        except:
            pass
        try:
            if self._tracker_bridge:
                self._tracker_bridge._poll_timer.stop()
        except:
            pass

        event.accept()
