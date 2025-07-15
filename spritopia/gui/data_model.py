from PySide6.QtCore import QObject, Signal
from spritopia.data_storage.data_storage import d

# Unified object for controlling all data throughout the GUI
class DataModel(QObject):

    # Simple init
    def __init__(self):
        super().__init__()
        self.gameData = d

        self.selectedSidebarSpriteID = 0
        self.availableSidebarSpriteIDs = list(d.players.keys())


    #region === General Data Storage ===

    gameDataUpdated = Signal()

    #endregion === General Data Storage ===

    #region === Player Finder Sidebar ===

    selectedSidebarSpriteIDChanged = Signal()
    availableSidebarSpriteIDsChanged = Signal()

    @property
    def selectedSidebarSpriteID(self):
        return self._selectedSidebarSpriteID
    @selectedSidebarSpriteID.setter
    def selectedSidebarSpriteID(self,spriteID : int):
        if spriteID:
            if spriteID < 0:
                spriteID = 0
            self._selectedSidebarSpriteID = spriteID
            self.selectedSidebarSpriteIDChanged.emit()
            print(f"NEW PLAYER: '{spriteID}'")

    @property
    def availableSidebarSpriteIDs(self):
        return self._availableSidebarSpriteIDs
    @availableSidebarSpriteIDs.setter
    def availableSidebarSpriteIDs(self,spriteIDList : list):
        self._availableSidebarSpriteIDs = spriteIDList
        self.availableSidebarSpriteIDsChanged.emit()

    #endregion === Player Finder Sidebar ===

