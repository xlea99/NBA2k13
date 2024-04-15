from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.players import archetypes
from spritopia.gui.app_state import globalAppState
from spritopia.data_storage import data_storage as d

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

        # Connect to global spriteID change
        globalAppState.currentSpriteIDChanged.connect(self.reorder_attributes)
        globalAppState.currentSpriteIDChanged.connect(self.update_attributes)
        self.reorder_attributes(globalAppState.currentSpriteID)
        self.update_attributes(globalAppState.currentSpriteID)

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

    def reorder_attributes(self, spriteID):
        thisArchetype = d.d.players[spriteID]["Archetype_Name"]

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
        for widget in archetypeOrders[thisArchetype]:
            self.layout.addWidget(widget)
    def update_attributes(self, spriteID):
        thisPlayer = d.d.players[spriteID]

        attributeAccessors = {
            "Offensive" : archetypes.OFFENSIVE_ATTRIBUTES,
            "Defensive" : archetypes.DEFENSIVE_ATTRIBUTES,
            "Control": archetypes.CONTROL_ATTRIBUTES,
            "General" : archetypes.GENERAL_ATTRIBUTES
        }


        for attribute,label in self.offensiveAttributes.items():
            label.setText(f"{archetypes.MAPPED_ATTRIBUTES[attribute]}: {thisPlayer[attribute]}")
        for attribute,label in self.defensiveAttributes.items():
            label.setText(f"{archetypes.MAPPED_ATTRIBUTES[attribute]}: {thisPlayer[attribute]}")
        for attribute,label in self.controlAttributes.items():
            label.setText(f"{archetypes.MAPPED_ATTRIBUTES[attribute]}: {thisPlayer[attribute]}")
        for attribute,label in self.generalAttributes.items():
            label.setText(f"{archetypes.MAPPED_ATTRIBUTES[attribute]}: {thisPlayer[attribute]}")