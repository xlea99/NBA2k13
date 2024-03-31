from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui import const
from spritopia.gui.player_card import PlayerCard
from functools import partial



# Class for providing the Picker Menu
class PickerMenu(QWidget):

    ACTION_BUTTONS_ACTIVE_COLOR = "green"
    ACTION_BUTTONS_INACTIVE_COLOR = "#3b3b3b"

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

        self.midLayout.addWidget(self.selectedPlayerCard)
        self.midLayout.addSpacerItem(spacer)

        # Ballerz Team Layout
        self.ballerzLayout = QVBoxLayout()
        headersFont = QFont("Arial",24)
        ballerzHeader = QLabel("Ballerz")
        ballerzHeader.setFont(headersFont)
        ballerzHeader.setAlignment(Qt.AlignCenter)
        self.ballerzLayout.addWidget(ballerzHeader)

        # Ringers Team Layout
        self.ringersLayout = QVBoxLayout()
        ringersHeader = QLabel("Ringers")
        ringersHeader.setAlignment(Qt.AlignCenter)
        ringersHeader.setFont(headersFont)
        self.ringersLayout.addWidget(ringersHeader)

        self.playerCardSlots = [{} for i in range(10)]
        for index,playerCardSlot in enumerate(self.playerCardSlots):
            playerCardSlot["MainLayout"] = QHBoxLayout()
            playerCardSlot["IsLocked"] = False
            playerCardSlot["Actions"] = {}
            playerCardSlot["Badges"] = {}

            thisPlayerCard = PlayerCard()
            thisBadgesLayout = QVBoxLayout()
            thisBadgesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            thisActionsLayout = QVBoxLayout()
            thisActionsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            thisActionsLayout.addWidget(spacer)
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            thisBadgesLayout.addWidget(spacer)

            addPlayerButton = QPushButton("+")
            addPlayerButton.setStyleSheet(f"background-color: {self.ACTION_BUTTONS_ACTIVE_COLOR}")
            addPlayerButton.clicked.connect(partial(self.updatePlayerSlot,index))
            addPlayerButton.setMinimumWidth(0.08 * thisPlayerCard.width())
            addPlayerButton.setMaximumWidth(0.08 * thisPlayerCard.width())
            removePlayerButton = QPushButton("-")
            removePlayerButton.setStyleSheet(f"background-color: {self.ACTION_BUTTONS_ACTIVE_COLOR}")
            removePlayerButton.clicked.connect(partial(self.removePlayerSlot,index))
            removePlayerButton.setMinimumWidth(0.08 * thisPlayerCard.width())
            removePlayerButton.setMaximumWidth(0.08 * thisPlayerCard.width())
            thisActionsLayout.addWidget(addPlayerButton)
            thisActionsLayout.addWidget(removePlayerButton)
            thisActionsLayout.addStretch(1)

            playerCardSlot["PlayerCard"] = thisPlayerCard
            playerCardSlot["BadgesLayout"] = thisBadgesLayout
            playerCardSlot["ActionsLayout"] = thisActionsLayout
            playerCardSlot["Actions"]["AddPlayerButton"] = addPlayerButton
            playerCardSlot["Actions"]["RemovePlayerButton"] = removePlayerButton

            if(index < 5):
                playerCardSlot["MainLayout"].addLayout(thisBadgesLayout)
                playerCardSlot["MainLayout"].addWidget(thisPlayerCard)
                playerCardSlot["MainLayout"].addLayout(thisActionsLayout)
                self.ballerzLayout.addLayout(playerCardSlot["MainLayout"])
            else:
                playerCardSlot["MainLayout"].addLayout(thisActionsLayout)
                playerCardSlot["MainLayout"].addWidget(thisPlayerCard)
                playerCardSlot["MainLayout"].addLayout(thisBadgesLayout)
                self.ringersLayout.addLayout(playerCardSlot["MainLayout"])

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

        self.lockSlot(0)
        self.lockSlot(1)
        self.lockSlot(2)
        self.lockSlot(3)
        self.lockSlot(7)

        self.unlockSlot(2)


    # Method for updating the center player selection widget.
    def updateCurrentPlayerSelected(self,spriteID = None):
        self.currentSelectorSpriteID = spriteID
        self.selectedPlayerCard.setSpriteID(spriteID)
    # Method for adding a play to the given slot.
    def updatePlayerSlot(self,slot):
        if(self.currentSelectorSpriteID is not None and self.currentSelectorSpriteID in [playerCardSection["PlayerCard"].spriteID for playerCardSection in self.playerCardSlots]):
            return False
        else:
            self.playerCardSlots[slot]["PlayerCard"].setSpriteID(self.currentSelectorSpriteID)
            return True
    # Method for removing a player from the given slot.
    def removePlayerSlot(self,slot):
        self.playerCardSlots[slot]["PlayerCard"].setSpriteID(None)

    badges = {"Padlock" : {"Path" : paths["Graphics"] / "GUI/padlock.png", "Priority": 100}}
    # Helper methods to add and remove the given badge to the given slotID
    def addBadge(self,slotID,badgeName):
        if (badgeName not in self.playerCardSlots[slotID]["Badges"].keys()):
            newBadge = QLabel()
            newBadgeImage = QPixmap(self.badges[badgeName]["Path"]).scaled(const.PICKER_BADGE_SIZE,const.PICKER_BADGE_SIZE)
            newBadge.setPixmap(newBadgeImage)
            newBadge.setMinimumWidth(const.PICKER_BADGE_SIZE)
            newBadge.setMaximumWidth(const.PICKER_BADGE_SIZE)
            newBadge.setMinimumHeight(const.PICKER_BADGE_SIZE)
            newBadge.setMaximumHeight(const.PICKER_BADGE_SIZE)
            newBadge.setWindowFlags(Qt.FramelessWindowHint)
            newBadge.setAttribute(Qt.WA_TranslucentBackground)

            currentBadgeOrder = []
            for thisBadgeName in self.playerCardSlots[slotID]["Badges"].keys():
                if(currentBadgeOrder):
                    hasAddedBadge = False
                    for index,orderedBadgeName in enumerate(currentBadgeOrder):
                        if(self.badges[orderedBadgeName]["Priority"] < self.badges[thisBadgeName]["Priority"]):
                            currentBadgeOrder.insert(index,thisBadgeName)
                            hasAddedBadge = True
                            break
                    if(not hasAddedBadge):
                        currentBadgeOrder.append(thisBadgeName)
                else:
                    currentBadgeOrder.append(thisBadgeName)

            targetIndex = len(self.playerCardSlots[slotID]["Badges"])
            for index,orderedBadgeName in enumerate(currentBadgeOrder):
                if(self.badges[orderedBadgeName]["Priority"] < self.badges[badgeName]["Priority"]):
                    targetIndex = index
                    break

            self.playerCardSlots[slotID]["Badges"][badgeName] = newBadge
            self.playerCardSlots[slotID]["BadgesLayout"].insertWidget(targetIndex,newBadge)
    def removeBadge(self,slotID,badgeName):
        if(badgeName in self.playerCardSlots[slotID]["Badges"].keys()):
            self.playerCardSlots[slotID]["BadgesLayout"].removeWidget(self.playerCardSlots[slotID]["Badges"][badgeName])
            self.playerCardSlots[slotID]["Badges"][badgeName].hide()
            self.playerCardSlots[slotID]["Badges"][badgeName].deleteLater()
            del self.playerCardSlots[slotID]["Badges"][badgeName]

    # Method to lock and unlock the given slot, setting its interactivity
    def lockSlot(self,slotID):
        self.playerCardSlots[slotID]["Locked"] = True
        self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setEnabled(False)
        self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setStyleSheet(f"background-color: {self.ACTION_BUTTONS_INACTIVE_COLOR}")
        self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setEnabled(False)
        self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setStyleSheet(f"background-color: {self.ACTION_BUTTONS_INACTIVE_COLOR}")
        self.addBadge(slotID,"Padlock")
    def unlockSlot(self,slotID):
        self.playerCardSlots[slotID]["Locked"] = False
        self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setEnabled(True)
        self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setStyleSheet(f"background-color: {self.ACTION_BUTTONS_ACTIVE_COLOR}")
        self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setEnabled(True)
        self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setStyleSheet(f"background-color: {self.ACTION_BUTTONS_ACTIVE_COLOR}")
        self.removeBadge(slotID,"Padlock")