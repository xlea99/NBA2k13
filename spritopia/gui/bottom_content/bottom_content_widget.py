from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.main_content.picker_menu import PickerMenu
from spritopia.gui.bottom_content.premier_game_options import PremierGameOptions


class BottomContentWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("BottomContentWidget")
        self.setContentsMargins(0,0,0,0)


        # Central widget setup
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)  # Main layout
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
        #BottomContentWidget {
            background-color: #1e3059;
        }
        """)

        #self.premierGameOptions = PremierGameOptions() #TODO TEMP DISABLED
        #self.layout.addWidget(self.premierGameOptions)