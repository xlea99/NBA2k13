from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage import data_storage as d
from spritopia.gui.left_sidebar.player_bio import PlayerBio
from spritopia.gui.left_sidebar.player_selection_box import PlayerSelectionBox
from spritopia.gui.left_sidebar.player_stats_display import PlayerStatsDisplay
from spritopia.gui.left_sidebar.player_attribute_display import PlayerAttributeDisplay


class LeftSidebarWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("LeftSidebarWidget")

        # Central widget setup
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)  # Main layout

        #self.setStyleSheet("""
        ##LeftSidebarWidget {
        #    background-color: #939393;
        #}
        #""")
        # Holder member for the currently selected player.
        self.currentPlayer = None

        # Initialize the PlayerComboBox
        self.playerComboBox = PlayerSelectionBox(parent=self)
        self.layout.addWidget(self.playerComboBox)  # Add to layout

        # Initialize the PlayerBio
        self.playerBio = PlayerBio(self)
        self.layout.addWidget(self.playerBio)


        # Initialize the tab widget.
        self.tabWidget = QTabWidget()
        self.layout.addWidget(self.tabWidget)

        # Initialize the AttributeDisplay
        self.attributeDisplay = PlayerAttributeDisplay(self)
        #self.layout.addWidget(self.attributeDisplay)  # Add to layout below the dropdown
        self.tabWidget.addTab(self.attributeDisplay,"Attributes")

        # Intialize the StatsDisplay
        self.statsDisplay = PlayerStatsDisplay(parent=self)
        self.tabWidget.addTab(self.statsDisplay,"Stats")

        # Connect the player selection change signal to update the attribute display
        self.playerComboBox.currentIndexChanged.connect(self.onPlayerSelected)
        self.onPlayerSelected(None)

    def onPlayerSelected(self, index):
        spriteID = self.playerComboBox.getCurrentSpriteID()
        self.currentPlayer = d.d.players[spriteID]
        self.playerBio.update_player_bio(self.currentPlayer)
        self.attributeDisplay.reorder_attributes(self.currentPlayer["Archetype_Name"])
        self.attributeDisplay.update_attributes(self.currentPlayer)
        self.statsDisplay.update_stats(spriteID=self.currentPlayer["SpriteID"])