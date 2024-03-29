import Archetypes
import BaseFunctions as b
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import DataStorage as d
import Player
import Helpers
import sys
from functools import partial

ARCHETYPE_COLORS = {"Slayer" : "blue",
                    "Vigilante" : "green",
                    "Medic" : "red",
                    "Guardian" : "yellow",
                    "Engineer" : "orange",
                    "Director" : "purple",
                    "None" : "white"}

# Helper method to dynamically resize font based on label width.
def dynamicallyResizeFont(label: QLabel,baseFont = None):
    # Retrieve the text from the QLabel
    text = label.text()

    # Use the current width of the label
    current_width = label.maximumWidth()

    # Initial font and font size
    if(baseFont):
        label.setFont(baseFont)
    font = label.font()


    # Create QFontMetrics for measuring text width
    fm = QFontMetrics(font)

    # Check if the text width is within the bounds of current width
    text_width = fm.horizontalAdvance(text)
    while text_width > current_width and font.pointSize() > 1:  # Ensure the font size never goes below 1
        # Decrease font size
        font.setPointSize(font.pointSize() - 1)
        # Update QFontMetrics with the new font size
        fm = QFontMetrics(font)
        # Recalculate text width
        text_width = fm.horizontalAdvance(text)

    # Set the adjusted font to the label
    label.setFont(font)

QApplication.setStyle("Fusion")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        #self.setWindowTitle("Spritopia Presents")
        #self.setGeometry(100, 100, 1200, 900)

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)  # Horizontal layout to hold sidebars and main content
        self.mainLayout.setSpacing(0)  # No space between widgets
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # No margins

        # Initialize left sidebar
        self.leftSidebar = LeftSidebarWidget()
        #sself.leftSidebar.setFixedWidth(400)
        self.mainLayout.addWidget(self.leftSidebar,1)


        # Initialize outer main content area
        self.mainContentOuter = QWidget()
        self.mainContentOuterLayout = QVBoxLayout(self.mainContentOuter)  # Placeholder layout
        self.mainContentOuterLayout.setSpacing(0)  # No space between widgets
        self.mainContentOuterLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.mainLayout.addWidget(self.mainContentOuter,3)  # Add to layout with stretch factor

        self.mainContent = MainContentWidget()
        self.mainContent.setObjectName("mainContentArea")
        self.mainContent.setStyleSheet("#mainContentArea {border: 1px solid black;}")  # TODO TEMP
        #self.mainContent.setStyleSheet("border: 1px solid black;")  # TODO TEMP

        self.bottomContent = QWidget()
        self.bottomContent.setObjectName("bottomContentArea")
        self.bottomContent.setStyleSheet("#bottomContentArea {border: 1px solid black;}") #TODO TEMP

        self.mainContentOuterLayout.addWidget(self.mainContent,2)
        self.mainContentOuterLayout.addWidget(self.bottomContent,1)

        self.leftSidebar.playerComboBox.currentIndexChanged.connect(
            lambda index: self.mainContent.pickerMenuWidget.updateCurrentPlayerSelected(self.leftSidebar.currentPlayer["SpriteID"]))

        self.showMaximized()


#region === Main Content ===

class MainContentWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainContentWidget")

        # Central widget setup
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)  # Main layout

        self.setStyleSheet("""
        #MainContentWidget {
            background-color: #1e3059;
        }
        """)

        self.pickerMenuWidget = PickerMenu(self)
        self.layout.addWidget(self.pickerMenuWidget)

# This is the top half widget the displays basic player description and graphics.
class PlayerCreation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.createAPlayerLabel = QLabel()
        createAPlayerFont = QFont("Arial",30)
        createAPlayerFont.setBold(True)
        self.createAPlayerLabel.setFont(createAPlayerFont)
        self.layout.addWidget(self.createAPlayerLabel)
        self.createAPlayerLabel.setText("Create a New Player")


    def setup_ui(self):
        layout = QVBoxLayout(self)  # Main layout for the widget

        # Top layout for Faction and Artifact images
        topLayout = QHBoxLayout()
        self.factionImage = QLabel()
        self.factionImage.setFixedSize(75, 75)  # Fixed small size for images
        self.playerName = QLabel()
        playerNameFont = QFont("Arial", 20)
        playerNameFont.setBold(True)
        self.playerName.setFont(playerNameFont)
        self.playerName.setMaximumWidth(200)
        self.artifactImage = QLabel()
        self.artifactImage.setFixedSize(75, 75)
        topLayout.addWidget(self.factionImage)
        topLayout.addStretch()
        topLayout.addWidget(self.playerName)
        topLayout.addStretch()
        topLayout.addWidget(self.artifactImage)

        # Middle layout for Archetype and Rarity
        middleLayout = QVBoxLayout()
        self.archetypeLabel = QLabel()
        archetypeLabelFont = QFont("Arial", 10)
        archetypeLabelFont.setItalic(True)
        self.archetypeLabel.setFont(archetypeLabelFont)
        self.archetypeLabel.setAlignment(Qt.AlignCenter)
        self.rarityLabel = QLabel()
        rarityLabelFont = QFont("Arial", 10)
        rarityLabelFont.setBold(True)
        self.rarityLabel.setFont(rarityLabelFont)
        self.rarityLabel.setAlignment(Qt.AlignCenter)
        middleLayout.addWidget(self.archetypeLabel)
        middleLayout.addWidget(self.rarityLabel)
        middleLayout.addStretch()

        # Bottom layout for Description
        self.descriptionLabel = QLabel()
        self.descriptionLabel.setWordWrap(True)  # Allow multi-line text
        self.descriptionLabel.setFont(QFont("Arial", 10))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        # Add sub-layouts to the main layout
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addWidget(self.descriptionLabel)

# Class for providing the Picker Menu
class PickerMenu(QWidget):

    pickOrder = [{"Name" : "Danny picks first 2","Picks" : (1,2)},{"Name" : "Alex picks first 2","Picks" : (1,2)}]

    def __init__(self,parent=None,pickOrder = (0,1,5,6,2,3,7,8,4,9)):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.addStretch(1)

        #region UI Init
        # Mid-section Layout
        self.midLayout = QVBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.midLayout.addSpacerItem(spacer)
        self.selectedPlayerCard = PlayerCard()
        #self.midPlayerSelectButton = QPushButton("Select")
        #self.midPlayerSelectButton.clicked.connect(self.addSelectedPlayer)
        #self.midPlayerRemoveButton = QPushButton("Remove")
        #self.midPlayerRemoveButton.clicked.connect(self.removePreviousSelection)

        self.midLayout.addWidget(self.selectedPlayerCard)
        #self.midLayout.addWidget(self.midPlayerSelectButton)
        #self.midLayout.addWidget(self.midPlayerRemoveButton)
        self.midLayout.addSpacerItem(spacer)

        # Ballerz Team Layout
        self.ballerzLayout = QVBoxLayout()
        ballerzHeader = QLabel("Ballerz")
        ballerzHeader.setAlignment(Qt.AlignCenter)
        self.ballerzLayout.addWidget(ballerzHeader)

        # Ringers Team Layout
        self.ringersLayout = QVBoxLayout()
        ringersHeader = QLabel("Ringers")
        ringersHeader.setAlignment(Qt.AlignCenter)
        self.ringersLayout.addWidget(ringersHeader)

        self.playerCardSections = [{} for i in range(10)]
        for index,playerCardSection in enumerate(self.playerCardSections):
            print(index)
            playerCardSection["MainLayout"] = QHBoxLayout()

            thisPlayerCard = PlayerCard()
            thisBadgesLayout = QVBoxLayout()

            thisActionsLayout = QVBoxLayout()
            addPlayerButton = QPushButton("+")
            addPlayerButton.clicked.connect(partial(self.updatePlayerSlot,index))
            addPlayerButton.setMinimumWidth(0.08 * thisPlayerCard.width())
            addPlayerButton.setMaximumWidth(0.08 * thisPlayerCard.width())
            removePlayerButton = QPushButton("-")
            removePlayerButton.clicked.connect(partial(self.removePlayerSlot,index))
            removePlayerButton.setMinimumWidth(0.08 * thisPlayerCard.width())
            removePlayerButton.setMaximumWidth(0.08 * thisPlayerCard.width())
            thisActionsLayout.addWidget(addPlayerButton)
            thisActionsLayout.addWidget(removePlayerButton)
            thisActionsLayout.addStretch(1)

            playerCardSection["PlayerCard"] = thisPlayerCard
            playerCardSection["BadgesLayout"] = thisBadgesLayout
            playerCardSection["ActionsLayout"] = thisActionsLayout

            if(index < 5):
                playerCardSection["MainLayout"].addLayout(playerCardSection["BadgesLayout"])
                playerCardSection["MainLayout"].addWidget(playerCardSection["PlayerCard"])
                playerCardSection["MainLayout"].addLayout(playerCardSection["ActionsLayout"])
                self.ballerzLayout.addLayout(playerCardSection["MainLayout"])
            else:
                playerCardSection["MainLayout"].addLayout(playerCardSection["ActionsLayout"])
                playerCardSection["MainLayout"].addWidget(playerCardSection["PlayerCard"])
                playerCardSection["MainLayout"].addLayout(playerCardSection["BadgesLayout"])
                self.ringersLayout.addLayout(playerCardSection["MainLayout"])

        # Adding team layouts to the main layout
        self.layout.addLayout(self.ballerzLayout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.midLayout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.ringersLayout)
        self.layout.addStretch(1)

        self.setLayout(self.layout)
        self.setWindowTitle("Player Picker Menu")
        self.resize(500, 300)
        #endregion UI Init


        self.currentSelectorSpriteID = None

        self.currentPhase = 0
        self.phaseOrder = pickOrder


    # Method for updating the center player selection widget.
    def updateCurrentPlayerSelected(self,spriteID = None):
        self.currentSelectorSpriteID = spriteID
        self.selectedPlayerCard.setSpriteID(spriteID)
    # Method for adding a play to the given slot.
    def updatePlayerSlot(self,slot):
        if(self.currentSelectorSpriteID is not None and self.currentSelectorSpriteID in [playerCardSection["PlayerCard"].spriteID for playerCardSection in self.playerCardSections]):
            return False
        else:
            self.playerCardSections[slot]["PlayerCard"].setSpriteID(self.currentSelectorSpriteID)
            return True
    # Method for removing a player from the given slot.
    def removePlayerSlot(self,slot):
        self.playerCardSections[slot]["PlayerCard"].setSpriteID(None)



# Helper class to represent a PickerMenu slot.
class PickerSlot():

    def __init__(self,spriteID = None):
        # Currently assigned player
        self.spriteID = spriteID

        # Whether this slot is "locked" meaning it can't be added to or removed from.
        self.isLocked = True


    # A helper method that attempts to add the given player to this slot. If it is successful (dependent
    # on conditional logic of this particular PickerSlot) it returns True, otherwise False.
    def setSpriteID(self,spriteID):
        if(not self.isLocked):
            self.spriteID = spriteID
            return True
        return False


#endregion === Main Content ===

#region === Left Sidebar ===

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

# This combo box provides a simple player selection menu, with the SpriteID of the given player accessible
# using the getCurrentSpriteID method.
class PlayerSelectionBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.populate()
        self.currentIndexChanged.connect(self.onPlayerSelected)
        self.spriteID = self.currentData()

    def populate(self):
        # Populate with players' names and spriteIDs.
        for spriteID, player in d.d.players.items():
            self.addItem(f"{player['First_Name']} {player['Last_Name']}", spriteID)

    def getCurrentSpriteID(self):
        return self.currentData()

    def onPlayerSelected(self,index):
        self.spriteID = self.currentData()

# This is the top half widget the displays basic player description and graphics.
class PlayerBio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)  # Main layout for the widget

        # Top layout for Faction and Artifact images
        topLayout = QHBoxLayout()
        self.factionImage = QLabel()
        self.factionImage.setFixedSize(75, 75)  # Fixed small size for images
        self.playerName = QLabel()
        playerNameFont = QFont("Arial", 20)
        playerNameFont.setBold(True)
        self.playerName.setFont(playerNameFont)
        self.playerName.setMaximumWidth(200)
        self.artifactImage = QLabel()
        self.artifactImage.setFixedSize(75, 75)
        topLayout.addWidget(self.factionImage)
        topLayout.addStretch()
        topLayout.addWidget(self.playerName)
        topLayout.addStretch()
        topLayout.addWidget(self.artifactImage)

        # Middle layout for Archetype and Rarity
        middleLayout = QVBoxLayout()
        self.archetypeLabel = QLabel()
        archetypeLabelFont = QFont("Arial", 10)
        archetypeLabelFont.setItalic(True)
        self.archetypeLabel.setFont(archetypeLabelFont)
        self.archetypeLabel.setAlignment(Qt.AlignCenter)
        self.rarityLabel = QLabel()
        rarityLabelFont = QFont("Arial", 10)
        rarityLabelFont.setBold(True)
        self.rarityLabel.setFont(rarityLabelFont)
        self.rarityLabel.setAlignment(Qt.AlignCenter)
        middleLayout.addWidget(self.archetypeLabel)
        middleLayout.addWidget(self.rarityLabel)
        middleLayout.addStretch()

        # Bottom layout for Description
        self.descriptionLabel = QLabel()
        self.descriptionLabel.setWordWrap(True)  # Allow multi-line text
        self.descriptionLabel.setFont(QFont("Arial", 10))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        # Add sub-layouts to the main layout
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addWidget(self.descriptionLabel)

    def update_player_bio(self, playerObj):
        factionPixmap = QPixmap(f"{b.paths.graphics}\\FactionIcons\\{playerObj['Faction']}.png") # Assume you get a QPixmap for the faction
        self.factionImage.setPixmap(factionPixmap.scaled(75, 75, Qt.KeepAspectRatio,Qt.SmoothTransformation))

        # Set artifact image here.
        self.artifactImage.clear()
        artifactPMod = None
        if(len(playerObj["PMods"]) > 0):
            for pmod in playerObj["PMods"]:
                if(pmod["Type"]["TypeName"] == "Artifact"):
                    artifactPMod = pmod
                    break
        if(artifactPMod is not None):
            artifactPixmap = QPixmap(f"{b.paths.graphics}\\{artifactPMod['Image']}")
            self.artifactImage.setPixmap(artifactPixmap.scaled(75,75,Qt.KeepAspectRatio,Qt.SmoothTransformation))

        # Set player name
        self.playerName.setText(f"{playerObj['First_Name']} {playerObj['Last_Name']}")
        dynamicallyResizeFont(self.playerName)
        # Update Archetype with coloring based on value
        archetype = playerObj["Archetype_Name"]
        self.archetypeLabel.setText(f"<i>{archetype}</i>")
        # Example to set color, adjust as necessary
        self.archetypeLabel.setStyleSheet(f"color: {self.get_archetype_color(archetype)};")

        # Update Rarity with coloring based on value
        rarity = playerObj["Rarity"]
        self.rarityLabel.setText(f"<b>{rarity}</b>")
        # Example to set color, adjust as necessary
        self.rarityLabel.setStyleSheet(f"color: {self.get_rarity_color(rarity)};")

        # Update Description
        description = playerObj["Biography"]
        self.descriptionLabel.setText(description)

    def get_archetype_color(self, archetype):
        # Define archetype colors
        colors = {
            "Slayer": "#6d1f44",  # Maroon
            "Vigilante": "#06a309",  # Green
            "Medic": "#e53b3b",  # Red
            "Guardian" : "#968242", # Gold
            "Engineer" : "#fc7b02", # Orange
            "Director" : "#1cbfb7", # Turquoise
            "None" : "#000000"  # Black for None
        }
        return colors.get(archetype, "#000000")  # Default to black

    def get_rarity_color(self, rarity):
        # Define rarity colors
        colors = {
            "Common": "#CCCCCC",  # Light grey
            "Rare": "#6666FF",  # Light blue
            "Epic": "#9933FF",  # Purple
            "Legendary": "#FF6600",  # Orange
            "Godlike": "#FFD700",  # Gold
        }
        return colors.get(rarity, "#CCCCCC")  # Default to light grey

# This is one of the bottom half widgets that displays attribute info. It is capable of displaying all player
# attributes, and dynamically rearranging according to archetype.
class PlayerAttributeDisplay(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.setup_offensive_attributes()
        self.setup_defensive_attributes()
        self.setup_control_attributes()
        self.setup_general_attributes()

    def setup_offensive_attributes(self):
        self.offensiveFrame = QFrame(self)
        self.offensiveFrame.setFrameShape(QFrame.StyledPanel)
        self.offensiveLayout = QGridLayout(self.offensiveFrame)

        # Define offensive attributes
        self.offensiveAttributes = {
            "SShtCls": QLabel("Shot Close: N/A"),
            "SLayUp": QLabel("Layup: N/A"),
            "SPstFdaway": QLabel("Post-Fadeaway: N/A"),
            "SPstHook": QLabel("Post-Hook: N/A"),
            "SOLowPost": QLabel("Offensive Low Post: N/A"),
            "SShtMed": QLabel("Shot Medium: N/A"),
            "SSht3PT": QLabel("3 Point Shot: N/A"),
            "SShtInT": QLabel("Shot in Traffic: N/A"),
            "SShtOfD": QLabel("Shot Off Dribble: N/A"),
            "SConsis": QLabel("Consistency: N/A"),
        }

        # Position the labels in the grid
        positions = [(i, j) for i in range(5) for j in range(2)]  # Adjust grid size as needed
        for pos, (name, label) in zip(positions, self.offensiveAttributes.items()):
            self.offensiveLayout.addWidget(label, *pos)

        self.layout.addWidget(self.offensiveFrame)
    def setup_defensive_attributes(self):
        self.defensiveFrame = QFrame(self)
        self.defensiveFrame.setFrameShape(QFrame.StyledPanel)
        self.defensiveLayout = QGridLayout(self.defensiveFrame)

        # Define defensive attributes
        self.defensiveAttributes = {
            "SDLowPost": QLabel("Low-Post Defense: N/A"),
            "SStrength": QLabel("Strength: N/A"),
            "SBlock": QLabel("Block: N/A"),
            "SOnBallD": QLabel("On-Ball Defense: N/A"),
            "SOReb": QLabel("Offensive Rebound: N/A"),
            "SDReb": QLabel("Defensive Rebound: N/A"),
            "SDAwar": QLabel("Defensive Awareness: N/A"),
        }

        # Position the labels in the grid
        positions = [(i, j) for i in range(4) for j in range(2)]
        for pos, (name, label) in zip(positions, self.defensiveAttributes.items()):
            self.defensiveLayout.addWidget(label, *pos)

        # Add the frame to the widget's layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.defensiveFrame)
    def setup_control_attributes(self):
        self.controlFrame = QFrame(self)
        self.controlFrame.setFrameShape(QFrame.StyledPanel)
        self.controlLayout = QGridLayout(self.controlFrame)

        # Define control attributes
        self.controlAttributes = {
            "SOffHDrib": QLabel("Off-hand Dribbling: N/A"),
            "SHands": QLabel("Hands: N/A"),
            "SOAwar": QLabel("Offensive Awareness: N/A"),
            "SBallHndl": QLabel("Ball Handling: N/A"),
            "SHustle": QLabel("Hustle: N/A"),
            "SBallSec": QLabel("Ball Security: N/A"),
            "SPass": QLabel("Pass: N/A"),
            "SSpeed": QLabel("Speed: N/A"),
            "SSteal": QLabel("Steal: N/A"),
            "SQuick": QLabel("Quickness: N/A"),
        }

        # Position the labels in the grid
        positions = [(i, j) for i in range(5) for j in range(2)]  # Adjust grid size as needed
        for pos, (name, label) in zip(positions, self.controlAttributes.items()):
            self.controlLayout.addWidget(label, *pos)

        self.layout.addWidget(self.controlFrame)
    def setup_general_attributes(self):
        self.generalFrame = QFrame(self)
        self.generalFrame.setFrameShape(QFrame.StyledPanel)
        self.generalLayout = QGridLayout(self.generalFrame)

        # Define general attributes
        self.generalAttributes = {
            "SShtIns": QLabel("Shot Inside: N/A"),
            "SDunk": QLabel("Dunk: N/A"),
            "SStdDunk": QLabel("Standing Dunk: N/A"),
            "SVertical": QLabel("Vertical: N/A"),
            "SShtFT": QLabel("Free Throw: N/A"),
            "SStamina": QLabel("Stamina: N/A"),
            "SDurab": QLabel("Durability: N/A"),
            "SPOT": QLabel("Potential: N/A"),
        }

        # Position the labels in the grid
        positions = [(i, j) for i in range(4) for j in range(2)]  # Adjust grid size as needed
        for pos, (name, label) in zip(positions, self.generalAttributes.items()):
            self.generalLayout.addWidget(label, *pos)

        self.layout.addWidget(self.generalFrame)

    def reorder_attributes(self, archetype):

        # Define the order of attributes for each archetype
        archetypeOrders = {
            "Slayer": [self.offensiveFrame, self.controlFrame, self.defensiveFrame, self.generalFrame],
            "Vigilante": [self.offensiveFrame, self.defensiveFrame, self.controlFrame, self.generalFrame],
            "Medic": [self.defensiveFrame, self.controlFrame, self.offensiveFrame, self.generalFrame],
            "Guardian": [self.defensiveFrame, self.offensiveFrame, self.controlFrame, self.generalFrame],
            "Engineer": [self.controlFrame, self.defensiveFrame, self.offensiveFrame, self.generalFrame],
            "Director": [self.controlFrame, self.offensiveFrame, self.defensiveFrame, self.generalFrame],
            "None" : [self.offensiveFrame, self.defensiveFrame, self.controlFrame, self.generalFrame]
        }

        # Clear the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        # Add widgets back in the correct order
        for widget in archetypeOrders[archetype]:
            self.layout.addWidget(widget)

    def update_attributes(self, playerObj):
        attributeAccessors = {
            "Offensive" : Archetypes.OFFENSIVE_ATTRIBUTES,
            "Defensive" : Archetypes.DEFENSIVE_ATTRIBUTES,
            "Control": Archetypes.CONTROL_ATTRIBUTES,
            "General" : Archetypes.GENERAL_ATTRIBUTES
        }


        for attribute,label in self.offensiveAttributes.items():
            label.setText(f"{Archetypes.MAPPED_ATTRIBUTES[attribute]}: {playerObj[attribute]}")
        for attribute,label in self.defensiveAttributes.items():
            label.setText(f"{Archetypes.MAPPED_ATTRIBUTES[attribute]}: {playerObj[attribute]}")
        for attribute,label in self.controlAttributes.items():
            label.setText(f"{Archetypes.MAPPED_ATTRIBUTES[attribute]}: {playerObj[attribute]}")
        for attribute,label in self.generalAttributes.items():
            label.setText(f"{Archetypes.MAPPED_ATTRIBUTES[attribute]}: {playerObj[attribute]}")

# This is one of the bottom half widgets that displays stats info. It displays all relevant player stats.
class PlayerStatsDisplay(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setup_stats_display()

    def setup_stats_display(self):
        self.statsFrame = QFrame(self)
        self.statsFrame.setFrameShape(QFrame.StyledPanel)
        self.statsLayout = QGridLayout(self.statsFrame)

        # Header labels for the grid
        self.headerLabels = ["Stat Name", "Total", "Average"]
        for col, text in enumerate(self.headerLabels):
            label = QLabel(text)
            self.statsLayout.addWidget(label, 0, col)

        # Thick, translucent line
        headerLine = QFrame()
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setStyleSheet("border: 2px solid rgba(0, 0, 0, 50);")  # Adjust color and opacity here
        self.statsLayout.addWidget(headerLine, 1, 0, 1, -1)  # Span across all columns

        self.displayedStatNames = [
            "Games Played",
            "Points",
            "Defensive Rebounds",
            "Offensive Rebounds",
            "Points Per Assist",
            "Assist Count",
            "Steals",
            "Blocks",
            "Turnovers",
            "Insides Made",
            "Insides Attempted",
            "Threes Made",
            "Threes Attempted",
            "Fouls",
            "Dunks",
            "Layups"
        ]

        self.statsLabels = {}
        row_offset = 2  # Adjust for header and thick line
        for i, statName in enumerate(self.displayedStatNames, row_offset):
            rowIndex = i * 2  # Double the row index for each stat to accommodate separators
            self.statsLabels[statName] = {
                "TotalLabel": QLabel("N/A"),
                "AverageLabel": QLabel("N/A")
            }
            self.statsLayout.addWidget(QLabel(statName), rowIndex, 0)
            self.statsLayout.addWidget(self.statsLabels[statName]["TotalLabel"], rowIndex, 1)
            self.statsLayout.addWidget(self.statsLabels[statName]["AverageLabel"], rowIndex, 2)

            # Hazy, semi-transparent line after each row
            if i < len(self.displayedStatNames) + row_offset - 1:  # Avoid adding at the very end
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.setStyleSheet("border: 1px solid rgba(0, 0, 0, 25);")  # Adjust color and opacity here
                self.statsLayout.addWidget(separator, rowIndex + 1, 0, 1, -1)  # Span across all columns

        self.layout.addWidget(self.statsFrame)

    def update_stats(self, spriteID):
        if spriteID not in d.d.stats["Players"]:
            for statName in self.displayedStatNames:
                self.statsLabels[statName]["TotalLabel"].setText("0")
                if(statName == "Games Played"):
                    self.statsLabels[statName]["AverageLabel"].setText(f"-")
                else:
                    self.statsLabels[statName]["AverageLabel"].setText("0.00")
        else:
            for statName in self.displayedStatNames:
                totalValue = d.d.stats["Players"][spriteID]["Totals"].get(statName.replace(" ",""), 0)
                averageValue = d.d.stats["Players"][spriteID]["Averages"].get(statName.replace(" ",""), 0)
                self.statsLabels[statName]["TotalLabel"].setText(str(totalValue))
                if(statName == "Games Played"):
                    self.statsLabels[statName]["AverageLabel"].setText(f"-")
                else:
                    self.statsLabels[statName]["AverageLabel"].setText(f"{averageValue:.2f}")

#endregion === Left Sidebar ===

#region === Bottom Bar ===



#endregion === Bottom Bar ===


# Simple, classy widget for displaying a player's info in a compact way.
class PlayerCard(QWidget):

    NAME_FONT = QFont("Arial",24)
    NAME_FONT.setUnderline(True)
    GAMES_FONT = QFont("Arial",7)

    # Basic setup init method.
    def __init__(self,parent=None,spriteID = None):
        super().__init__(parent)

        self.setObjectName("playerCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.backgroundColor = "grey"
        self.borderColor = "black"

        self.spriteID = spriteID

        self.setMinimumHeight(120)
        self.setMaximumHeight(120)
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

        self.outerLayout = QVBoxLayout(self)
        self.upperHalfLayout = QVBoxLayout()
        self.lowerHalfLayout = QVBoxLayout()
        self.outerLayout.addLayout(self.upperHalfLayout)
        self.outerLayout.addLayout(self.lowerHalfLayout)

        # Upper half config
        self.playerLabelLayout = QHBoxLayout()
        self.playerLabelLayout.setContentsMargins(4,1,4,1)
        self.archetypeLabel = QLabel()
        self.archetypeLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.heightLabel = QLabel()
        self.heightLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.nameLayout = QVBoxLayout()
        self.nameLayout.setSpacing(0)
        self.nameLabel = QLabel()
        self.nameLabel.setMaximumWidth(0.817 * self.width())
        self.nameLabel.setFont(self.NAME_FONT)
        self.nameLabel.setStyleSheet("color: black")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.gamesLabel = QLabel()
        self.gamesLabel.setMaximumWidth(self.nameLabel.maximumWidth())
        self.gamesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.gamesLabel.setFont(self.GAMES_FONT)
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.gamesLabel)
        self.playerLabelLayout.addWidget(self.archetypeLabel)
        self.playerLabelLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.playerLabelLayout.addLayout(self.nameLayout)
        self.playerLabelLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.playerLabelLayout.addWidget(self.heightLabel)

        self.upperHalfLayout.addLayout(self.playerLabelLayout)

        # Lower half config
        self.statsLabel = QLabel()
        self.statsLabel.setMaximumWidth(self.maximumWidth())
        self.statsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.attributeLabel = QLabel()
        self.attributeLabel.setMaximumWidth(self.maximumWidth())
        self.attributeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lowerHalfLayout.addWidget(self.statsLabel)
        self.lowerHalfLayout.addWidget(self.attributeLabel)
        self.lowerHalfLayout.setContentsMargins(1,0,1,1)


        self.outerLayout.setContentsMargins(1, 1, 1, 2)
        self.configureStyle()
        self.setSpriteID(self.spriteID)

    archetypeStatsToShow = {"Slayer" : {""}}
    # This method sets the player to the given SpriteID, and updates the contents.
    def setSpriteID(self,spriteID):
        self.spriteID = spriteID
        if(self.spriteID is None):
            self.archetypeLabel.setText("N")
            self.heightLabel.setText("")
            self.nameLabel.setText("")
            self.gamesLabel.setText("---")
            self.statsLabel.setText("")
            self.attributeLabel.setText("")
            self.configureStyle(borderColor="grey")
        else:
            try:
                statStrings = {"W/L": f"W/L: {d.d.stats['Players'][spriteID]['Averages']['Wins'] * 100:04.1f}%",
                               "Games": f"{d.d.stats['Players'][spriteID]['Totals']['GamesPlayed']} Games, {d.d.stats['Players'][spriteID]['Averages']['Wins'] * 100:04.1f}% W/L",
                               "PPG": f"PPG: {d.d.stats['Players'][spriteID]['Averages']['Points']:<4.1f}",
                               "3P%": f"3P%: {d.d.stats['Players'][spriteID]['Other']['ThreePercentage'] * 100:04.1f}%",
                               "RPG": f"RPG: {d.d.stats['Players'][spriteID]['Averages']['OffensiveRebounds'] + d.d.stats['Players'][spriteID]['Averages']['DefensiveRebounds']:3.1f}",
                               "TPT": f"TPT: {b.getTimeString(d.d.stats['Players'][spriteID]['Other']['TimePerTurnover'])}",
                               "SPG": f"SPG: {d.d.stats['Players'][spriteID]['Averages']['Steals']:.1f}",
                               "APG": f"APG: {d.d.stats['Players'][spriteID]['Averages']['AssistCount']:.1f}",
                               "3PA": f"3PA: {d.d.stats['Players'][spriteID]['Averages']['ThreesAttempted']:.1f}"}
            except KeyError:
                statStrings = {"W/L": "W/L: ???",
                               "Games": "Games: ???",
                               "PPG": "PPG: ???",
                               "3P%": "3P%: ???",
                               "RPG": "RPG: ???",
                               "TPT": "TPT: ???",
                               "SPG": "SPG: ???",
                               "APG": "APG: ???",
                               "3PA": "3PA: ???"}
            attributeStrings = {"Sht3PT": f"Sht3PT: {d.d.players[spriteID]['SSht3PT']:02}",
                                "ShtOffD": f"ShtOffD: {d.d.players[spriteID]['SShtOfD']:02}",
                                "ShtTraff": f"ShtTraff: {d.d.players[spriteID]['SShtInT']:02}",
                                "Speed": f"Speed: {d.d.players[spriteID]['SSpeed']:02}",
                                "OReb": f"OReb: {d.d.players[spriteID]['SOReb']:02}",
                                "DReb": f"DReb: {d.d.players[spriteID]['SDReb']:02}",
                                "BSecure": f"BSecure: {d.d.players[spriteID]['SBallSec']:02}",
                                "Hands": f"Hands: {d.d.players[spriteID]['SHands']:02}",
                                "Consis": f"Consis: {d.d.players[spriteID]['SConsis']:02}",
                                "DAware": f"DAware: {d.d.players[spriteID]['SDAwar']:02}",
                                "OAware": f"OAware: {d.d.players[spriteID]['SOAwar']:02}",
                                "Steal": f"Steal: {d.d.players[spriteID]['SSteal']:02}",
                                "Strength": f"Strength: {d.d.players[spriteID]['SStrength']:02}",
                                "Vertical": f"Vertical: {d.d.players[spriteID]['SVertical']:02}"}

            archetypeStatLabels = {"Slayer" : ("PPG","3P%","3PA","TPT"),
                                   "Vigilante" : ("PPG","3P%","RPG","TPT"),
                                   "Medic" : ("PPG","RPG","APG","TPT"),
                                   "Guardian" : ("PPG","RPG","3P%","TPT"),
                                   "Engineer" : ("PPG","RPG","APG","TPT"),
                                   "Director" : ("PPG","3P%","APG","TPT"),
                                   "None" : ("PPG","3P%","RPG","TPT")}
            archetypeAttributeLabels = {"Slayer" : ("Sht3PT","ShtOffD","Consis","Speed"),
                                        "Vigilante" : ("Sht3PT","ShtTraff","OReb","DReb"),
                                        "Medic" : ("OReb","DReb","Speed","Vertical"),
                                        "Guardian" : ("OReb","DReb","Sht3PT","Speed"),
                                        "Engineer" : ("BSecure","Steal","Speed","Vertical"),
                                        "Director" : ("Speed","BSecure","Steal","Sht3PT"),
                                        "None" : ("Sht3PT","Speed","OReb","DReb")}

            archetypeName = d.d.players[spriteID]['Archetype_Name']

            self.archetypeLabel.setText(f"{archetypeName[0]}")
            self.archetypeLabel.setStyleSheet(f"color: {ARCHETYPE_COLORS[archetypeName]}")
            self.configureStyle(borderColor=ARCHETYPE_COLORS[archetypeName])

            self.heightLabel.setText(f"{d.d.players[spriteID]['HeightFt']}")

            self.nameLabel.setText(d.d.players[spriteID].getFullName())
            dynamicallyResizeFont(self.nameLabel,baseFont=self.NAME_FONT)

            try:
                self.gamesLabel.setText(f"Games: {d.d.stats['Players'][spriteID]['Totals']['GamesPlayed']} (<i>{d.d.stats['Players'][spriteID]['Averages']['Wins']*100:.1f}%</i> W/L)")
            except KeyError:
                self.gamesLabel.setText(f"0 <i>(0.0%)</i>")
            dynamicallyResizeFont(self.gamesLabel,baseFont=self.GAMES_FONT)

            self.statsLabel.setText(" | ".join(statStrings[statType] for statType in archetypeStatLabels[archetypeName]))
            self.attributeLabel.setText(" | ".join(attributeStrings[attributeType] for attributeType in archetypeAttributeLabels[archetypeName]))
            dynamicallyResizeFont(self.statsLabel)
            dynamicallyResizeFont(self.attributeLabel)

    # Helper method to reconfigure the stylesheet of the PlayerCard.
    def configureStyle(self,backgroundColor=None,borderColor=None):
        if(backgroundColor):
            self.backgroundColor = backgroundColor
        if(borderColor):
            self.borderColor = borderColor
        self.setStyleSheet(f".PlayerCard#playerCard {{ border: 3px solid {self.borderColor}; "
                           f"background: {self.backgroundColor}; "
                           f"padding: 3px; }}")


app = QApplication()
#thisPlayer = PlayerCard(spriteID=2)
#thisPlayer.show()
window = MainWindow()
window.show()
sys.exit(app.exec())