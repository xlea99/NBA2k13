from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.players.factions import dbDict as factionDBDict
from spritopia.gui.widgets.input_combo_box import InputComboBox
from spritopia.data_storage.data_storage import d
from spritopia.players.players import Player
from spritopia.players import factions

LABEL_WIDTH = 80

# Class for providing the Picker Menu
class PremierCreateAPlayer(QWidget):

    # Initialize UI and tracking variables
    def __init__(self,parent=None):
        super().__init__(parent)
        self.createAPlayerLayout = QHBoxLayout(self)

        # region === Create A Player Queue ===

        # Player queue listbox
        createAPlayerQueueContainer = QWidget()
        createAPlayerQueueLayout = QVBoxLayout(createAPlayerQueueContainer)
        createAPlayerQueueLabel = QLabel("Queue")
        font = QFont("Arial", 12, QFont.Bold)
        createAPlayerQueueLabel.setFont(font)
        createAPlayerQueueLabel.setAlignment(Qt.AlignCenter)
        self.createAPlayerQueueListWidget = QListWidget()
        createAPlayerQueueLayout.addWidget(createAPlayerQueueLabel)
        createAPlayerQueueLayout.addWidget(self.createAPlayerQueueListWidget)

        # Clear button
        clearButton = QPushButton(" Remove Selected")
        clearButton.clicked.connect(self.removeSelectedPlayer)
        clearButton.setIcon(QIcon(str(paths["graphics"] / "warning.png")))
        createAPlayerQueueLayout.addWidget(clearButton)

        # Execute button
        executeButton = QPushButton("Execute")
        executeButton.clicked.connect(self.executeQueue)
        createAPlayerQueueLayout.addWidget(executeButton)

        self.createAPlayerLayout.addWidget(createAPlayerQueueContainer,1)

        # endregion === Create a Player Queue ===

        # region === Create A Player Console ===

        # Create A PLayer Header
        createAPlayerConsoleContainer = QWidget()
        createAPlayerConsoleLayout = QVBoxLayout(createAPlayerConsoleContainer)
        createAPlayerConsoleLabel = QLabel("Create A Player")
        font = QFont("Arial", 22, QFont.Bold)
        createAPlayerConsoleLabel.setFont(font)
        createAPlayerConsoleLabel.setAlignment(Qt.AlignCenter)
        createAPlayerConsoleLayout.addWidget(createAPlayerConsoleLabel)

        # First name selection
        firstNameSelectionContainer = QWidget()
        firstNameSelectionLayout = QHBoxLayout(firstNameSelectionContainer)
        firstNameSelectionLabel = QLabel("First: ")
        self.firstNameSelectionLineEdit = QLineEdit()
        self.firstNameSelectionLineEdit.setPlaceholderText("Random")
        self.firstNameSelectionLineEdit.setMaximumWidth(200)  # Set a maximum width
        firstNameSelectionLayout.addStretch()  # Add stretch before widgets
        firstNameSelectionLayout.addWidget(firstNameSelectionLabel)
        firstNameSelectionLayout.addWidget(self.firstNameSelectionLineEdit)
        firstNameSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(firstNameSelectionContainer)

        # Last name selection
        lastNameSelectionContainer = QWidget()
        lastNameSelectionLayout = QHBoxLayout(lastNameSelectionContainer)
        lastNameSelectionLabel = QLabel("Last: ")
        self.lastNameSelectionLineEdit = QLineEdit()
        self.lastNameSelectionLineEdit.setPlaceholderText("Random")
        self.lastNameSelectionLineEdit.setMaximumWidth(200)  # Set a maximum width
        lastNameSelectionLayout.addStretch()  # Add stretch before widgets
        lastNameSelectionLayout.addWidget(lastNameSelectionLabel)
        lastNameSelectionLayout.addWidget(self.lastNameSelectionLineEdit)
        lastNameSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(lastNameSelectionContainer)

        # Archetype
        archetypeSelectionContainer = QWidget()
        archetypeSelectionLayout = QHBoxLayout(archetypeSelectionContainer)
        archetypeSelectionLabel = QLabel("Archetype: ")
        self.archetypeSelectionComboBox = QComboBox()
        self.archetypeSelectionComboBox.addItems(["Random", "Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"])
        archetypeSelectionLayout.addStretch()  # Add stretch before widgets
        archetypeSelectionLayout.addWidget(archetypeSelectionLabel)
        archetypeSelectionLayout.addWidget(self.archetypeSelectionComboBox)
        archetypeSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(archetypeSelectionContainer)

        # Faction selection
        factionSelectionContainer = QWidget()
        factionSelectionLayout = QHBoxLayout(factionSelectionContainer)
        factionSelectionLabel = QLabel("Faction: ")
        self.factionSelectionComboBox = QComboBox()
        allFactions = list(factionDBDict["Factions"].keys())
        allFactions.sort()
        allFactions.insert(0,"Random")
        self.factionSelectionComboBox.addItems(allFactions)
        factionSelectionLayout.addStretch()  # Add stretch before widgets
        factionSelectionLayout.addWidget(factionSelectionLabel)
        factionSelectionLayout.addWidget(self.factionSelectionComboBox)
        factionSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(factionSelectionContainer)

        # Random Appearance Selection
        randomAppearanceSelectionContainer = QWidget()
        randomAppearanceSelectionLayout = QHBoxLayout(randomAppearanceSelectionContainer)
        randomAppearanceSelectionLabel = QLabel("Random appearance: ")
        self.randomAppearanceCheckbox = QCheckBox()
        randomAppearanceSelectionLayout.addStretch()  # Add stretch before widgets
        randomAppearanceSelectionLayout.addWidget(randomAppearanceSelectionLabel)
        randomAppearanceSelectionLayout.addWidget(self.randomAppearanceCheckbox)
        randomAppearanceSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(randomAppearanceSelectionContainer)

        # Bio
        bioSelectionContainer = QWidget()
        bioSelectionLayout = QHBoxLayout(bioSelectionContainer)
        self.bioSelectionTextEdit = QTextEdit()
        self.bioSelectionTextEdit.setPlaceholderText("Enter player biography here, or leave blank to randomize...")
        bioSelectionLayout.addWidget(self.bioSelectionTextEdit)
        createAPlayerConsoleLayout.addWidget(bioSelectionContainer)

        # Queue Section
        queueSectionContainer = QWidget()
        queueSectionLayout = QHBoxLayout(queueSectionContainer)
        queueButton = QPushButton("Queue")
        queueButton.clicked.connect(self.queuePlayerForCreation)
        queueSectionLayout.addStretch()  # Add stretch before the button to center it (optional)
        queueSectionLayout.addWidget(queueButton)
        queueSectionLayout.addStretch()  # Add stretch after the button to center it (optional)
        createAPlayerConsoleLayout.addWidget(queueSectionContainer)



        self.createAPlayerLayout.addWidget(createAPlayerConsoleContainer,2)

        # Function to update the color theme
        def update_color_theme(archetype):
            color_themes = {
                "Random": {
                    "background": "#333333",  # Dark grey
                    "text": "#E0E0E0",  # Light grey text
                    "input_background": "#424242",  # Darker grey for input fields
                    "border": "1px solid #606060",  # Medium grey border
                    "checkbox_background": "#424242",  # Background for checkboxes
                    "checkbox_border": "1px solid #606060",  # Border for checkboxes
                },
                "Slayer": {
                    "background": "#3e60ad",  # Blue
                    "text": "#E0E0E0",  # Light grey text
                    "input_background": "#424242",  # Darker grey for input fields
                    "border": "1px solid #7180a3",  # Medium blue border
                    "checkbox_background": "#424242",  # Background for checkboxes
                    "checkbox_border": "1px solid #7180a3",  # Border for checkboxes
                },
                "Vigilante": {
                    "background": "#3C763D",  # Soft green
                    "text": "#F9F9F9",  # Very light grey text
                    "input_background": "#4D926F",  # Muted green for input fields
                    "border": "1px solid #4D926F",  # Matching green border
                    "checkbox_background": "#4D926F",  # Background for checkboxes
                    "checkbox_border": "1px solid #4D926F",  # Border for checkboxes
                },
                "Medic": {
                    "background": "#a94442",  # Soft red
                    "text": "#FFFFFF",  # White text
                    "input_background": "#D36E70",  # Muted red for input fields
                    "border": "1px solid #D36E70",  # Matching red border
                    "checkbox_background": "#D36E70",  # Background for checkboxes
                    "checkbox_border": "1px solid #D36E70",  # Border for checkboxes
                },
                "Guardian": {
                    "background": "#FFFFFF",  # Pure white
                    "text": "#000000",  # Black text
                    "input_background": "#FFFFFF",  # White for input fields
                    "border": "1px solid #000000",  # Black border
                    "checkbox_background": "#FFFFFF",  # Background for checkboxes
                    "checkbox_border": "1px solid #000000",  # Border for checkboxes
                },
                "Engineer": {
                    "background": "#b85d09",  # Darkened orange
                    "text": "#FFFFFF",  # White text
                    "input_background": "#cc7a00",  # Darker orange for input fields
                    "border": "1px solid #cc7a00",  # Matching orange border
                    "checkbox_background": "#cc7a00",  # Background for checkboxes
                    "checkbox_border": "1px solid #cc7a00",  # Border for checkboxes
                },
                "Director": {
                    "background": "#9467BD",  # Soft purple
                    "text": "#FFFFFF",  # White text
                    "input_background": "#B09EC7",  # Muted purple for input fields
                    "border": "1px solid #B09EC7",  # Matching purple border
                    "checkbox_background": "#B09EC7",  # Background for checkboxes
                    "checkbox_border": "1px solid #B09EC7",  # Border for checkboxes
                }
            }
            theme = color_themes.get(archetype,
                                     {"background": "#FFFFFF", "text": "#000000", "input_background": "#CCCCCC",
                                      "border": "1px solid #000000"})  # Default to white if not found
            createAPlayerConsoleContainer.setStyleSheet(f"""
                QWidget {{ 
                    background-color: {theme['background']}; 
                    color: {theme['text']};
                }}
                QLineEdit, QComboBox, QTextEdit {{ 
                    background-color: {theme['input_background']}; 
                    color: {theme['text']}; 
                    border: {theme['border']};
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 16px;
                }}
                QCheckBox {{
                    font-size: 16px;  # Larger font size for better readability
                    color: {theme['text']};  # Text color
                    spacing: 5px;  # Space between checkbox and label
                }}
                QCheckBox::indicator {{
                    width: 20px;  # Increase width of the checkbox
                    height: 20px;  # Increase height of the checkbox
                }}
                QCheckBox::indicator:checked {{
                    background-color: {theme['checkbox_background']};  # Background when checked
                    border: {theme['checkbox_border']};
                }}
                QCheckBox::indicator:unchecked {{
                    background-color: {theme['checkbox_background']};  # Background when unchecked
                    border: {theme['checkbox_border']};
                }}
                QLabel {{
                    color: {theme['text']};
                    border: none;
                }}
            """)

        # Connect the signal
        self.archetypeSelectionComboBox.currentTextChanged.connect(update_color_theme)

        update_color_theme("Random")

        # endregion === Create A Player Console ===

        # region === Create A Player Roster Statistics ===

        # Roster Stats section
        createAPlayerRosterStatsContainer = QWidget()
        createAPlayerRosterStatsLayout = QVBoxLayout(createAPlayerRosterStatsContainer)

        # Roster Stats title
        rosterStatsLabel = QLabel("Roster Stats")
        font = QFont("Arial", 16, QFont.Bold)  # Larger font size
        rosterStatsLabel.setFont(font)
        rosterStatsLabel.setAlignment(Qt.AlignCenter)
        createAPlayerRosterStatsLayout.addWidget(rosterStatsLabel)

        # Statistic labels with initial values
        #TODO in case you change how "Premier" is identified, IE not by roster but by tag, change this
        archetypeStats = {"Slayer" : 0,"Vigilante" : 0,"Medic" : 0,"Guardian" : 0,"Engineer" : 0,"Director" : 0,"Total" : 0}
        currentPremierSpriteIDs = set(d.rosters["Premier"]["SpriteIDs"].values())
        for spriteID,player in d.players.items():
            if(spriteID in currentPremierSpriteIDs):
                archetypeStats[player["Archetype_Name"]] += 1
                archetypeStats["Total"] += 1

        for archetypeName, archetypeCount in archetypeStats.items():
            statLayout = QHBoxLayout()
            archetypeNameLabel = QLabel(archetypeName)
            archetypeCountLabel = QLabel(str(archetypeCount))
            if(archetypeName == "Total"):
                font = QFont("Arial", 12)  # Slightly larger than normal
                font.setBold(True)
            else:
                font = QFont("Arial", 12)  # Slightly larger than normal
            archetypeNameLabel.setFont(font)
            archetypeCountLabel.setFont(font)
            statLayout.addWidget(archetypeNameLabel)
            statLayout.addWidget(archetypeCountLabel)
            createAPlayerRosterStatsLayout.addLayout(statLayout)



        self.createAPlayerLayout.addWidget(createAPlayerRosterStatsContainer, 1)

        # endregion === Create A Player Roster Statistics ===


    # This function is run when the "queue" button is clicked, to add a player to the creation queue
    def queuePlayerForCreation(self,event):
        playerFirstName = self.firstNameSelectionLineEdit.text() if self.firstNameSelectionLineEdit.text() != "" else "???"
        playerLastName = self.lastNameSelectionLineEdit.text() if self.lastNameSelectionLineEdit.text() != "" else "???"
        playerArchetype = self.archetypeSelectionComboBox.currentText()
        playerFaction = self.factionSelectionComboBox.currentText()
        isPlayerRandGenFace = self.randomAppearanceCheckbox.isChecked()
        playerBio = self.bioSelectionTextEdit.toPlainText() if self.bioSelectionTextEdit.toPlainText() != "" else "???"

        newPlayerDict = {"FirstName" : playerFirstName,
                         "LastName": playerLastName,
                         "Archetype": playerArchetype,
                         "Faction": playerFaction,
                         "RandGenAppearance": isPlayerRandGenFace,
                         "Bio": playerBio}
        self.addPlayerToQueue(newPlayerDict)

    # Methods for adding and removing player entries to the queue.
    def addPlayerToQueue(self,playerDict):
        thisListItem = QListWidgetItem(f"({playerDict['Archetype'][0]}) {playerDict['FirstName']} {playerDict['LastName']} || Faction: {playerDict['Faction']} || Face: {playerDict['RandGenAppearance']}")
        thisListItem.setData(Qt.UserRole,playerDict)
        self.createAPlayerQueueListWidget.addItem(thisListItem)
    def removeSelectedPlayer(self):
        self.createAPlayerQueueListWidget.takeItem(self.createAPlayerQueueListWidget.currentRow())

    # Method for executing the queue, IE creating new player objects for each entry in the
    # list box, then removing them
    def executeQueue(self):
        allNewPlayers = []
        while self.createAPlayerQueueListWidget.count() > 0:
            thisItem = self.createAPlayerQueueListWidget.takeItem(0)
            if(thisItem):
                thisPlayerDict = thisItem.data(Qt.UserRole)
                newPlayer = Player()

                if(thisPlayerDict["Archetype"] == "Random"):
                    newPlayer.genArchetype()
                else:
                    newPlayer["Archetype"] = thisPlayerDict["Archetype"]

                if(thisPlayerDict["Faction"] == "Random"):
                    newPlayer["Faction"] = factions.getRandomFaction()
                else:
                    newPlayer["Faction"] = thisPlayerDict["Faction"]

                factions.genFactionName(faction=newPlayer["Faction"],player=newPlayer)
                if(thisPlayerDict["FirstName"] != "???"):
                    newPlayer["First_Name"] = thisPlayerDict["FirstName"]
                if(thisPlayerDict["LastName"] != "???"):
                    newPlayer["Last_Name"] = thisPlayerDict["LastName"]

                if(thisPlayerDict["RandGenAppearance"]):
                    factions.genFactionRace(faction=newPlayer["Faction"], player=newPlayer)
                    factions.genFactionGearset(faction=newPlayer["Faction"], player=newPlayer)
                    factions.genFactionHair(faction=newPlayer["Faction"], player=newPlayer)
                    factions.genFactionTattoos(faction=newPlayer["Faction"], player=newPlayer)

                #TODO come back here for random bios once complete
                if(thisPlayerDict["Bio"] == "???"):
                    newPlayer["Biography"] = "PLACEHOLDER_BIO"
                else:
                    newPlayer["Biography"] = thisPlayerDict["Bio"]

                newPlayer.genRarity()
                newPlayer.genAttributes()
                newPlayer.genTendencies()
                newPlayer.genHotspots()
                newPlayer.genHeight()
                newPlayer.genAnimations()
                newPlayer.genPlayStyle()
                newPlayer.genPlayTypes()
                newPlayer.genMisc()
                newPlayer.genArtifact()

                allNewPlayers.append(newPlayer)

        for thisNewPlayer in allNewPlayers:
            print(thisNewPlayer.getOverviewString())

