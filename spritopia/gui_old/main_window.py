from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from spritopia.gui_old.sidebar.player_finder import PlayerFinder
from spritopia.gui_old.data_model import DataModel
import sys


class GUIMainWindow(QMainWindow):


    def __init__(self, parent = None):
        super().__init__(parent)

        self.dataModel = DataModel()

        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)

        # Build the three sections of the main window.
        mainContentSkeleton = QWidget()
        self.mainContentLayout = QVBoxLayout(mainContentSkeleton)
        secondaryContentSkeleton = QWidget()
        self.secondaryContentLayout = QVBoxLayout(secondaryContentSkeleton)
        sidebarSkeleton = QWidget()
        self.sidebarLayout = QVBoxLayout(sidebarSkeleton)

        contentContainer = QWidget()
        contentLayout = QVBoxLayout(contentContainer)
        contentLayout.setSpacing(0)
        contentLayout.setContentsMargins(0,0,0,0)
        contentLayout.addWidget(mainContentSkeleton,stretch=6)
        contentLayout.addWidget(secondaryContentSkeleton,stretch=3)

        #region === Build Sidebar ===

        self.playerFinder = PlayerFinder(dataModel=self.dataModel)
        self.sidebarLayout.addWidget(self.playerFinder,stretch=1)

        self.sidebarLayout.addStretch(2)


        #endregion === Build Sidebar ===

        self.mainLayout.addWidget(sidebarSkeleton,stretch=3)
        self.mainLayout.addWidget(contentContainer,stretch=8)


        self.showMaximized()



app = QApplication()
window = GUIMainWindow()
window.show()
sys.exit(app.exec())



