from PySide6.QtCore import QObject, Signal

class AppState(QObject):
    currentSpriteIDChanged = Signal(int)  # Emits the entire player data

    def __init__(self):
        super().__init__()
        self._currentSpriteID = 0

    @property
    def currentSpriteID(self):
        return self._currentSpriteID

    @currentSpriteID.setter
    def currentSpriteID(self, value):
        if self._currentSpriteID != value:
            self._currentSpriteID = value
            self.currentSpriteIDChanged.emit(value)

# Create a global instance of AppState
globalAppState = AppState()