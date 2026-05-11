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
from spritopia.gui.widgets.tracker_hud import TrackerHUDWidget
from spritopia.gui.settings_tab import SettingsTab
from spritopia.gui.radio_tab import RadioTab
from spritopia.gui.tournament_tab import TournamentTab
from spritopia.gui.premier.play import PlayWidget
from spritopia.gui.premier.home import PremierHomeWidget
from spritopia.gui.create_player.create_player_page import CreatePlayerPage
from spritopia.gui.save_manager import SaveButton, get_save_manager
from spritopia.gui.stats import StatsCenterWidget

from spritopia.data_storage.data_storage import d
from spritopia.common.logger import log


# Mode tab index → mode key consumed by RosterRegistry. Tabs not in this map
# (Settings) intentionally do not change the working roster on entry.
_MODE_KEY_BY_TAB_INDEX: dict[int, str] = {
    0: "premier",
    1: "gauntlet",
    2: "league",
    3: "tournaments",
    4: "radio",
}


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
        self._init_roster_registry()

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

        # Gauntlet tab — enabled (placeholder content) so we can exercise the
        # roster registry's mode → working-roster transition for Gauntlet.ROS.
        gauntlet_placeholder = self._create_placeholder("Gauntlet", "Coming soon...")
        self.mode_tabs.addTab(gauntlet_placeholder, "Gauntlet")

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

        # Settings tab — added as a real tab so QTabWidget owns its content,
        # but its tab-bar entry is HIDDEN. The gear button in the corner widget
        # is the only way to navigate to it. This gives us native tab behavior
        # plus visual separation from the gameplay tabs.
        self.settings_tab = SettingsTab()
        self._settings_tab_index = self.mode_tabs.addTab(self.settings_tab, "Settings")
        self.mode_tabs.tabBar().setTabVisible(self._settings_tab_index, False)

        # Gear button — always visible at the right edge of the tab bar.
        self._settings_btn = QPushButton("⚙  Settings")
        self._settings_btn.setCheckable(True)
        self._settings_btn.setCursor(Qt.PointingHandCursor)
        self._settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                border: none;
                padding: 10px 22px;
                margin-left: 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['accent_primary']};
            }}
        """)
        self._settings_btn.toggled.connect(self._on_settings_toggled)
        self.mode_tabs.setCornerWidget(self._settings_btn, Qt.TopRightCorner)

        # When the user clicks a visible (gameplay) tab, un-check the gear so
        # button state stays in sync with what's actually on screen.
        self.mode_tabs.currentChanged.connect(self._on_mode_tab_changed)

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

        # Vertical divider 2 (between radio and tracker HUD)
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.VLine)
        divider2.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-width: 1px;")
        divider2.setFixedHeight(36)
        layout.addWidget(divider2)

        layout.addStretch()

        # RIGHT-CENTER: Live tracker HUD (current 2K13 screen + active roster)
        self.tracker_hud = TrackerHUDWidget()
        layout.addWidget(self.tracker_hud)

        # Vertical divider 3 (between tracker HUD and save)
        divider3 = QFrame()
        divider3.setFrameShape(QFrame.VLine)
        divider3.setStyleSheet(f"background-color: {COLORS['border_dark']}; max-width: 1px;")
        divider3.setFixedHeight(36)
        layout.addWidget(divider3)

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

    def _on_settings_toggled(self, checked: bool):
        """Gear button — switch the (hidden) Settings tab in/out of view."""
        if checked:
            self.mode_tabs.setCurrentIndex(self._settings_tab_index)
        else:
            # Toggling off the gear returns to the previously-selected gameplay tab.
            # If we're still on the Settings tab somehow, default to Premier (0).
            if self.mode_tabs.currentIndex() == self._settings_tab_index:
                self.mode_tabs.setCurrentIndex(0)

    def _on_mode_tab_changed(self, index: int):
        """Keep the gear button in sync AND propagate the active mode to the
        RosterRegistry so the working roster follows the user's mode."""
        is_settings = (index == self._settings_tab_index)
        if self._settings_btn.isChecked() != is_settings:
            self._settings_btn.blockSignals(True)
            self._settings_btn.setChecked(is_settings)
            self._settings_btn.blockSignals(False)

        mode_key = _MODE_KEY_BY_TAB_INDEX.get(index)
        if mode_key is not None:
            registry = get_app_state().roster_registry
            try:
                registry.set_working_roster_for_mode(mode_key)
            except ValueError as e:
                # Roster CSVs missing on disk — not fatal at this stage.
                # Phase 3 will wire a proper "missing roster" startup dialog;
                # for now we log loudly and leave working_roster unchanged.
                log.warning(
                    f"Mode '{mode_key}' wants a roster that isn't available: {e}"
                )

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
        # Probe for pymem up-front. The bridge's lazy-import + bare-except design
        # otherwise swallows ImportError silently and the GUI just shows a muted
        # "Disconnected" status forever — see BUDDY_LOAD_BUG.md for war story.
        try:
            import pymem  # noqa: F401
        except ImportError as e:
            self._tracker_bridge = None
            log.error(f"pymem not installed — tracker integration disabled: {e}")
            QMessageBox.critical(
                self,
                "Missing Dependency: pymem",
                "The 'pymem' package is not installed in this Python environment.\n\n"
                "Without it, Spritopia cannot read or write NBA 2K13's memory — "
                "player loading, live stats, and post-game ripping will all silently "
                "fail.\n\n"
                "Install it with:\n    pip install pymem\n\n"
                "Then restart Spritopia.",
            )
            return

        try:
            from spritopia.gui.tracker_bridge import get_tracker_bridge
            self._tracker_bridge = get_tracker_bridge()
            self._tracker_bridge.connection_changed.connect(self._on_tracker_connection_changed)
            log.info("Tracker bridge initialized")

            # Stand up the incoming-CAP sync coordinator now that the bridge is live.
            from spritopia.gui.cap_sync import CAPSyncCoordinator
            self._cap_sync = CAPSyncCoordinator(self)
        except Exception as e:
            self._tracker_bridge = None
            self._cap_sync = None
            log.warning(f"Failed to initialize tracker bridge: {e}")
            QMessageBox.warning(
                self,
                "Tracker Bridge Failed",
                f"Could not initialize the NBA 2K13 tracker bridge.\n\n"
                f"Error: {e}\n\n"
                f"The GUI will run, but features that depend on 2K13 integration "
                f"(player loading, live stats, ripping) will be unavailable."
            )

    def _init_roster_registry(self):
        """Trigger an initial working-roster set based on the default mode tab.

        Qt's QTabWidget does not fire `currentChanged` on the initial tab,
        so without this manual nudge the registry would stay at None until
        the user actually changes tabs — and the picker, sidebar, etc. would
        all see a `working_roster=None` state on boot. Fire it once now.

        Also wire the tracker bridge's roster_loaded_in_2k signal so that
        whenever the user manually reloads a roster in 2K, any prior staleness
        flag for that roster gets cleared automatically.
        """
        # Capture the result of the initial mode-tab nudge so we can detect
        # whether the default mode's roster failed to import (e.g. Premier.ROS
        # missing on this machine).
        initial_index = self.mode_tabs.currentIndex()
        initial_mode_key = _MODE_KEY_BY_TAB_INDEX.get(initial_index)
        self._on_mode_tab_changed(initial_index)

        if (initial_mode_key is not None
                and get_app_state().roster_registry.working_roster is None):
            # The default mode has a roster mapping but the registry couldn't
            # load it — surface a one-time startup warning so the user knows
            # why downstream features (loading players, etc.) will refuse.
            from spritopia.gui.roster_registry import MODE_ROSTER_MAP
            expected = MODE_ROSTER_MAP.get(initial_mode_key, "?")
            QMessageBox.warning(
                self,
                "Working Roster Missing",
                f"The default mode ({initial_mode_key.title()}) expects roster "
                f"'{expected}', but no CSVs were found in save/roster_csvs/.\n\n"
                f"Open Settings → Manage Data and either:\n"
                f"  • Create '{expected}' from the blank template, or\n"
                f"  • Switch to a different mode whose roster is available.\n\n"
                f"Until then, anything that needs a working roster (loading "
                f"players, drafting, stat filtering) will refuse."
            )

        if self._tracker_bridge is not None:
            self._tracker_bridge.roster_loaded_in_2k.connect(self._on_roster_loaded_in_2k)

    def _on_roster_loaded_in_2k(self, roster_name):
        """User just exited the LoadRoster screen in 2K — mark the freshly-loaded
        roster as in-sync, clearing any prior staleness flag."""
        if not roster_name:
            return
        get_app_state().roster_registry.mark_loaded_in_2k(roster_name)

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
