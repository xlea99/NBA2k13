from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage import data_storage as d
from spritopia.gui.app_state import globalAppState
from spritopia.gui.widgets.input_combo_box import InputComboBox


# This combo box provides a simple player selection menu, with the SpriteID of the given player accessible
# using the getCurrentSpriteID method.
class PlayerSelectionBox(InputComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.populate()
        self.currentIndexChanged.connect(self.onPlayerSelected)
        self.spriteID = self.currentData()
        self.onPlayerSelected(self.spriteID)

    # Populate with players' names and spriteIDs.
    def populate(self): 
        for spriteID, player in d.d.players.items():
            self.addItem(f"{player['First_Name']} {player['Last_Name']}", spriteID)

    def getCurrentSpriteID(self):
        return self.currentData()

    def onPlayerSelected(self,index):
        self.spriteID = self.currentData()
        globalAppState.currentSpriteID = self.spriteID
