from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.widgets.player_card_base import PlayerCardBase
from spritopia.gui.widgets.player_reveal_card import PlayerRevealCard
from spritopia.gui.app_state import globalAppState


class CAPReveal(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        self.mainLayout = QHBoxLayout(self)

        self.testPlayerCard1 = PlayerRevealCard()
        self.mainLayout.addWidget(self.testPlayerCard1)
        globalAppState.currentSpriteIDChanged.connect(self.updateTestThing)


    def updateTestThing(self,spriteID):
        self.testPlayerCard1.setSpriteID(spriteID)


        #self.playerCards = []
        #for index, spriteID in enumerate(listOfSpriteIDs):
        #    newPlayer = PlayerRevealCard()
        #    newPlayer.setSpriteID(spriteID)
        #    self.playerCards.append(newPlayer)
        #
        #    self.mainLayout.addWidget(newPlayer)
        #


            #playerCard[2]