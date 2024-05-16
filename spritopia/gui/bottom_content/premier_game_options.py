from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui import const
from spritopia.gui.widgets.player_card import PlayerCard
from spritopia.gui.app_state import globalAppState
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from functools import partial

PREMADE_GAME_MODES = [
    {"Name": "Classic", "Description": "Classic 2K experience - revolving picks, no bans."},
    {"Name": "Smite", "Description": "Smite-style picking, all players allowed, 5 bans each."}
]


class PremierGameOptions(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)



        self.currentGameMode = PREMADE_GAME_MODES[0]
        self.setupGeneralOptions()



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
        self.optionsPicksContainer = QWidget()
        self.optionsTabWidget.addTab(self.optionsPicksContainer,"Picks")
        self.optionsBansContainer = QWidget()
        self.optionsTabWidget.addTab(self.optionsBansContainer,"Bans")
        self.layout.addWidget(self.optionsTabWidget)

        self.layout.setStretchFactor(gameModeSelectionContainer, 1)
        self.layout.setStretchFactor(self.optionsTabWidget,3)


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

        self.generalOptionsLayout.addStretch(2)







        #self.generalOptionsLayout.addStretch(2)
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









