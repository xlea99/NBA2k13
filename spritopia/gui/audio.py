"""
Audio playback utilities for Spritopia GUI.
"""

import os
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from spritopia.common.paths import paths


class AudioPlayer:
    """Simple audio player for UI sounds and reveals."""

    def __init__(self):
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._audio_output.setVolume(0.7)

        # Cache paths
        self._audio_path = paths["assets"] / "media" / "common"

    def play(self, filename: str):
        """Play an audio file from the common media folder."""
        filepath = self._audio_path / filename
        if filepath.exists():
            self._player.setSource(QUrl.fromLocalFile(str(filepath)))
            self._player.play()

    def play_click(self):
        """Play the click sound."""
        self.play("Click.ogg")

    def play_rarity_reveal(self, rarity: str):
        """Play the reveal sound for a rarity level."""
        rarity_files = {
            "common": "Common.ogg",
            "rare": "Rare.ogg",
            "epic": "Epic.ogg",
            "legendary": "Legendary.ogg",
            "godlike": "Godlike.mp3",
        }
        filename = rarity_files.get(rarity.lower(), "Common.ogg")
        self.play(filename)

    def play_title(self):
        """Play the title/intro music."""
        self.play("Title.ogg")

    def play_win(self, variant: int = 1):
        """Play a win sound (W1-W13)."""
        variant = max(1, min(13, variant))
        self.play(f"W{variant}.ogg")

    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)."""
        self._audio_output.setVolume(max(0.0, min(1.0, volume)))

    def stop(self):
        """Stop the current audio."""
        self._player.stop()


# Global singleton
_audio_player: Optional[AudioPlayer] = None


def get_audio_player() -> AudioPlayer:
    """Get the global audio player instance."""
    global _audio_player
    if _audio_player is None:
        _audio_player = AudioPlayer()
    return _audio_player
