import Archetypes
import BaseFunctions as b
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import DataStorage
import Helpers
import sys


class MainPlayerViewerWindow(QMainWindow):
    def __init__(self,dataStorageObject : DataStorage.DataStorage):
        super().__init__()
        self.dataStorageObject = dataStorageObject

        self.setWindowTitle("Spritopia Presents")
        self.setGeometry(100, 100, 400, 800)  # Window size

        # Central widget setup
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)  # Main layout

        # Holder member for the currently selected player.
        self.currentPlayer = None

        # Initialize the PlayerComboBox
        self.playerComboBox = PlayerSelectionBox(dataStorageObject=self.dataStorageObject, parent=self)
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

        # Connect the player selection change signal to update the attribute display
        self.playerComboBox.currentIndexChanged.connect(self.onPlayerSelected)

        self.onPlayerSelected(None)

    def onPlayerSelected(self, index):
        spriteID = self.playerComboBox.getCurrentSpriteID()
        self.currentPlayer = self.dataStorageObject.players[spriteID]
        self.playerBio.update_player_bio(self.currentPlayer)
        self.attributeDisplay.reorder_attributes(self.currentPlayer["Archetype_Name"])
        self.attributeDisplay.update_attributes(self.currentPlayer)

# This combo box provides a simple player selection menu, with the SpriteID of the given player accessible
# using the getCurrentSpriteID method.
class PlayerSelectionBox(QComboBox):
    def __init__(self, dataStorageObject : DataStorage.DataStorage, parent=None):
        super().__init__(parent)
        self.dataStorageObject = dataStorageObject
        self.populate()
        self.currentIndexChanged.connect(self.onPlayerSelected)
        self.spriteID = self.currentData()

    def populate(self):
        # Populate with players' names and spriteIDs.
        for spriteID, player in self.dataStorageObject.players.items():
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

        self.playerName.setText(f"{playerObj['First_Name']} {playerObj['Last_Name']}")

        # Update the artifact image if it exists
        #TODO add description label
        #if playerObj["ArtifactName"] is not None:
        #    artifactPixmap = QPixmap()  # Assume you get a QPixmap for the artifact
        #    self.artifactImage.setPixmap(artifactPixmap.scaled(75, 75, Qt.KeepAspectRatio))
        #else:
        self.artifactImage.clear()

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

    def __init__(self, dataStorageObject : DataStorage.DataStorage, parent=None):
        super().__init__(parent)

        self.dataStorage = dataStorageObject

        self.layout = QVBoxLayout(self)

        self.setup_stats_display()

    def setup_stats_display(self):
        self.statsFrame = QFrame(self)
        self.statsFrame.setFrameShape(QFrame.StyledPanel)
        self.statsLayout = QGridLayout(self.statsFrame)

        # Define stats labels
        self.statsLabels = {
            "Points": QLabel("Points: N/A"),
            "DefensiveRebounds": QLabel("Defensive Rebounds: N/A"),
            "OffensiveRebounds": QLabel("Offensive Rebounds: N/A"),
            "PointsPerAssist": QLabel("Points Per Assist: N/A"),
            "AssistCount": QLabel("Assist Count: N/A"),
            "Steals": QLabel("Steals: N/A"),
            "Blocks": QLabel("Blocks: N/A"),
            "Turnovers": QLabel("Turnovers: N/A"),
            "InsidesMade": QLabel("Insides Made: N/A"),
            "InsidesAttempted": QLabel("Insides Attempted: N/A"),
            "ThreesMade": QLabel("Threes Made: N/A"),
            "ThreesAttempted": QLabel("Threes Attempted: N/A"),
            "Fouls": QLabel("Fouls: N/A"),
            "Dunks": QLabel("Dunks: N/A"),
            "Layups": QLabel("Layups: N/A"),
            "Unknown1": QLabel("Unknown1: N/A"),
            "Unknown2": QLabel("Unknown2: N/A"),
        }

        # Position the labels in the grid
        positions = [(i, j) for i in range(8) for j in range(2)]  # Adjust grid size as needed
        for pos, (name, label) in zip(positions, self.statsLabels.items()):
            self.statsLayout.addWidget(label, *pos)

        self.layout.addWidget(self.statsFrame)

    def update_stats(self, spriteID, statType="Totals"):
        # statType could be "Totals" or "Averages"
        for statName, label in self.statsLabels.items():
            statValue = self.dataStorage.stats[spriteID][statType][statName]
            label.setText(f"{statName.replace('_', ' ')}: {statValue}")


app = QApplication()
window = MainPlayerViewerWindow(DataStorage.d)
window.show()
sys.exit(app.exec())