from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui import const
from spritopia.gui.widgets.player_card import PlayerCard
from spritopia.gui.app_state import globalAppState
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from functools import partial
import random

PREMADE_GAME_MODES = [
    {"Name": "Classic", "Description": "Classic 2K experience - revolving picks, no bans."},
    {"Name": "Smite", "Description": "Smite-style picking, all players allowed, 5 bans each."}
]
DRAFT_TYPES = {
    "Classic": "Bans are done before picks are made. Users take turns selecting one player each until draft has concluded.",
    "Smite": "Half of the total bans are made before picks are made. User 1 gets the first pick, User 2 gets the following two picks, User 1 gets the next pick. The next ban phase commences. Then, User 2 gets one pick, User 1 gets two picks, and User 2 gets the final pick.",
    "Danny-First": "Bans are done before picks are made. Danny selects his entire team first, then Alex drafts his team.",
    "Alex-First": "Bans are done before picks are made. Alex selects his entire team first, then Danny drafts his team.",
    "2-4-2": "Bans are done before picks are made. User 1 gets two picks, User 2 gets 4 picks, User 1 gets the final two picks."}
DRAFT_CONTENT_DESCRIPTIONS = {
    "Normal": "Every pick is normally selected.",
    "Random": "Every pick is randomly selected.",
    "Semi-Random": "Every other pick is random.",
    "Archetypal-Random": "Every pick must be a random pre-selected archetype.",
    "Captains": "First pick is random, every other pick is normal.",
    "Affirmative-Action": "Last pick for each team is random.",
    "Archetype Showdown": "Each user is assigned one archetype that they must build their team with.",
    "Spritopian Duos": "Each user is assigned a shooting archetype and a non-shooting archetype to build their team around.",
    "Chaos": "Every slot is given a random rule. It can be a normal pick, random pick, or random archetype lock."}


class PremierGameOptions(QWidget):

    pickTypeOptions = ["Normal", "Random", "Archetype (Random)", "Archetype (Slayer)", "Archetype (Vigilante)",
                            "Archetype (Medic)", "Archetype (Guardian)", "Archetype (Engineer)", "Archetype (Director)"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)


        self.currentGameMode = PREMADE_GAME_MODES[0]
        self.setupGeneralOptions()
        self.setupPickOptions()



        # region === Game Mode Preset Options ===

        # Game Mode General selection area
        gameModeSelectionContainer = QWidget()
        #gameModeSelectionContainer.setMaximumWidth(220)
        gameModeSelectionLayout = QVBoxLayout(gameModeSelectionContainer)
        self.layout.addWidget(gameModeSelectionContainer)


        # Game Options Caption
        self.gameOptionsTitleGameLabel = AutoResizeLabel("Game Options", autoWrap=True)
        #self.gameOptionsTitleGameLabel.setMaximumWidth(30)
        self.gameOptionsTitleGameLabel.setFont(QFont("Arial", 20))
        self.gameOptionsTitleGameLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        gameModeSelectionLayout.addWidget(self.gameOptionsTitleGameLabel)

        gameModePresetSelectorContainer = QWidget()
        gameModePresetSelectorLayout = QHBoxLayout(gameModePresetSelectorContainer)
        gameModePresetSelectorLabel = QLabel("Preset: ")
        self.gameModeComboBox = QComboBox()
        for gameMode in PREMADE_GAME_MODES:
            self.gameModeComboBox.addItem(gameMode["Name"], gameMode)
        gameModePresetSelectorLayout.addWidget(gameModePresetSelectorLabel)
        gameModePresetSelectorLayout.setStretchFactor(gameModePresetSelectorLabel, 1)
        gameModePresetSelectorLayout.addWidget(self.gameModeComboBox)
        gameModePresetSelectorLayout.setStretchFactor(self.gameModeComboBox, 3)
        gameModeSelectionLayout.addWidget(gameModePresetSelectorContainer)
        gameModeSelectionLayout.addStretch(1)

        # Game Mode Description
        self.gameModeDescription = QLabel()
        self.gameModeDescription.setWordWrap(True)
        gameModeSelectionLayout.addWidget(self.gameModeDescription)
        gameModeSelectionLayout.addStretch(1)

        # Confirmation buttons
        gameModeConfirmationButtonsContainer = QWidget()
        gameModeSelectionLayout.addWidget(gameModeConfirmationButtonsContainer)
        gameModeConfirmationButtonsLayout = QHBoxLayout(gameModeConfirmationButtonsContainer)
        self.gameModeStatusLabel = AutoResizeLabel()
        self.gameModeStatusLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        thisFont = QFont("Arial", 8)
        thisFont.setItalic(True)
        self.gameModeStatusLabel.setFont(thisFont)
        gameModeConfirmationButtonsLayout.addWidget(self.gameModeStatusLabel)
        self.gameModeApplyButton = QPushButton("Apply")
        self.gameModeApplyButton.clicked.connect(self.applySelectedGameMode)
        self.gameModeApplyButton.setDisabled(True)

        gameModeConfirmationButtonsLayout.addWidget(self.gameModeApplyButton)
        self.gameModeComboBox.currentIndexChanged.connect(self.onGameModeComboUpdate)
        self.onGameModeComboUpdate()

        # endregion === Game Mode Preset Options ===


        # Advanced Options Tab Container
        self.optionsTabWidget = QTabWidget()
        self.optionsTabWidget.addTab(self.generalOptionsContainer,"General")
        self.optionsTabWidget.addTab(self.pickOptionsContainer,"Draft")
        self.layout.addWidget(self.optionsTabWidget)

        self.layout.setStretchFactor(gameModeSelectionContainer, 1)
        self.layout.setStretchFactor(self.optionsTabWidget,3)

    # General options setup
    def setupGeneralOptions(self):
        self.generalOptionsContainer = QWidget()
        self.generalOptionsLayout = QHBoxLayout(self.generalOptionsContainer)
        self.generalOptionsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #region === Basic Game Options ===
        basicGameOptionsContainer = QWidget()
        basicGameOptionsLayout = QVBoxLayout(basicGameOptionsContainer)

        # Player set selection
        playerSetSelectionContainer = QWidget()
        playerSetSelectionLayout = QHBoxLayout(playerSetSelectionContainer)
        playerSetSelectionLabel = QLabel("Player Set: ")
        self.playerSetSelectionCombo = QComboBox()
        self.playerSetSelectionCombo.addItem("Premier")
        self.playerSetSelectionCombo.addItem("Wild")
        playerSetSelectionLayout.addWidget(playerSetSelectionLabel)
        playerSetSelectionLayout.addWidget(self.playerSetSelectionCombo)
        basicGameOptionsLayout.addWidget(playerSetSelectionContainer)

        # Read Stats checkbox
        giveCoinBoolContainer = QWidget()
        giveCoinBoolLayout = QHBoxLayout(giveCoinBoolContainer)
        giveCoinBoolLabel = QLabel("Use Coin: ")
        self.giveCoinBoolCheckbox = QCheckBox()
        self.giveCoinBoolCheckbox.setChecked(True)
        giveCoinBoolLayout.addWidget(giveCoinBoolLabel)
        giveCoinBoolLayout.addWidget(self.giveCoinBoolCheckbox)
        basicGameOptionsLayout.addWidget(giveCoinBoolContainer)

        # Give Coin checkbox
        readStatsBoolContainer = QWidget()
        readStatsBoolLayout = QHBoxLayout(readStatsBoolContainer)
        readStatsBoolLabel = QLabel("Save Stats: ")
        self.readStatsBoolCheckbox = QCheckBox()
        self.readStatsBoolCheckbox.setChecked(True)
        readStatsBoolLayout.addWidget(readStatsBoolLabel)
        readStatsBoolLayout.addWidget(self.readStatsBoolCheckbox)
        basicGameOptionsLayout.addWidget(readStatsBoolContainer)

        # Special Game label checkbox
        specialGameLabelContainer = QWidget()
        specialGameLabelLayout = QHBoxLayout(specialGameLabelContainer)
        specialGameLabelLabel = QLabel("Special Game Label: ")
        thisFont = specialGameLabelLabel.font()
        thisFont.setItalic(True)
        specialGameLabelLabel.setFont(thisFont)
        self.specialGameLabelInput = QLineEdit()
        specialGameLabelLayout.addWidget(specialGameLabelLabel)
        specialGameLabelLayout.setStretchFactor(specialGameLabelLabel,1)
        specialGameLabelLayout.addWidget(self.specialGameLabelInput)
        specialGameLabelLayout.setStretchFactor(self.specialGameLabelInput,2)
        basicGameOptionsLayout.addWidget(specialGameLabelContainer)

        self.generalOptionsLayout.addWidget(basicGameOptionsContainer)
        self.generalOptionsLayout.setStretchFactor(basicGameOptionsContainer,1)

        #endregion === Basic Game Options ===

        # Line
        vLine = QFrame()
        vLine.setFrameShape(QFrame.VLine)
        vLine.setFrameShadow(QFrame.Sunken)
        self.generalOptionsLayout.addWidget(vLine)

        #region === Common Options ===
        commonOptionsContainer = QWidget()
        commonOptionsLayout = QVBoxLayout(commonOptionsContainer)

        # Player count selection
        playerCountSelectionContainer = QWidget()
        playerCountSelectionLayout = QHBoxLayout(playerCountSelectionContainer)
        playerCountSelectionLabel = QLabel("Player Count: ")
        self.playerCountSelectionCombo = QComboBox()
        self.playerCountSelectionCombo.addItem("1v1",1)
        self.playerCountSelectionCombo.addItem("2v2",2)
        self.playerCountSelectionCombo.addItem("3v3",3)
        self.playerCountSelectionCombo.addItem("4v4",4)
        self.playerCountSelectionCombo.addItem("5v5",5)
        self.playerCountSelectionCombo.setCurrentIndex(3)
        playerCountSelectionLayout.addWidget(playerCountSelectionLabel)
        playerCountSelectionLayout.addWidget(self.playerCountSelectionCombo)
        commonOptionsLayout.addWidget(playerCountSelectionContainer)

        # Pick time selection
        pickTimeInputContainer = QWidget()
        pickTimeInputLayout = QHBoxLayout(pickTimeInputContainer)
        pickTimeInputLabel = QLabel("Pick/Ban Time: ")
        self.pickTimeInputCombo = QComboBox()
        self.pickTimeInputCombo.addItem("Unlimited")
        self.pickTimeInputCombo.addItem("5 Seconds")
        self.pickTimeInputCombo.addItem("10 Seconds")
        self.pickTimeInputCombo.addItem("20 Seconds")
        self.pickTimeInputCombo.addItem("30 Seconds")
        self.pickTimeInputCombo.addItem("40 Seconds")
        self.pickTimeInputCombo.addItem("50 Seconds")
        self.pickTimeInputCombo.addItem("60 Seconds")
        pickTimeInputLayout.addWidget(pickTimeInputLabel)
        pickTimeInputLayout.addWidget(self.pickTimeInputCombo)
        commonOptionsLayout.addWidget(pickTimeInputContainer)

        # First Pick Options
        firstPickOptionContainer = QWidget()
        firstPickOptionLayout = QHBoxLayout(firstPickOptionContainer)
        firstPickOptionLabel = QLabel("First Pick: ")
        self.firstPickOptionCombo = QComboBox()
        self.firstPickOptionCombo.addItem("Random")
        self.firstPickOptionCombo.addItem("Alex")
        self.firstPickOptionCombo.addItem("Danny")
        firstPickOptionLayout.addWidget(firstPickOptionLabel)
        firstPickOptionLayout.addWidget(self.firstPickOptionCombo)
        commonOptionsLayout.addWidget(firstPickOptionContainer)

        self.generalOptionsLayout.addWidget(commonOptionsContainer)
        self.generalOptionsLayout.setStretchFactor(commonOptionsContainer,1)
        #endregion === Common Options ===

        # Line
        vLine = QFrame()
        vLine.setFrameShape(QFrame.VLine)
        vLine.setFrameShadow(QFrame.Sunken)
        self.generalOptionsLayout.addWidget(vLine)

        self.generalOptionsLayout.addStretch(2)
    def onGameModeComboUpdate(self):
        currentlySelectGameModeData = self.gameModeComboBox.currentData()
        self.gameModeDescription.setText(currentlySelectGameModeData["Description"])
        if(currentlySelectGameModeData["Name"] == self.currentGameMode["Name"]):
            self.gameModeApplyButton.setDisabled(True)
            self.gameModeStatusLabel.setText("")
        else:
            self.gameModeApplyButton.setDisabled(False)
            self.gameModeStatusLabel.setText("*Not Yet Applied*")
    def applySelectedGameMode(self):
        currentlySelectGameModeData = self.gameModeComboBox.currentData()
        self.currentGameMode = currentlySelectGameModeData


        self.onGameModeComboUpdate()
    def updateDraftTypeDescription(self,draftType):
        self.draftTypeDescriptionLabel.setText(DRAFT_TYPES[draftType])
    def updateContentTypeDescription(self,contentType):
        self.contentOverrideDescriptionLabel.setText(DRAFT_CONTENT_DESCRIPTIONS[contentType])

    # Pick options setup
    def setupPickOptions(self):
        self.pickOptionsContainer = QWidget()
        self.pickOptionsLayout = QHBoxLayout(self.pickOptionsContainer)

        # region === Draft Options ===
        draftOptionsContainer = QWidget()
        draftOptionsLayout = QVBoxLayout(draftOptionsContainer)

        # Draft type selection
        draftTypeSelectionContainer = QWidget()
        draftTypeSelectionLayout = QHBoxLayout(draftTypeSelectionContainer)
        draftTypeSelectionLabel = QLabel("Draft order: ")
        self.draftTypeSelectionCombo = QComboBox()
        self.draftTypeSelectionCombo.addItems(list(DRAFT_TYPES.keys()))
        self.draftTypeSelectionCombo.currentTextChanged.connect(self.updateDraftTypeDescription)
        draftTypeSelectionLayout.addWidget(draftTypeSelectionLabel)
        draftTypeSelectionLayout.addWidget(self.draftTypeSelectionCombo)
        draftOptionsLayout.addWidget(draftTypeSelectionContainer)

        # Draft type description
        draftTypeDescriptionContainer = QWidget()
        draftTypeDescriptionLayout = QHBoxLayout(draftTypeDescriptionContainer)
        self.draftTypeDescriptionLabel = QLabel()
        self.draftTypeDescriptionLabel.setWordWrap(True)
        draftTypeDescriptionLayout.addWidget(self.draftTypeDescriptionLabel)
        draftOptionsLayout.addWidget(draftTypeDescriptionContainer)

        self.draftTypeSelectionCombo.setCurrentIndex(0)
        self.updateDraftTypeDescription(self.draftTypeSelectionCombo.currentText())

        self.pickOptionsLayout.addWidget(draftOptionsContainer)

        # endregion === Draft Options ===

        # region === Ban Options ===

        # Bans selection
        banCountContainer = QWidget()
        banCountLayout = QHBoxLayout(banCountContainer)
        banCountLabel = QLabel("Bans: ")
        self.banCountSpinBox = QSpinBox()
        self.banCountSpinBox.setAlignment(Qt.AlignCenter)
        self.banCountSpinBox.setMaximumWidth(50)
        banCountLayout.addWidget(banCountLabel)
        banCountLayout.addWidget(self.banCountSpinBox)
        draftOptionsLayout.addWidget(banCountContainer)

        # Random Bans selection
        randomBanCountContainer = QWidget()
        randomBanCountLayout = QHBoxLayout(randomBanCountContainer)
        randomBanCountLabel = QLabel("Random Bans: ")
        self.randomBanCountSpinBox = QSpinBox()
        self.randomBanCountSpinBox.setAlignment(Qt.AlignCenter)
        self.randomBanCountSpinBox.setMaximumWidth(50)
        randomBanCountLayout.addWidget(randomBanCountLabel)
        randomBanCountLayout.addWidget(self.randomBanCountSpinBox)
        draftOptionsLayout.addWidget(randomBanCountContainer)

        # endregion === Ban Options ===

        # Line
        vLine = QFrame()
        vLine.setFrameShape(QFrame.VLine)
        vLine.setFrameShadow(QFrame.Sunken)
        self.pickOptionsLayout.addWidget(vLine)

        # region === Content Options ===
        contentOptionsContainer = QWidget()
        contentOptionsLayout = QVBoxLayout(contentOptionsContainer)

        # Content Override selection
        contentOverrideContainer = QWidget()
        contentOverrideLayout = QHBoxLayout(contentOverrideContainer)
        contentOverrideLabel = QLabel("Draft content: ")
        self.contentOverrideCombo = QComboBox()
        self.contentOverrideCombo.addItems(list(DRAFT_CONTENT_DESCRIPTIONS.keys()))
        self.contentOverrideCombo.currentTextChanged.connect(self.updateContentTypeDescription)
        contentOverrideLayout.addWidget(contentOverrideLabel)
        contentOverrideLayout.addWidget(self.contentOverrideCombo)
        contentOptionsLayout.addWidget(contentOverrideContainer)

        # Content Override description
        contentOverrideDescriptionContainer = QWidget()
        contentOverrideDescriptionLayout = QHBoxLayout(contentOverrideDescriptionContainer)
        self.contentOverrideDescriptionLabel = QLabel()
        self.contentOverrideDescriptionLabel.setWordWrap(True)
        contentOverrideDescriptionLayout.addWidget(self.contentOverrideDescriptionLabel)
        contentOptionsLayout.addWidget(contentOverrideDescriptionContainer)

        self.contentOverrideCombo.setCurrentIndex(0)
        self.updateContentTypeDescription(self.contentOverrideCombo.currentText())

        self.pickOptionsLayout.addWidget(contentOptionsContainer)

        # endregion === Content Options ===

        # Line
        vLine = QFrame()
        vLine.setFrameShape(QFrame.VLine)
        vLine.setFrameShadow(QFrame.Sunken)
        self.pickOptionsLayout.addWidget(vLine)


        #region === Picks ===
        ballerzOptionsContainer = QWidget()
        ballerzOptionsLayout = QVBoxLayout(ballerzOptionsContainer)
        self.pickOptionsLayout.addWidget(ballerzOptionsContainer)
        ballerzPicksHeaderLabel = QLabel("Ballerz Picks")
        ballerzPicksHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ballerzOptionsLayout.addWidget(ballerzPicksHeaderLabel)

        ringersOptionsContainer = QWidget()
        ringersOptionsLayout = QVBoxLayout(ringersOptionsContainer)
        self.pickOptionsLayout.addWidget(ringersOptionsContainer)
        ringersPicksHeaderLabel = QLabel("Ringers Picks")
        ringersPicksHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ringersOptionsLayout.addWidget(ringersPicksHeaderLabel)

        self.playerPickComboBoxes = []

        for i in range(5):
            thisBallerzPickContainer = QWidget()
            thisBallerzPickLayout = QHBoxLayout(thisBallerzPickContainer)
            ballerzOptionsLayout.addWidget(thisBallerzPickContainer)
            thisPickLabel = QLabel(f"Pick {i + 1}")
            thisPickComboBox = QComboBox()
            thisPickComboBox.addItems(self.pickTypeOptions)
            thisBallerzPickLayout.addWidget(thisPickLabel)
            thisBallerzPickLayout.addWidget(thisPickComboBox)
            self.playerPickComboBoxes.append(thisPickComboBox)
        for i in range(5):
            thisRingersPickContainer = QWidget()
            thisRingersPickLayout = QHBoxLayout(thisRingersPickContainer)
            ringersOptionsLayout.addWidget(thisRingersPickContainer)
            thisPickLabel = QLabel(f"Pick {i + 1}")
            thisPickComboBox = QComboBox()
            thisPickComboBox.addItems(self.pickTypeOptions)
            thisRingersPickLayout.addWidget(thisPickLabel)
            thisRingersPickLayout.addWidget(thisPickComboBox)
            self.playerPickComboBoxes.append(thisPickComboBox)

            self.contentOverrideCombo.currentTextChanged.connect(self.updateDraftContentSlots)
            self.updateDraftContentSlots(self.contentOverrideCombo.currentText())

        # endregion === Picks ===

        self.pickOptionsLayout.addStretch(1)

    # This method generates a list that will determine the content of each pick slot
    def genDraftContentFromPreset(self,draftContentPreset, playerCount: int):
        returnSlots = []

        if (draftContentPreset == "Normal"):
            for i in range(10):
                returnSlots.append("Normal")
        elif (draftContentPreset == "Random"):
            for i in range(10):
                returnSlots.append("Random")
        elif (draftContentPreset == "Semi-Random"):
            for i in range(2):
                returnSlots.append("Normal")
                returnSlots.append("Random")
                returnSlots.append("Normal")
                returnSlots.append("Random")
                returnSlots.append("Normal")
        elif (draftContentPreset == "Archetypal-Random"):
            for i in range(10):
                returnSlots.append("Archetype (Random)")
        elif (draftContentPreset == "Captains"):
            for i in range(10):
                if i != 0 and i != 5:
                    returnSlots.append("Normal")
                else:
                    returnSlots.append("Random")
        elif (draftContentPreset == "Affirmative-Action"):
            for i in range(10):
                if i == playerCount - 1 or i == playerCount + 4:
                    returnSlots.append("Random")
                else:
                    returnSlots.append("Normal")
        elif (draftContentPreset == "Archetype Showdown"):
            archetypes = ["Archetype (Slayer)", "Archetype (Vigilante)", "Archetype (Medic)", "Archetype (Guardian)",
                          "Archetype (Engineer)", "Archetype (Director)"]
            ballerz = random.choice(archetypes)
            ringers = random.choice(archetypes)

            for i in range(5):
                returnSlots.append(ballerz)
            for i in range(5):
                returnSlots.append(ringers)

        elif (draftContentPreset == "Spritopian Duos"):
            shootingArchetypes = ["Archetype (Slayer)", "Archetype (Vigilante)"]
            nonShootingArchetypes = ["Archetype (Medic)", "Archetype (Guardian)", "Archetype (Engineer)",
                                     "Archetype (Director)"]

            ballerz1 = random.choice(shootingArchetypes)
            ballerz2 = random.choice(nonShootingArchetypes)
            ringers1 = random.choice(shootingArchetypes)
            ringers2 = random.choice(nonShootingArchetypes)

            ballerzPick = random.choice([ballerz1, ballerz2])
            ringersPick = random.choice([ringers1, ringers2])
            for i in range(5):
                if i % 2 == 0:
                    if ballerzPick == ballerz1:
                        returnSlots.append(ballerz1)
                    elif ballerzPick == ballerz2:
                        returnSlots.append(ballerz2)
                else:
                    if ballerzPick == ballerz1:
                        returnSlots.append(ballerz2)
                    elif ballerzPick == ballerz2:
                        returnSlots.append(ballerz1)

            for i in range(5):
                if i % 2 == 0:
                    if ringersPick == ringers1:
                        returnSlots.append(ringers1)
                    elif ringersPick == ringers2:
                        returnSlots.append(ringers2)
                else:
                    if ringersPick == ringers1:
                        returnSlots.append(ringers2)
                    elif ringersPick == ringers2:
                        returnSlots.append(ringers1)

        elif (draftContentPreset == "Chaos"):
            for i in range(10):
                returnSlots.append(random.choice(self.pickTypeOptions))

        return returnSlots
    def updateDraftContentSlots(self,draftContentPreset):
        playerCount = int(self.playerCountSelectionCombo.currentText().split("v")[0])
        draftContentList = self.genDraftContentFromPreset(draftContentPreset,playerCount)

        for i, pickComboBox in enumerate(self.playerPickComboBoxes):
            pickComboBox.setCurrentText(draftContentList[i])





    # Ban options setup
    def setupBanOptions(self):
        pass


