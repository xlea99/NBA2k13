from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage.data_storage import d
from spritopia.gui.app_state import globalAppState
from spritopia.gui.widgets.input_combo_box import InputComboBox
from spritopia.gui.widgets.player_filter_menu import PlayerFilterMenu
from spritopia.data_storage.player_filter import filterSpriteIDs


# This input combo box provides a simple player selection menu, with the SpriteID of the given player accessible
# using the getCurrentSpriteID method.
class PlayerSelectionBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        # Input box for actual player selection
        self.playerInputComboBox = InputComboBox()
        self.playerInputComboBox.currentIndexChanged.connect(self.onPlayerSelected)
        self.populate(d.players.keys())
        self.spriteID = self.playerInputComboBox.currentData()
        self.onPlayerSelected(self.spriteID)

        # Filter button
        self.filterMenu = PlayerFilterMenu(self)
        self.filterMenu.filterApplied.connect(self.applyFilter)
        self.filterButton = QPushButton()
        self.filterButton.setText("▼")
        self.filterButton.setMaximumWidth(40)
        self.filterButton.setMaximumHeight(40)
        self.filterButton.clicked.connect(self.showFilterMenu)

        self.layout.addWidget(self.playerInputComboBox)
        self.layout.addWidget(self.filterButton)




    # Populate with players' names and spriteIDs.
    def applyFilter(self,filterDict):
        spriteIDs = filterSpriteIDs(condition=filterDict)
        self.populate(spriteIDs=spriteIDs)
    def populate(self,spriteIDs : list):
        self.playerInputComboBox.clear()
        for spriteID in spriteIDs:
            self.playerInputComboBox.addItem(d.players[spriteID].getFullName(), spriteID)

    def getCurrentSpriteID(self):
        return self.playerInputComboBox.currentData()

    def onPlayerSelected(self,index):
        self.spriteID = self.playerInputComboBox.currentData()
        globalAppState.currentSpriteID = self.spriteID

    def showFilterMenu(self):
        pos = self.mapToGlobal(self.rect().topRight())
        self.filterMenu.move(pos + QPoint(10, 0))
        self.filterMenu.exec()
