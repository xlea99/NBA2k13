from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from spritopia.gui.app_state import globalAppState
from spritopia.data_storage import data_storage as d


# This is the top half widget the displays basic player description and graphics.
class PlayerBio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        # Connect to AppState to update on spriteID change
        globalAppState.currentSpriteIDChanged.connect(self.update_player_bio)
        self.update_player_bio(globalAppState.currentSpriteID)

    def setup_ui(self):
        layout = QVBoxLayout(self)  # Main layout for the widget

        # Top layout for Faction and Artifact images
        topLayout = QHBoxLayout()
        self.factionImage = QLabel()
        self.factionImage.setFixedSize(75, 75)  # Fixed small size for images
        self.playerName = AutoResizeLabel()
        playerNameFont = QFont("Arial", 20)
        playerNameFont.setBold(True)
        self.playerName.setFont(playerNameFont)
        self.playerName.setMinimumWidth(200)
        self.playerName.setMaximumWidth(200)
        self.playerName.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
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

    def update_player_bio(self, currentSpriteID):
        thisPlayer = d.d.players[currentSpriteID]
        factionPixmap = QPixmap(paths["graphics"] / f"FactionIcons/{thisPlayer['Faction']}.png")
        self.factionImage.setPixmap(factionPixmap.scaled(75, 75, Qt.KeepAspectRatio,Qt.SmoothTransformation))

        # Set artifact image here.
        self.artifactImage.clear()
        artifactPMod = None
        if(len(thisPlayer["PMods"]) > 0):
            for pmod in thisPlayer["PMods"]:
                if(pmod["Type"]["TypeName"] == "Artifact"):
                    artifactPMod = pmod
                    break
        if(artifactPMod is not None):
            artifactPixmap = QPixmap(paths["graphics"] / artifactPMod["Image"])
            self.artifactImage.setPixmap(artifactPixmap.scaled(75,75,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            self.artifactImage.setToolTip(artifactPMod["Description"])

        # Set player name
        self.playerName.setText(f"{thisPlayer['First_Name']} {thisPlayer['Last_Name']}")
        # Update Archetype with coloring based on value
        archetype = thisPlayer["Archetype_Name"]
        self.archetypeLabel.setText(f"<i>{archetype}</i>")
        # Example to set color, adjust as necessary
        self.archetypeLabel.setStyleSheet(f"color: {self.get_archetype_color(archetype)};")

        # Update Rarity with coloring based on value
        rarity = thisPlayer["Rarity"]
        self.rarityLabel.setText(f"<b>{rarity}</b>")
        # Example to set color, adjust as necessary
        self.rarityLabel.setStyleSheet(f"color: {self.get_rarity_color(rarity)};")

        # Update Description
        description = thisPlayer["Biography"]
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