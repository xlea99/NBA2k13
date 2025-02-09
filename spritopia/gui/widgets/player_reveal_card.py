from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from spritopia.data_storage.data_storage import d
from spritopia.common.paths import paths
from spritopia.gui import gui_const
from spritopia.players.archetypes import MAPPED_ATTRIBUTES


class PlayerRevealCard(QWidget):
    def __init__(self, parent=None, spriteID=None):
        super().__init__(parent=parent)
        self.setObjectName("playerRevealCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.backgroundColor = "grey"
        self.borderColor = "black"
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Name/Title Section
        titleContainer = QWidget()
        titleLayout = QVBoxLayout(titleContainer)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(titleContainer, 1)  # 1 part of 5 total

        title_mainContentContainer = QWidget()
        title_mainContentLayout = QHBoxLayout(title_mainContentContainer)
        title_mainContentLayout.setContentsMargins(5, 0, 5, 0)
        titleLayout.addWidget(title_mainContentContainer)

        self.title_playerNameLabel = AutoResizeLabel(autoWrap=False)
        self.title_playerNameLabel.setObjectName("PlayerName")
        self.title_playerNameLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        title_mainContentLayout.addWidget(self.title_playerNameLabel)

        # Lower Section
        lowerContainer = QWidget()
        lowerLayout = QHBoxLayout(lowerContainer)
        lowerLayout.setContentsMargins(8, 0, 8, 0)
        self.mainLayout.addWidget(lowerContainer, 4)  # 4 parts of 5 total

        # Archetype and Faction Icon
        archetypeContainer = QWidget()
        archetypeLayout = QVBoxLayout(archetypeContainer)
        self.archetypeLabel = QLabel()
        self.archetypeLabel.setFont(QFont("Arial",12))
        self.archetypeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.factionIcon = QLabel()
        self.factionIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.factionIcon.setFixedSize(70, 70)  # Example size
        self.factionLabel = AutoResizeLabel(autoWrap=True,minimumSize=12)
        self.factionLabel.setFont(QFont("Arial",12))
        self.factionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.factionLabel.setMaximumWidth(70)
        archetypeLayout.addWidget(self.archetypeLabel)
        archetypeLayout.addWidget(self.factionIcon)
        archetypeLayout.addWidget(self.factionLabel)
        archetypeLayout.addStretch(1)
        lowerLayout.addWidget(archetypeContainer)
        lowerLayout.addStretch(1)

        # Attribute List
        attributesContainer = QWidget()
        attributesLayout = QVBoxLayout(attributesContainer)
        self.attributeLabels = []
        for _ in range(7):
            thisAttributeLabel = QLabel()
            thisAttributeLabel.setFont(self.baseAttributeFont)
            thisAttributeLabel.setStyleSheet(self.baseAttributeStylesheet)
            thisAttributeLabel.setWordWrap(True)
            thisAttributeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            attributesLayout.addWidget(thisAttributeLabel)
            self.attributeLabels.append(thisAttributeLabel)
        lowerLayout.addWidget(attributesContainer)
        lowerLayout.addStretch(1)

        # Rarity and Artifact
        rarityArtifactContainer = QWidget()
        rarityArtifactLayout = QVBoxLayout(rarityArtifactContainer)
        self.rarityLabel = QLabel()
        self.rarityLabel.setFont(QFont("Arial",12))
        self.rarityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artifactImage = QLabel()
        self.artifactImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artifactImage.setFixedSize(70, 70)  # Example size
        self.artifactLabel = AutoResizeLabel(autoWrap=True,minimumSize=12)
        self.artifactLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artifactLabel.setMaximumWidth(70)
        rarityArtifactLayout.addWidget(self.rarityLabel)
        rarityArtifactLayout.addWidget(self.artifactImage)
        rarityArtifactLayout.addWidget(self.artifactLabel)
        rarityArtifactLayout.addStretch(1)
        lowerLayout.addWidget(rarityArtifactContainer)

        # Adjust the widget sizes and policy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMaximumHeight(360)
        self.setMaximumWidth(360)
        self.__spriteID = spriteID
        self.__sizeHint = QSize(360, 360)
        self.configureStyle()
        #self.setSpriteID(self.__spriteID)

    # Configures some styling elements for the player card.
    def configureStyle(self,backgroundColor=None,borderColor=None):
        if(backgroundColor):
            self.backgroundColor = backgroundColor
        if(borderColor):
            self.borderColor = borderColor
        self.setStyleSheet(f".PlayerRevealCard#playerRevealCard {{ border: 3px solid {self.borderColor}; "
                           f"background: {self.backgroundColor}; "
                           f"padding: 3px; }}")


    # Base attribute label font/stylesheet
    baseAttributeFont = QFont("Helvetica",10)
    baseAttributeStylesheet = "color: black"
    attributeIncreaseValStylesheet = "color: green"
    attributeDecreaseValStylesheet = "color: red"
    attributeSetValStylesheet = "color: blue"
    # Sets the spriteID (and updates all elements) to the given ID
    def setSpriteID(self,spriteID):
        self.__spriteID = spriteID
        if(self.__spriteID is None):
            self.title_playerNameLabel.setText("-")
            self.archetypeLabel.setText("")
            self.factionIcon.setText("")
        else:
            # Player name
            thisPlayer = d.players[spriteID]
            self.title_playerNameLabel.setText(thisPlayer.getFullName())

            # Archetype/Faction Label
            self.archetypeLabel.setText(thisPlayer["Archetype_Name"])
            self.archetypeLabel.setStyleSheet(f"color: {gui_const.ARCHETYPE_COLORS[thisPlayer['Archetype_Name']]}")
            factionPixmap = QPixmap(paths["graphics"] / f"FactionIcons/{thisPlayer['Faction']}.png")
            self.factionIcon.clear()
            self.factionIcon.setPixmap(factionPixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.factionLabel.setText(thisPlayer["Faction"])

            # Rarity/Artifact Label
            self.rarityLabel.setText(thisPlayer["Rarity"])
            self.rarityLabel.setStyleSheet(f"color: {gui_const.RARITY_COLORS[thisPlayer['Rarity']]}")
            self.artifactImage.clear()
            artifactPMod = thisPlayer.getArtifactPMod()
            if (artifactPMod is not None):
                artifactPixmap = QPixmap(paths["graphics"] / artifactPMod["Image"])
                self.artifactImage.setPixmap(artifactPixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.artifactImage.setToolTip(artifactPMod["Description"])
                adjustedTitle = artifactPMod["Name"]
                if(len(adjustedTitle) > 38):
                    adjustedTitle = adjustedTitle[:30].rstrip() + "... " + adjustedTitle[-8:]
                self.artifactLabel.setText(adjustedTitle)
            else:
                self.artifactLabel.setText("")

            # Attributes List
            attributeImportanceList = thisPlayer.getAttributeImportantList(forcedPriorityCount=3)
            for i,attributeLabel in enumerate(self.attributeLabels):
                attributeLabelString = f"{MAPPED_ATTRIBUTES[attributeImportanceList[i]]}: {thisPlayer[attributeImportanceList[i]]}"
                #attributeLabel.setFont(self.baseAttributeFont) Currently unneeded
                attributeLabel.setStyleSheet(self.baseAttributeStylesheet)
                if(artifactPMod is not None):
                    for modification in artifactPMod["Modifications"]:
                        if(attributeImportanceList[i] == modification["Key"]):
                            attributeLabelString += f" ("
                            if(modification["Operation"] == "Add"):
                                attributeLabelString += f"+{modification['Value']})"
                                attributeLabel.setStyleSheet(self.attributeIncreaseValStylesheet)
                            elif(modification["Operation"] == "Subtract"):
                                attributeLabelString += f"-{modification['Value']})"
                                attributeLabel.setStyleSheet(self.attributeDecreaseValStylesheet)
                            elif (modification["Operation"] == "Set"):
                                attributeLabelString += f"og. {artifactPMod['PrevValues'][attributeImportanceList[i]]})"
                                attributeLabel.setStyleSheet(self.attributeSetValStylesheet)
                attributeLabel.setText(attributeLabelString)
