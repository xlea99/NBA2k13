"""
Create Player Page.

Combines the creation form and pack reveal into a complete workflow.
Changes are queued to the save manager instead of being saved immediately.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QMessageBox, QProgressDialog
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer

from spritopia.players.players import Player
from spritopia.data_storage.data_storage import d
from spritopia.data_storage.roster_io import exportRosterData
from spritopia.common.logger import log
from spritopia.gui.create_player.creation_form import CreationFormWidget
from spritopia.gui.create_player.pack_reveal import PackRevealWidget
from spritopia.gui.app_state import get_app_state
from spritopia.gui.save_manager import get_save_manager, PendingChange, ChangeType


class PlayerGeneratorWorker(QThread):
    """Background worker for generating players."""

    progress = Signal(int, int)  # current, total
    player_generated = Signal(object)  # Player
    finished = Signal(list)  # All players
    error = Signal(str)

    def __init__(self, queue_data: dict, parent=None):
        super().__init__(parent)
        self._queue_data = queue_data
        self._players = []

    def run(self):
        try:
            players_data = self._queue_data.get('players', [])
            total = len(players_data)

            for i, player_info in enumerate(players_data):
                self.progress.emit(i + 1, total)

                # Create new player
                player = Player()

                # Set archetype (or randomize)
                if player_info.get('archetype'):
                    player["Archetype"] = player_info['archetype']
                else:
                    player.genArchetype()

                # Generate rarity
                player.genRarity()

                # Generate all stats based on archetype
                player.genAttributes()
                player.genTendencies()
                player.genHotspots()
                player.genHeight()
                player.genAnimations()
                player.genPlayTypes()
                player.genMisc()

                # Generate artifact (if not Common)
                if player["Rarity"] != "Common":
                    player.genArtifact()

                # Generate faction (this also generates a random name)
                if player_info.get('faction'):
                    player.genFaction(faction=player_info['faction'])
                else:
                    player.genFaction()

                # IMPORTANT: Apply user-specified names AFTER genFaction
                # because genFaction calls genFactionName which overwrites names
                if player_info.get('first_name'):
                    player["First_Name"] = player_info['first_name']
                if player_info.get('last_name'):
                    player["Last_Name"] = player_info['last_name']

                # Mark as having pending updates (needs to be saved)
                player.hasPendingUpdates = True

                self._players.append(player)
                self.player_generated.emit(player)

            self.finished.emit(self._players)

        except Exception as e:
            log.exception(f"Error generating players: {e}")
            self.error.emit(str(e))


class CreatePlayerPage(QWidget):
    """
    Complete Create Player workflow page.

    States:
    1. Form - Queue players for creation
    2. Generating - Show progress while generating
    3. Reveal - Pack opening reveal experience
    4. Done - Return to form

    Changes are queued to the save manager, not saved immediately.
    """

    players_created = Signal(list)  # Emits list of created players

    def __init__(self, parent=None):
        super().__init__(parent)
        self._generated_players = []
        self._queue_data = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Stacked widget for different states
        self.stack = QStackedWidget()

        # Form page
        self.form_widget = CreationFormWidget()
        self.form_widget.generate_requested.connect(self._on_generate_requested)
        self.stack.addWidget(self.form_widget)

        # Reveal page
        self.reveal_widget = PackRevealWidget()
        self.reveal_widget.finished.connect(self._on_reveal_finished)
        self.stack.addWidget(self.reveal_widget)

        layout.addWidget(self.stack)

    def _on_generate_requested(self, queue_data_list: list):
        """Handle generate request from form."""
        if not queue_data_list:
            return

        self._queue_data = queue_data_list[0]
        players_data = self._queue_data.get('players', [])

        if not players_data:
            return

        # Show progress dialog
        self.progress = QProgressDialog(
            "Generating players...",
            None,  # No cancel button
            0,
            len(players_data),
            self
        )
        self.progress.setWindowTitle("Creating Players")
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setMinimumDuration(0)
        self.progress.setValue(0)

        # Start generation in background
        self.worker = PlayerGeneratorWorker(self._queue_data)
        self.worker.progress.connect(self._on_generation_progress)
        self.worker.finished.connect(self._on_generation_finished)
        self.worker.error.connect(self._on_generation_error)
        self.worker.start()

    def _on_generation_progress(self, current: int, total: int):
        """Update progress dialog."""
        self.progress.setValue(current)
        self.progress.setLabelText(f"Generating player {current} of {total}...")

    def _on_generation_finished(self, players: list):
        """Handle generation completion - queue changes to save manager."""
        self.progress.close()
        self._generated_players = players

        save_manager = get_save_manager()
        roster_name = self._queue_data.get('roster_name') if self._queue_data.get('add_to_roster') else None

        # Queue each player to be added to the database
        for player in players:
            name = f"{player['First_Name'] or '???'} {player['Last_Name'] or '???'}"

            # Queue database add
            save_manager.add_change(PendingChange(
                change_type=ChangeType.ADD_PLAYER_TO_DB,
                description=f"Add {name} to Players.db",
                data={'player': player},
                execute_fn=self._execute_add_player_to_db
            ))

            # Queue roster add if requested
            if roster_name:
                save_manager.add_change(PendingChange(
                    change_type=ChangeType.ADD_PLAYER_TO_ROSTER,
                    description=f"Add {name} to {roster_name} CSVs",
                    data={'player': player, 'roster_name': roster_name},
                    execute_fn=self._execute_add_player_to_roster
                ))

        # Queue RedMC sync for the roster (only once, after all player additions)
        if roster_name:
            save_manager.add_change(PendingChange(
                change_type=ChangeType.SYNC_ROSTER_TO_ROS,
                description=f"Sync {roster_name} to .ROS via RedMC",
                data={'roster_name': roster_name},
                execute_fn=self._execute_sync_roster
            ))

        # Add players to app state immediately (they exist in memory)
        # The save manager will persist them to disk later
        app_state = get_app_state()
        current_players = list(app_state.players)
        current_players.extend(players)
        app_state.set_players(current_players)

        log.info(f"Queued {len(players)} players for saving (use Save button to persist)")

        # Clear form and switch to reveal
        self.form_widget.clear_after_generation()
        self.reveal_widget.set_players(players)
        self.stack.setCurrentWidget(self.reveal_widget)

    def _execute_add_player_to_db(self, data: dict):
        """Execute adding a player to the database."""
        player = data['player']
        d.playersDB_AddPlayer(player)
        d.playersDB_UploadPlayers()
        log.debug(f"Saved player to DB: {player['First_Name']} {player['Last_Name']}")

    def _execute_add_player_to_roster(self, data: dict):
        """Execute adding a player to a roster (CSV only, no RedMC yet)."""
        player = data['player']
        roster_name = data['roster_name']

        # Import CSVs if not already loaded
        if roster_name not in d.rosters:
            d.csv_ImportCSVs(roster_name)

        # Find first unused roster ID
        roster_id = int(d.csv_FindFirstUnusedRosterID(roster_name))
        # Update the roster with this player
        d.csv_UpdatePlayer(roster_name, roster_id, player)

        # Export CSVs (to file, not to .ROS yet)
        d.csv_ExportCSVs(roster_name)
        log.debug(f"Added player to roster CSV: {player['First_Name']} {player['Last_Name']} -> {roster_name}")

    def _execute_sync_roster(self, data: dict):
        """Execute syncing roster CSVs to .ROS file via RedMC."""
        roster_name = data['roster_name']
        log.info(f"Starting RedMC sync for roster: {roster_name}")
        exportRosterData(roster_name, d)
        log.info(f"Completed RedMC sync for roster: {roster_name}")

    def _on_generation_error(self, error_msg: str):
        """Handle generation error."""
        self.progress.close()
        QMessageBox.critical(
            self,
            "Generation Error",
            f"Failed to generate players: {error_msg}"
        )

    def _on_reveal_finished(self):
        """Handle reveal completion."""
        # Emit signal with created players
        self.players_created.emit(self._generated_players)

        # Reset state
        self._generated_players = []
        self._queue_data = None

        # Switch back to form
        self.stack.setCurrentWidget(self.form_widget)

    def reset(self):
        """Reset to initial state."""
        self._generated_players = []
        self._queue_data = None
        self.stack.setCurrentWidget(self.form_widget)
