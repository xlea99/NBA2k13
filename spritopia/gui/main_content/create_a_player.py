from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.common.paths import paths
from spritopia.gui import const
from spritopia.gui.widgets.player_card import PlayerCard
from spritopia.gui.app_state import globalAppState


# Class for providing the Picker Menu
class CreateAPlayer(QWidget):

    # Initialize UI and tracking variables
    def __init__(self,parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
