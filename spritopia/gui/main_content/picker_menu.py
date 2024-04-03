from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui import const
from spritopia.gui.widgets.player_card import PlayerCard
from spritopia.gui.app_state import globalAppState
from functools import partial

MID_TITLE_HEADER_FONT = QFont("Arial",42)
MID_TITLE_SUBTEXT_FONT = QFont("Arial",16)

BADGE_SIZE = 24

BANS_HEIGHT = 24

ACTION_BUTTONS_ACTIVE_COLOR = "green"
ACTION_BUTTONS_INACTIVE_COLOR = "#3b3b3b"

DEFAULT_PHASE_ORDER = ({"Desc": "Danny Bans 2", "BallerzBans": 2},
                       {"Desc": "Alex Bans 2", "RingersBans": 2},
                       {"Desc": "Danny Picks 1 Player", "Picks": (0,)},
                       {"Desc": "Alex Picks 2 Players", "Picks": (5, 6)},
                       {"Desc": "Danny Picks 2 Players", "Picks": (1, 2)},
                       {"Desc": "Alex Picks 1 Player", "Picks": (7,)},
                       {"Desc": "Danny Picks 1 Player", "Picks": (3,)},
                       {"Desc": "Alex Picks 1 Player", "Picks": (8,)})

# Class for providing the Picker Menu
class PickerMenu(QWidget):

    # Initialize UI and tracking variables
    def __init__(self,parent=None,phaseOrder = DEFAULT_PHASE_ORDER,gameMode=4):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.addStretch(1)

        self.gameMode = gameMode


        #region Base Setup UI

        # Mid-section Layout
        self.midLayout = QVBoxLayout()

        # Ballerz Team Layout
        self.ballerzLayout = QVBoxLayout()

        # Ringers Team Layout
        self.ringersLayout = QVBoxLayout()

        #endregion Base Setup UI

        # region Bans UI

        ballerzBanContainerWidget = QWidget()
        ballerzBanContainerWidget.setMinimumHeight(64)
        ballerzBanContainerWidget.setMaximumHeight(64)
        #ballerzBanContainerWidget.setObjectName("ballerzBanContainerWidget")
        #ballerzBanContainerWidget.setStyleSheet("#ballerzBanContainerWidget: {border: 2px black}")
        self.ballerzBanLayout = QHBoxLayout(ballerzBanContainerWidget)
        self.ballerzBanLayout.setContentsMargins(0,0,0,0)
        #self.ballerzBanTitle = QLabel("B\nA\nN\nS")
        #self.ballerzBanTitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ballerzBanButtonContainer = QWidget()
        ballerzBanButtonContainer.setMaximumWidth(64)
        ballerzBanButtonLayout = QHBoxLayout(ballerzBanButtonContainer)
        ballerzBanButtonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ballerzBanButton = QPushButton("BAN")
        self.ballerzBanButton.clicked.connect(lambda _: self.ban(self.currentSelectorSpriteID,ballerz=True))
        ballerzBanButtonLayout.addWidget(self.ballerzBanButton)
        self.ballerzBanListLayout = QHBoxLayout()
        self.ballerzBanListLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ballerzBanLayout.addWidget(ballerzBanButtonContainer)
        self.ballerzBanLayout.addLayout(self.ballerzBanListLayout)
        self.ballerzLayout.addWidget(ballerzBanContainerWidget)

        ringersBanContainerWidget = QWidget()
        ringersBanContainerWidget.setMinimumHeight(64) #TODO make dynamic based on playercard icon size
        ringersBanContainerWidget.setMaximumHeight(64) #TODO make dynamic based on playercard icon size
        #ringersBanContainerWidget.setObjectName("ringersBanContainerWidget")
        #ringersBanContainerWidget.setStyleSheet("#ringersBanContainerWidget: {border: 2px black}")
        self.ringersBanLayout = QHBoxLayout(ringersBanContainerWidget)
        self.ringersBanLayout.setContentsMargins(0,0,0,0)
        #self.ringersBanTitle = QLabel("B\nA\nN\nS")
        #self.ringersBanTitle.setAlignment(Qt.AlignmentFlag.AlignRight)
        ringersBanButtonContainer = QWidget()
        ringersBanButtonContainer.setMaximumWidth(64)
        ringersBanButtonLayout = QHBoxLayout(ringersBanButtonContainer)
        ringersBanButtonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ringersBanButton = QPushButton("BAN")
        self.ringersBanButton.clicked.connect(lambda _: self.ban(self.currentSelectorSpriteID,ballerz=False))
        ringersBanButtonLayout.addWidget(self.ringersBanButton)
        self.ringersBanListLayout = QHBoxLayout()
        self.ringersBanListLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.ringersBanLayout.addLayout(self.ringersBanListLayout)
        self.ringersBanLayout.addWidget(ringersBanButtonContainer)
        self.ringersLayout.addWidget(ringersBanContainerWidget)

        headersFont = QFont("Arial",24)
        ballerzHeader = QLabel("Ballerz")
        ballerzHeader.setFont(headersFont)
        ballerzHeader.setAlignment(Qt.AlignCenter)
        self.ballerzLayout.addWidget(ballerzHeader)

        ringersHeader = QLabel("Ringers")
        ringersHeader.setAlignment(Qt.AlignCenter)
        ringersHeader.setFont(headersFont)
        self.ringersLayout.addWidget(ringersHeader)




        # endregion Bans UI

        #region Player Card Slots UI

        self.playerCardSlots = [{} for i in range(10)]
        for index,playerCardSlot in enumerate(self.playerCardSlots):
            playerCardSlot["MainContainer"] = QWidget()
            playerCardSlot["MainLayout"] = QHBoxLayout(playerCardSlot["MainContainer"])
            playerCardSlot["IsLocked"] = False
            playerCardSlot["Actions"] = {}
            playerCardSlot["Badges"] = {}

            playerCardContainer = QWidget()
            playerCardLayout = QVBoxLayout(playerCardContainer)
            playerCardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            playerCardLayout.setContentsMargins(0,0,0,0)
            thisPlayerCard = PlayerCard()
            playerCardLayout.addWidget(thisPlayerCard)

            thisBadgesContainerWidget = QWidget()
            thisBadgesContainerWidget.setMinimumWidth(BADGE_SIZE)
            thisBadgesContainerWidget.setMaximumWidth(BADGE_SIZE)
            thisBadgesLayout = QVBoxLayout(thisBadgesContainerWidget)
            thisBadgesLayout.setContentsMargins(0,0,0,0)
            thisBadgesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            thisActionsContainerWidget = QWidget()
            thisActionsContainerWidget.setMinimumWidth(BADGE_SIZE)
            thisActionsContainerWidget.setMaximumWidth(BADGE_SIZE)
            thisActionsLayout = QVBoxLayout(thisActionsContainerWidget)
            thisActionsLayout.setContentsMargins(0,0,0,0)
            thisActionsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

            addPlayerButton = QPushButton("+")
            addPlayerButton.setStyleSheet(f"background-color: {ACTION_BUTTONS_ACTIVE_COLOR}")
            addPlayerButton.clicked.connect(partial(self.updatePlayerSlot,index))
            addPlayerButton.setMinimumWidth(BADGE_SIZE)
            addPlayerButton.setMaximumWidth(BADGE_SIZE)
            removePlayerButton = QPushButton("-")
            removePlayerButton.setStyleSheet(f"background-color: {ACTION_BUTTONS_ACTIVE_COLOR}")
            removePlayerButton.clicked.connect(partial(self.removePlayerSlot,index))
            removePlayerButton.setMinimumWidth(BADGE_SIZE)
            removePlayerButton.setMaximumWidth(BADGE_SIZE)
            thisActionsLayout.addWidget(addPlayerButton)
            thisActionsLayout.addWidget(removePlayerButton)
            thisActionsLayout.addStretch(1)

            playerCardSlot["PlayerCard"] = thisPlayerCard
            playerCardSlot["PlayerCardLayout"] = playerCardLayout
            playerCardSlot["PlayerCardContainer"] = playerCardContainer
            playerCardSlot["BadgesLayout"] = thisBadgesLayout
            playerCardSlot["BadgesContainer"] = thisBadgesContainerWidget
            playerCardSlot["ActionsLayout"] = thisActionsLayout
            playerCardSlot["ActionsContainer"] = thisActionsContainerWidget
            playerCardSlot["Actions"]["AddPlayerButton"] = addPlayerButton
            playerCardSlot["Actions"]["RemovePlayerButton"] = removePlayerButton

            if(index < 5):
                playerCardSlot["MainLayout"].addWidget(thisBadgesContainerWidget)
                playerCardSlot["MainLayout"].addWidget(playerCardContainer)
                playerCardSlot["MainLayout"].addWidget(thisActionsContainerWidget)
                self.ballerzLayout.addWidget(playerCardSlot["MainContainer"])
            else:
                playerCardSlot["MainLayout"].addWidget(thisActionsContainerWidget)
                playerCardSlot["MainLayout"].addWidget(playerCardContainer)
                playerCardSlot["MainLayout"].addWidget(thisBadgesContainerWidget)
                self.ringersLayout.addWidget(playerCardSlot["MainContainer"])
        self.adjustPlayerCardsToGameMode(self.gameMode)


        #endregion Player Card Slots UI

        #region Mid Layout UI

        self.pickerTitleLayout = QVBoxLayout()
        self.pickerTitleHeader = QLabel("Premier")
        self.pickerTitleHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pickerTitleHeader.setFont(MID_TITLE_HEADER_FONT)
        self.pickerTitleSubtext = QLabel("Standard 5-Ban")
        self.pickerTitleSubtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pickerTitleSubtext.setFont(MID_TITLE_SUBTEXT_FONT)
        self.pickerTitleLayout.addWidget(self.pickerTitleHeader)
        self.pickerTitleLayout.addWidget(self.pickerTitleSubtext)
        self.midLayout.addLayout(self.pickerTitleLayout)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.midLayout.addSpacerItem(spacer)
        phaseContainerWidget = QWidget()
        self.phaseLayout = QVBoxLayout(phaseContainerWidget)
        self.phaseHeaderLabel = QLabel("")
        self.phaseHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phaseSubtextLabel = QLabel("No Rules Set")
        self.phaseSubtextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phaseLayout.addWidget(self.phaseHeaderLabel)
        self.phaseLayout.addWidget(self.phaseSubtextLabel)

        self.midLayout.addWidget(phaseContainerWidget)
        self.selectedPlayerCard = PlayerCard()
        self.midLayout.addWidget(self.selectedPlayerCard)
        self.midLayout.addSpacerItem(spacer)

        #endregion Mid Layout UI

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

        # Connect to global spriteID
        globalAppState.currentSpriteIDChanged.connect(self.updateCurrentPlayerSelected)
        self.updateCurrentPlayerSelected(globalAppState.currentSpriteID)

        self.currentSelectorSpriteID = None
        self.ballerzBans = {}
        self.ballerzBansRemaining = 2
        self.ringersBans = {}
        self.ringersBansRemaining = 0
        self.currentPhase = 0
        self.phases = phaseOrder

        self.setPhase(2)

    # Helper method to adjust player slots to fit the given game mode.
    def adjustPlayerCardsToGameMode(self,gameMode):
        for index,playerCardSlot in enumerate(self.playerCardSlots):
            if (0 <= index <= gameMode - 1 or 5 <= index <= gameMode + 4):
                playerCardSlot["PlayerCard"].show()
                playerCardSlot["BadgesContainer"].show()
                playerCardSlot["ActionsContainer"].show()
            else:
                playerCardSlot["PlayerCard"].hide()
                playerCardSlot["BadgesContainer"].hide()
                playerCardSlot["ActionsContainer"].hide()

    # Method for updating the center player selection widget.
    def updateCurrentPlayerSelected(self,spriteID = None):
        self.currentSelectorSpriteID = spriteID
        self.selectedPlayerCard.setSpriteID(spriteID)
    # Method for adding a play to the given slot.
    def updatePlayerSlot(self,slot):
        if(self.currentSelectorSpriteID is not None and self.currentSelectorSpriteID in [playerCardSection["PlayerCard"].spriteID for playerCardSection in self.playerCardSlots]):
            return False
        elif(self.currentSelectorSpriteID in self.ballerzBans.keys() or self.currentSelectorSpriteID in self.ringersBans.keys()):
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
            newBadgeImage = QPixmap(self.badges[badgeName]["Path"]).scaled(BADGE_SIZE,BADGE_SIZE)
            newBadge.setPixmap(newBadgeImage)
            newBadge.setMinimumWidth(BADGE_SIZE)
            newBadge.setMaximumWidth(BADGE_SIZE)
            newBadge.setMinimumHeight(BADGE_SIZE)
            newBadge.setMaximumHeight(BADGE_SIZE)
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

    # Methods to add and remove bans to a given side.
    def ban(self,spriteID,ballerz : bool):
        #TODO handle cases when trying to ban players that are already selected or already banned.
        if(spriteID in self.ballerzBans.keys() or spriteID in self.ringersBans.keys()):
            return False
        elif((ballerz and self.ballerzBansRemaining == 0) or (not ballerz and self.ringersBansRemaining == 0)):
            return False
        else:
            newBanPlayerCard = PlayerCard(spriteID=spriteID,size="icon")
            if(ballerz):
                self.ballerzBans[spriteID] = newBanPlayerCard
                self.ballerzBanListLayout.addWidget(newBanPlayerCard)
                self.ballerzBansRemaining -= 1

            else:
                self.ringersBans[spriteID] = newBanPlayerCard
                self.ringersBanListLayout.addWidget(newBanPlayerCard)
                self.ringersBansRemaining -= 1

            if (self.ballerzBansRemaining > 0):
                self.ballerzBanButton.setEnabled(True)
            else:
                self.ballerzBanButton.setEnabled(False)
            if (self.ringersBansRemaining > 0):
                self.ringersBanButton.setEnabled(True)
            else:
                self.ringersBanButton.setEnabled(False)
    def unban(self,spriteID):
        if(spriteID in self.ballerzBans.keys()):
            self.ballerzBans[spriteID].hide()
            self.ballerzBanListLayout.removeWidget(self.ballerzBans[spriteID])
            del self.ballerzBans[spriteID]
            self.ballerzBansRemaining += 1
        if(spriteID in self.ringersBans.keys()):
            self.ringersBans[spriteID].hide()
            self.ringersBanListLayout.removeWidget(self.ringersBans[spriteID])
            del self.ringersBans[spriteID]
            self.ringersBansRemaining += 1

    # Method to lock and unlock the given slot, setting its interactivity
    def lockSlot(self,slotID):
        if(not self.playerCardSlots[slotID]["IsLocked"]):
            self.playerCardSlots[slotID]["IsLocked"] = True
            self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setEnabled(False)
            self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setStyleSheet(f"background-color: {ACTION_BUTTONS_INACTIVE_COLOR}")
            self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setEnabled(False)
            self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setStyleSheet(f"background-color: {ACTION_BUTTONS_INACTIVE_COLOR}")
            self.addBadge(slotID,"Padlock")
    def unlockSlot(self,slotID):
        if(self.playerCardSlots[slotID]["IsLocked"]):
            self.playerCardSlots[slotID]["IsLocked"] = False
            self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setEnabled(True)
            self.playerCardSlots[slotID]["Actions"]["AddPlayerButton"].setStyleSheet(f"background-color: {ACTION_BUTTONS_ACTIVE_COLOR}")
            self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setEnabled(True)
            self.playerCardSlots[slotID]["Actions"]["RemovePlayerButton"].setStyleSheet(f"background-color: {ACTION_BUTTONS_ACTIVE_COLOR}")
            self.removeBadge(slotID,"Padlock")

    # Method to set the current phase to the given index.
    def setPhase(self,phaseIndex):
        if(phaseIndex >= len(self.phases)):
            raise ValueError(f"Attempted to set invalid phase '{phaseIndex}', when there are only {len(self.phases)} phases configured!")

        self.phaseHeaderLabel.setText(f"Phase {phaseIndex + 1}")
        self.phaseSubtextLabel.setText(self.phases[phaseIndex]["Desc"])

        #TODO come back for specific game modes (4v4, 3v3)
        # Unlock all slots set to pick for this phase, lock all others
        allPicks = self.phases[phaseIndex].get("Picks", [])
        for i in range(10):
            if(i in allPicks):
                self.unlockSlot(i)
            else:
                self.lockSlot(i)

        self.ballerzBansRemaining = self.phases[phaseIndex].get("BallerzBans",0)
        self.ringersBansRemaining = self.phases[phaseIndex].get("RingersBans",0)

        if(self.ballerzBansRemaining > 0):
            self.ballerzBanButton.setEnabled(True)
        else:
            self.ballerzBanButton.setEnabled(False)
        if(self.ringersBansRemaining > 0):
            self.ringersBanButton.setEnabled(True)
        else:
            self.ringersBanButton.setEnabled(False)
    # This method tests to determine whether the current phase is completely satisfied (all bans banned,
    # all slots picked)
    def testPhaseCompletion(self):
        allSlotsFilled = True
        for slotID in self.phases[self.currentPhase]["Picks"]:
            if(self.playerCardSlots[slotID]["PlayerCard"].spriteID is None):
                allSlotsFilled = False
                break

        if(allSlotsFilled and self.ballerzBansRemaining == 0 and self.ringersBansRemaining == 0):
            return True
        else:
            return False
