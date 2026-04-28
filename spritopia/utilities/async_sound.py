import threading
import sys
import os
from spritopia.common.logger import log
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
import pygame
sys.stdout.close()
sys.stdout = original_stdout


# Global lock to prevent simultaneous plays
playsoundAsyncLock = threading.Lock()

# This method simply plays a target sound asynchronously (meaning, on a separate thread.)
def playsoundAsync(soundFilePath):
    try:
        def sound_player(path):
            # Load the sound file
            sound = pygame.mixer.Sound(path)
            # Play the sound asynchronously
            sound.play()
            # Wait for the sound to finish playing
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
    except pygame.error:
        log.warning("Pygame not initialized!!!!!")

    # Start a new thread to play the sound
    threading.Thread(target=sound_player, args=(soundFilePath,)).start()