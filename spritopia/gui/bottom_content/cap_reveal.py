from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.widgets.player_card import PlayerCard


class CAPReveal(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        self.mainLayout = QHBoxLayout(self)

        thisName = "Mahatma Gandhi"

        testPlayerCard1 = PlayerCard()
        testPlayerCard1.setSpriteID(thisName)
        testPlayerCard1.setSize("Box")
        self.mainLayout.addWidget(testPlayerCard1)

        testPlayerCard2 = PlayerCard()
        testPlayerCard2.setSpriteID(thisName)
        testPlayerCard2.setSize("Wide")
        self.mainLayout.addWidget(testPlayerCard2)

        testPlayerCard3 = PlayerCard()
        testPlayerCard3.setSpriteID(thisName)
        testPlayerCard3.setSize("Icon")
        self.mainLayout.addWidget(testPlayerCard3)