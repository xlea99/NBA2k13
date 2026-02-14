from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
from spritopia.data_storage.data_storage import d
from spritopia.gui_old.widgets.input_combo_box import InputComboBox
from spritopia.data_storage.player_filter import filterSpriteIDs
from spritopia.gui_old.widgets.player_filter_menu import PlayerFilterMenu
from spritopia.gui_old.data_model import DataModel



class PlayerFinder(QWidget):

    def __init__(self,parent=None,dataModel : DataModel = None):
        super().__init__(parent)

        #region === Basic Structure ===

        self.dataModel = dataModel
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        ezFilterButtonContainer = QWidget()
        self.ezFilterButtonLayout = QHBoxLayout(ezFilterButtonContainer)
        self.ezFilterButtonLayout.setSpacing(0)
        self.ezFilterButtonLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(ezFilterButtonContainer)

        playerSearchAndFilterContainer = QWidget()
        self.playerSearchAndFilterLayout = QHBoxLayout(playerSearchAndFilterContainer)
        self.mainLayout.addWidget(playerSearchAndFilterContainer)

        #endregion === Basic Structure ===

        #region === playerSearchAndFilterContainer ===

        playerSearchAndFilterFont = QFont("Arial",15)
        self.playerInputComboBox = InputComboBox()
        self.playerInputComboBox.setFont(playerSearchAndFilterFont)
        self.playerInputComboBox.currentIndexChanged.connect(self.onPlayerInputComboBoxSelected)
        self.dataModel.availableSidebarSpriteIDsChanged.connect(self.onAvailableSidebarSpriteIDsChanged)
        self.populatePlayerInputComboBox(self.dataModel.availableSidebarSpriteIDs)
        self.onPlayerInputComboBoxSelected()
        self.playerSearchAndFilterLayout.addWidget(self.playerInputComboBox,stretch=19)

        self.filterMenu = PlayerFilterMenu(self)
        self.filterMenu.filterApplied.connect(self.applyFilter)
        self.filterButton = QPushButton()
        self.filterButton.setFont(playerSearchAndFilterFont)
        self.filterButton.setText("▼")
        self.filterButton.setMaximumWidth(40)
        self.filterButton.clicked.connect(self.showFilterMenu)
        self.playerSearchAndFilterLayout.addWidget(self.filterButton,stretch=1)

        #endregion === playerSearchAndFilterContainer ===

        #region === ezFilterButtonContainer ===

        self.ezRosterFilterComboBox = QComboBox()
        self.dataModel.gameDataUpdated.connect(self.onGameDataUpdated)
        self.ezArchetypeFilterComboBox = QComboBox()
        self.ezArchetypeFilterComboBox.addItems(["All Archetypes","Slayer","Vigilante","Medic","Guardian","Engineer","Director"])

        self.defaultFiltersButton = QPushButton()
        self.defaultFiltersButton.setText("Reset to Defaults")

        self.ezFilterButtonLayout.addWidget(self.ezRosterFilterComboBox,stretch=3)
        self.ezFilterButtonLayout.addStretch(1)
        self.ezFilterButtonLayout.addWidget(self.ezArchetypeFilterComboBox,stretch=3)
        self.ezFilterButtonLayout.addStretch(1)
        self.ezFilterButtonLayout.addWidget(self.defaultFiltersButton,stretch=1)

        #endregion === ezFilterButtonContainer ===

        self.onGameDataUpdated()


    #region === Connectors ===

    # Controls updating the data model with the selected player's spriteID.
    def onPlayerInputComboBoxSelected(self):
        self.dataModel.selectedSidebarSpriteID = self.playerInputComboBox.currentData()
    # Controls updating the full list of available spriteIDs when a filter is applied.
    def onAvailableSidebarSpriteIDsChanged(self):
        self.populatePlayerInputComboBox(self.dataModel.availableSidebarSpriteIDs)
    # Updates the rosters dropdown to include all rosters.
    def onGameDataUpdated(self):
        self.ezRosterFilterComboBox.clear()
        self.ezRosterFilterComboBox.addItems(["Any Roster"] + list(self.dataModel.gameData.rosters.keys()))

    #endregion === Connectors ===


    # Simply updates the player input combo box with the given list of spriteIDs.
    def populatePlayerInputComboBox(self,spriteIDList : list):
        self.playerInputComboBox.clear()
        for spriteID in spriteIDList:
            self.playerInputComboBox.addItem(d.players[spriteID].getFullName(), spriteID)


    # Method to apply the filter to the sidebar spriteIDs.
    def applyFilter(self,filterDict):
        spriteIDs = filterSpriteIDs(condition=filterDict)
        self.dataModel.availableSidebarSpriteIDs = spriteIDs
    # Method to simply display the filter menu.
    def showFilterMenu(self):
        pos = self.mapToGlobal(self.rect().topRight())
        self.filterMenu.move(pos + QPoint(10, 0))
        self.filterMenu.exec()







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
