from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.players.factions import dbDict as factionDBDict
from spritopia.gui.widgets.input_combo_box import InputComboBox

LABEL_WIDTH = 80

# Class for providing the Picker Menu
class CreateAPlayer(QWidget):

    # Initialize UI and tracking variables
    def __init__(self,parent=None):
        super().__init__(parent)
        self.createAPlayerLayout = QHBoxLayout(self)

        # region === Create A Player Queue ===

        # Player queue listbox
        self.createAPlayerQueueContainer = QWidget()
        self.createAPlayerQueueLayout = QVBoxLayout(self.createAPlayerQueueContainer)
        self.createAPlayerQueueLabel = QLabel("Queue")
        font = QFont("Arial", 12, QFont.Bold)
        self.createAPlayerQueueLabel.setFont(font)
        self.createAPlayerQueueLabel.setAlignment(Qt.AlignCenter)
        self.createAPlayerQueueListWidget = QListWidget()
        self.createAPlayerQueueLayout.addWidget(self.createAPlayerQueueLabel)
        self.createAPlayerQueueLayout.addWidget(self.createAPlayerQueueListWidget)

        # Clear button
        self.clearButton = QPushButton("Clear")
        self.clearButton.setIcon(QIcon("D:/Coding/NBA2k13/assets/graphics/MusicIcons/warning.png"))
        self.createAPlayerQueueLayout.addWidget(self.clearButton)

        # Execute button
        self.executeButton = QPushButton("Execute")
        self.createAPlayerQueueLayout.addWidget(self.executeButton)

        self.createAPlayerLayout.addWidget(self.createAPlayerQueueContainer,1)

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
        firstNameSelectionLineEdit = QLineEdit()
        firstNameSelectionLineEdit.setPlaceholderText("Random")
        firstNameSelectionLineEdit.setMaximumWidth(200)  # Set a maximum width
        firstNameSelectionLayout.addStretch()  # Add stretch before widgets
        firstNameSelectionLayout.addWidget(firstNameSelectionLabel)
        firstNameSelectionLayout.addWidget(firstNameSelectionLineEdit)
        firstNameSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(firstNameSelectionContainer)

        # Last name selection
        lastNameSelectionContainer = QWidget()
        lastNameSelectionLayout = QHBoxLayout(lastNameSelectionContainer)
        lastNameSelectionLabel = QLabel("Last: ")
        lastNameSelectionLineEdit = QLineEdit()
        lastNameSelectionLineEdit.setPlaceholderText("Random")
        lastNameSelectionLineEdit.setMaximumWidth(200)  # Set a maximum width
        lastNameSelectionLayout.addStretch()  # Add stretch before widgets
        lastNameSelectionLayout.addWidget(lastNameSelectionLabel)
        lastNameSelectionLayout.addWidget(lastNameSelectionLineEdit)
        lastNameSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(lastNameSelectionContainer)

        # Archetype
        archetypeSelectionContainer = QWidget()
        archetypeSelectionLayout = QHBoxLayout(archetypeSelectionContainer)
        archetypeSelectionLabel = QLabel("Archetype: ")
        archetypeSelectionComboBox = QComboBox()
        archetypeSelectionComboBox.addItems(["Random", "Slayer", "Vigilante", "Medic", "Guardian", "Engineer", "Director"])
        archetypeSelectionLayout.addStretch()  # Add stretch before widgets
        archetypeSelectionLayout.addWidget(archetypeSelectionLabel)
        archetypeSelectionLayout.addWidget(archetypeSelectionComboBox)
        archetypeSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(archetypeSelectionContainer)

        # Faction selection
        factionSelectionContainer = QWidget()
        factionSelectionLayout = QHBoxLayout(factionSelectionContainer)
        factionSelectionLabel = QLabel("Faction: ")
        factionSelectionComboBox = QComboBox()
        allFactions = list(factionDBDict["Factions"].keys())
        allFactions.sort()
        allFactions.insert(0,"Random")
        factionSelectionComboBox.addItems(allFactions)
        factionSelectionLayout.addStretch()  # Add stretch before widgets
        factionSelectionLayout.addWidget(factionSelectionLabel)
        factionSelectionLayout.addWidget(factionSelectionComboBox)
        factionSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(factionSelectionContainer)

        # Random Appearance Selection
        randomAppearanceSelectionContainer = QWidget()
        randomAppearanceSelectionLayout = QHBoxLayout(randomAppearanceSelectionContainer)
        randomAppearanceSelectionLabel = QLabel("Random appearance: ")
        randomAppearanceCheckbox = QCheckBox()
        randomAppearanceSelectionLayout.addStretch()  # Add stretch before widgets
        randomAppearanceSelectionLayout.addWidget(randomAppearanceSelectionLabel)
        randomAppearanceSelectionLayout.addWidget(randomAppearanceCheckbox)
        randomAppearanceSelectionLayout.addStretch()  # Add stretch after widgets
        createAPlayerConsoleLayout.addWidget(randomAppearanceSelectionContainer)

        # Bio
        bioSelectionContainer = QWidget()
        bioSelectionLayout = QHBoxLayout(bioSelectionContainer)
        bioSelectionTextEdit = QTextEdit()
        bioSelectionTextEdit.setPlaceholderText("Enter player biography here, or leave blank to randomize...")
        bioSelectionLayout.addWidget(bioSelectionTextEdit)
        createAPlayerConsoleLayout.addWidget(bioSelectionContainer)

        # Queue Section
        queueSectionContainer = QWidget()
        queueSectionLayout = QHBoxLayout(queueSectionContainer)
        queueButton = QPushButton("Queue")
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
        archetypeSelectionComboBox.currentTextChanged.connect(update_color_theme)

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
        stats = [("Slayers: ", "0"), ("Vigilantes: ", "0"), ("Medics: ", "0"),
                 ("Guardians: ", "0"), ("Engineers: ", "0"), ("Directors: ", "0")]
        for stat, value in stats:
            statLayout = QHBoxLayout()
            statLabel = QLabel(stat)
            valueLabel = QLabel(value)
            font = QFont("Arial", 12)  # Slightly larger than normal
            statLabel.setFont(font)
            valueLabel.setFont(font)
            statLayout.addWidget(statLabel)
            statLayout.addWidget(valueLabel)
            createAPlayerRosterStatsLayout.addLayout(statLayout)

        # Total players label
        totalPlayersLabel = QLabel("Total players: ")
        totalPlayersValueLabel = QLabel("106")
        totalPlayersLabel.setFont(font)
        totalPlayersValueLabel.setFont(font)
        totalPlayersLayout = QHBoxLayout()
        totalPlayersLayout.addWidget(totalPlayersLabel)
        totalPlayersLayout.addWidget(totalPlayersValueLabel)
        createAPlayerRosterStatsLayout.addLayout(totalPlayersLayout)

        self.createAPlayerLayout.addWidget(createAPlayerRosterStatsContainer, 1)

        # endregion === Create A Player Roster Statistics ===

        #aLabel = QLabel("Beans!")
        #thisFont = QFont("Arial",24)
        #aLabel.setFont(thisFont)
        #self.createAPlayerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.createAPlayerLayout.addWidget(aLabel)

