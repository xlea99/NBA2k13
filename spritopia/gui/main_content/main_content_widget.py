from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.main_content.picker_menu import PickerMenu


class MainContentWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainContentWidget")

        # Central widget setup
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)  # Main layout

        self.setStyleSheet("""
        #MainContentWidget {
            background-color: #1e3059;
        }
        """)

        self.pickerMenuWidget = PickerMenu(self)
        self.layout.addWidget(self.pickerMenuWidget)