"""
Shared application state for Spritopia GUI.

This module provides a central state manager that widgets can subscribe to
for updates. When the selected player changes, all subscribed widgets are notified.
"""

from PySide6.QtCore import QObject, Signal
from typing import Optional, List, Callable
from spritopia.players.players import Player


class AppState(QObject):
    """
    Central state manager for the application.

    Emits signals when state changes so widgets can react accordingly.
    """

    # Signals
    selected_player_changed = Signal(object)  # Emits Player or None
    player_list_changed = Signal()  # Emits when player roster updates
    picker_updated = Signal()  # Emits when picker slots change

    def __init__(self):
        super().__init__()

        # Currently selected player in the player finder
        self._selected_player: Optional[Player] = None

        # All loaded players
        self._players: List[Player] = []

        # Premier picker state (8 slots, team assignments)
        self._picker_slots: List[Optional[Player]] = [None] * 8
        self._picker_config = {
            "pick_order": [1, 2, 2, 2, 1],  # Default 1-2-2-2-1 draft order
            "team_size": 4,
        }

        # Current game mode
        self._current_mode: str = "premier"

        # Player creation queue
        self._creation_queue: List[dict] = []

    # --- Selected Player ---

    @property
    def selected_player(self) -> Optional[Player]:
        return self._selected_player

    @selected_player.setter
    def selected_player(self, player: Optional[Player]):
        if self._selected_player != player:
            self._selected_player = player
            self.selected_player_changed.emit(player)

    # --- Player List ---

    @property
    def players(self) -> List[Player]:
        return self._players

    def set_players(self, players: List[Player]):
        """Set the full player list."""
        self._players = players
        self.player_list_changed.emit()

    def get_player_by_name(self, first_name: str, last_name: str) -> Optional[Player]:
        """Find a player by first and last name."""
        for player in self._players:
            if player["First_Name"] == first_name and player["Last_Name"] == last_name:
                return player
        return None

    # --- Picker ---

    @property
    def picker_slots(self) -> List[Optional[Player]]:
        return self._picker_slots

    def set_picker_slot(self, index: int, player: Optional[Player]):
        """Set a specific picker slot."""
        if 0 <= index < len(self._picker_slots):
            self._picker_slots[index] = player
            self.picker_updated.emit()

    def clear_picker_slot(self, index: int):
        """Clear a specific picker slot."""
        self.set_picker_slot(index, None)

    def clear_all_picker_slots(self):
        """Clear all picker slots."""
        self._picker_slots = [None] * 8
        self.picker_updated.emit()

    def add_selected_to_picker(self, slot_index: int) -> bool:
        """Add the currently selected player to a picker slot."""
        if self._selected_player is None:
            return False

        # Check if player is already in picker
        if self._selected_player in self._picker_slots:
            return False

        self.set_picker_slot(slot_index, self._selected_player)
        return True

    def get_team(self, team_num: int) -> List[Player]:
        """Get players for a specific team (1 or 2)."""
        team_size = self._picker_config["team_size"]
        if team_num == 1:
            return [p for p in self._picker_slots[:team_size] if p is not None]
        else:
            return [p for p in self._picker_slots[team_size:] if p is not None]

    # --- Picker Config ---

    @property
    def picker_config(self) -> dict:
        return self._picker_config

    def set_pick_order(self, order: List[int]):
        """Set the pick order (e.g., [1, 2, 2, 2, 1])."""
        self._picker_config["pick_order"] = order

    # --- Game Mode ---

    @property
    def current_mode(self) -> str:
        return self._current_mode

    @current_mode.setter
    def current_mode(self, mode: str):
        self._current_mode = mode

    # --- Creation Queue ---

    @property
    def creation_queue(self) -> List[dict]:
        return self._creation_queue

    def add_to_creation_queue(self, player_data: dict):
        """Add a player to the creation queue."""
        self._creation_queue.append(player_data)

    def clear_creation_queue(self):
        """Clear the creation queue."""
        self._creation_queue.clear()

    def pop_from_creation_queue(self) -> Optional[dict]:
        """Remove and return the first player from the queue."""
        if self._creation_queue:
            return self._creation_queue.pop(0)
        return None


# Global singleton instance
_app_state: Optional[AppState] = None


def get_app_state() -> AppState:
    """Get the global app state instance."""
    global _app_state
    if _app_state is None:
        _app_state = AppState()
    return _app_state
