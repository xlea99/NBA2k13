from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.main_content.main_content_widget import MainContentWidget
from spritopia.gui.left_sidebar.left_sidebar_widget import LeftSidebarWidget
import sys


QApplication.setStyle("Fusion")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        #self.setWindowTitle("Spritopia Presents")
        #self.setGeometry(100, 100, 1200, 900)

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)  # Horizontal layout to hold sidebars and main content
        self.mainLayout.setSpacing(0)  # No space between widgets
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # No margins

        # Initialize left sidebar
        self.leftSidebar = LeftSidebarWidget()
        #sself.leftSidebar.setFixedWidth(400)
        self.mainLayout.addWidget(self.leftSidebar,1)


        # Initialize outer main content area
        self.mainContentOuter = QWidget()
        self.mainContentOuterLayout = QVBoxLayout(self.mainContentOuter)  # Placeholder layout
        self.mainContentOuterLayout.setSpacing(0)  # No space between widgets
        self.mainContentOuterLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.mainLayout.addWidget(self.mainContentOuter,3)  # Add to layout with stretch factor

        self.mainContent = MainContentWidget()
        self.mainContent.setObjectName("mainContentArea")
        self.mainContent.setStyleSheet("#mainContentArea {border: 1px solid black;}")  # TODO TEMP
        #self.mainContent.setStyleSheet("border: 1px solid black;")  # TODO TEMP

        self.bottomContent = QWidget()
        self.bottomContent.setObjectName("bottomContentArea")
        self.bottomContent.setStyleSheet("#bottomContentArea {border: 1px solid black;}") #TODO TEMP

        self.mainContentOuterLayout.addWidget(self.mainContent,2)
        self.mainContentOuterLayout.addWidget(self.bottomContent,1)

        self.leftSidebar.playerComboBox.currentIndexChanged.connect(
            lambda index: self.mainContent.pickerMenuWidget.updateCurrentPlayerSelected(self.leftSidebar.currentPlayer["SpriteID"]))
        self.mainContent.pickerMenuWidget.updateCurrentPlayerSelected(self.leftSidebar.currentPlayer["SpriteID"])

        self.showMaximized()



app = QApplication()
window = MainWindow()
window.show()
sys.exit(app.exec())