from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QPushButton
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from spritopia.data_storage.data_storage import d
from spritopia.common.paths import paths
from spritopia.gui import gui_const
from spritopia.players.archetypes import MAPPED_ATTRIBUTES
from spritopia.gui.widgets.hoverable_image_label import HoverableImageLabel

class PlayerRevealCard(QWidget):
    def __init__(self, parent=None, spriteID=None):
        super().__init__(parent=parent)
        self.setObjectName("playerRevealCard")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Define a dark color scheme.
        self.backgroundColor = "#2e2e2e"  # Dark background
        self.borderColor = "#444444"      # Dark grey border

        # Main layout setup
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # -------------------
        # Default Button Section
        # -------------------
        self.revealButton = QPushButton("Reveal")
        self.revealButton.setFixedSize(100, 30)
        self.mainLayout.addWidget(self.revealButton, alignment=Qt.AlignCenter)

        # -------------------
        # Info Section
        # -------------------
        self.infoWidget = QWidget(self)
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.infoWidget)
        self.infoWidget.hide()

        # -------------------
        # Name/Title Section
        # -------------------
        titleContainer = QWidget()
        titleLayout = QVBoxLayout(titleContainer)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.addWidget(titleContainer, 1)  # 1 part of 5 total

        title_mainContentContainer = QWidget()
        title_mainContentLayout = QHBoxLayout(title_mainContentContainer)
        title_mainContentLayout.setContentsMargins(5, 0, 5, 0)
        titleLayout.addWidget(title_mainContentContainer)

        self.title_playerNameLabel = AutoResizeLabel(autoWrap=False)
        self.title_playerNameLabel.setObjectName("PlayerName")
        self.title_playerNameLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        title_mainContentLayout.addWidget(self.title_playerNameLabel)

        # -------------------
        # Lower Section
        # -------------------
        lowerContainer = QWidget()
        lowerLayout = QHBoxLayout(lowerContainer)
        lowerLayout.setContentsMargins(8, 0, 8, 0)
        self.infoLayout.addWidget(lowerContainer, 4)  # 4 parts of 5 total

        # Archetype and Faction Icon
        archetypeContainer = QWidget()
        archetypeLayout = QVBoxLayout(archetypeContainer)
        self.archetypeLabel = QLabel()
        self.archetypeLabel.setFont(QFont("Segoe UI", 12))
        self.archetypeLabel.setAlignment(Qt.AlignCenter)
        # Use HoverableImageLabel for faction (default preview: top_left).
        self.factionIcon = HoverableImageLabel(QSize(70, 70), QSize(280, 280))
        # Create a placeholder pixmap (70x70, transparent)
        placeholder_faction = QPixmap(70, 70)
        placeholder_faction.fill(Qt.transparent)
        self.factionIcon.setCardData(placeholder_faction, "Title", "This does shit")
        self.factionIcon.setAlignment(Qt.AlignCenter)
        self.factionLabel = AutoResizeLabel(autoWrap=True, minimumSize=12)
        self.factionLabel.setFont(QFont("Segoe UI", 12))
        self.factionLabel.setAlignment(Qt.AlignCenter)
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
            thisAttributeLabel.setAlignment(Qt.AlignCenter)
            attributesLayout.addWidget(thisAttributeLabel)
            self.attributeLabels.append(thisAttributeLabel)
        lowerLayout.addWidget(attributesContainer)
        lowerLayout.addStretch(1)

        # Rarity and Artifact
        rarityArtifactContainer = QWidget()
        rarityArtifactLayout = QVBoxLayout(rarityArtifactContainer)
        self.rarityLabel = QLabel()
        self.rarityLabel.setFont(QFont("Segoe UI", 12))
        self.rarityLabel.setAlignment(Qt.AlignCenter)
        # Use HoverableImageLabel for artifact with preview positioned at "top_right".
        self.artifactImage = HoverableImageLabel(QSize(70, 70), QSize(280, 280), preview_position="top_right")
        # Create a placeholder pixmap for artifact
        placeholder_artifact = QPixmap(70, 70)
        placeholder_artifact.fill(Qt.transparent)
        self.artifactImage.setCardData(placeholder_artifact, "Title", "Description")
        self.artifactImage.setAlignment(Qt.AlignCenter)
        rarityArtifactLayout.addWidget(self.rarityLabel)
        rarityArtifactLayout.addWidget(self.artifactImage)
        rarityArtifactLayout.addStretch(1)
        lowerLayout.addWidget(rarityArtifactContainer)

        # Adjust the widget sizes and policy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMaximumHeight(360)
        self.setMaximumWidth(360)
        self.__spriteID = spriteID
        self.__sizeHint = QSize(360, 360)

        # Configure style (including adding a drop shadow for depth)
        self.configureStyle()
        self.addShadowEffect()

        # What happens when you click the button
        self.revealButton.clicked.connect(self.revealCard)

    def revealCard(self):
        self.revealButton.hide()
        self.infoWidget.show()

    def unrevealCard(self):
        self.revealButton.show()
        self.infoWidget.hide()

    def configureStyle(self, backgroundColor=None, borderColor=None):
        if backgroundColor:
            self.backgroundColor = backgroundColor
        if borderColor:
            self.borderColor = borderColor

        # Apply a dark-themed stylesheet
        self.setStyleSheet(f"""
            QWidget#playerRevealCard {{
                background-color: {self.backgroundColor};
                border: 2px solid {self.borderColor};
                border-radius: 8px;
                padding: 10px;
            }}
            QLabel {{
                color: #e0e0e0;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
            }}
        """)

    def addShadowEffect(self):
        # Adding a subtle drop shadow can help lift the card visually.
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(shadow)

    # Base attribute label font/stylesheet
    baseAttributeFont = QFont("Segoe UI", 10)
    baseAttributeStylesheet = "color: #e0e0e0"  # Light grey text for dark background
    # Updated colors for attribute modifications (using slightly brighter accents)
    attributeIncreaseValStylesheet = "color: #66bb6a"  # Brighter green
    attributeDecreaseValStylesheet = "color: #ef5350"  # Brighter red
    attributeSetValStylesheet = "color: #42a5f5"  # Brighter blue

    def setSpriteID(self, spriteID):
        self.__spriteID = spriteID
        if self.__spriteID is None:
            self.title_playerNameLabel.setText("-")
            self.archetypeLabel.setText("")
            self.factionIcon.setText("")
        else:
            # Retrieve player data
            thisPlayer = d.players[spriteID]
            self.title_playerNameLabel.setText(thisPlayer.getFullName())

            # === Archetype/Faction Label ===
            archetype = thisPlayer["Archetype_Name"]
            darkArchetypeColors = {
                "Slayer": "#5A9BD5",  # Blue
                "Director": "#A366D0"  # Purple
            }
            archetypeColor = darkArchetypeColors.get(
                archetype,
                gui_const.ARCHETYPE_COLORS.get(archetype, "#e0e0e0")
            )
            self.archetypeLabel.setText(archetype)
            self.archetypeLabel.setStyleSheet(f"color: {archetypeColor}; font-weight: bold;")

            factionPixmap = QPixmap(paths["graphics"] / f"FactionIcons/{thisPlayer['Faction']}.png")
            self.factionIcon.setPixmap(factionPixmap)
            self.factionIcon.previewWidget.setToolTip(thisPlayer["Faction"])
            self.factionLabel.setText(thisPlayer["Faction"])

            # === Rarity/Artifact Label ===
            customRarityColors = {
                "Rare": "#4FC3F7",  # Blue for Rare
                "Epic": "#BA68C8"   # Purple for Epic
            }
            rarity = thisPlayer["Rarity"]
            if rarity in customRarityColors:
                rarityColor = customRarityColors[rarity]
            else:
                rarityColor = gui_const.RARITY_COLORS.get(rarity, "#e0e0e0")
            self.rarityLabel.setText(rarity)
            self.rarityLabel.setStyleSheet(f"color: {rarityColor}; font-weight: bold;")

            artifactPMod = thisPlayer.getArtifactPMod()
            if artifactPMod is not None:
                self.artifactImage.show()
                artifactPixmap = QPixmap(paths["graphics"] / artifactPMod["Image"])
                self.artifactImage.setPixmap(artifactPixmap)
                # Wrap the tooltip text in HTML to constrain its width (e.g., to 200px).
                artifactDescription = artifactPMod["Description"]
                artifactTitle = artifactPMod["Name"]
                self.artifactImage.setCardData(artifactPixmap, artifactTitle, artifactDescription)
            else:
                # Clear the artifact image and tooltip when no artifact is available.
                self.artifactImage.clear()
                self.artifactImage.hide()

            # === Attributes List ===
            attributeImportanceList = thisPlayer.getAttributeImportantList(forcedPriorityCount=3)
            for i, attributeLabel in enumerate(self.attributeLabels):
                attributeLabelString = f"{MAPPED_ATTRIBUTES[attributeImportanceList[i]]}: {thisPlayer[attributeImportanceList[i]]}"
                attributeLabel.setStyleSheet(self.baseAttributeStylesheet)
                if artifactPMod is not None:
                    for modification in artifactPMod["Modifications"]:
                        if attributeImportanceList[i] == modification["Key"]:
                            attributeLabelString += " ("
                            if modification["Operation"] == "Add":
                                attributeLabelString += f"+{modification['Value']})"
                                attributeLabel.setStyleSheet(self.attributeIncreaseValStylesheet)
                            elif modification["Operation"] == "Subtract":
                                attributeLabelString += f"-{modification['Value']})"
                                attributeLabel.setStyleSheet(self.attributeDecreaseValStylesheet)
                            elif modification["Operation"] == "Set":
                                attributeLabelString += f"was {artifactPMod['PrevValues'][attributeImportanceList[i]]})"
                                attributeLabel.setStyleSheet(self.attributeSetValStylesheet)
                attributeLabel.setText(attributeLabelString)
