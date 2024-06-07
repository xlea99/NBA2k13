from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.gui.main_content.picker_menu import PickerMenu
from spritopia.gui.main_content.create_a_player import CreateAPlayer
from spritopia.gui.bottom_content.premier_game_options import PremierGameOptions


class MainContentOuterWidget(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setObjectName("MainContentOuterWidget")
        self.outerContainer = QWidget()
        self.setCentralWidget(self.outerContainer)
        self.outerLayout = QVBoxLayout(self.outerContainer)  # Main layout
        self.outerLayout.setContentsMargins(0,0,0,0)
        self.outerLayout.setSpacing(0)
        #self.setStyleSheet("""
        ##MainContentOuterWidget {
        #    background-color: #1e3059;
        #}
        #""")


        #region === Middle Content ===

        self.middleContents = {}
        self.middleContentContainer = QWidget()
        self.middleContentContainer.setObjectName("middleContentArea")
        self.middleContentContainer.setStyleSheet("#middleContentArea {border: 1px solid black;}")
        self.middleContentLayout = QVBoxLayout(self.middleContentContainer)
        self.outerLayout.addWidget(self.middleContentContainer,5)

        # All middle contents
        self.middleContents["Premier_Picker"] = PickerMenu()
        self.middleContents["Premier_CAP"] = CreateAPlayer()

        #endregion === Middle Content ===

        #region === Bottom Content ===

        self.bottomContents = {}
        self.bottomContentContainer = QWidget()
        self.bottomContentContainer.setObjectName("bottomContentArea")
        self.bottomContentContainer.setStyleSheet("#bottomContentArea {border: 1px solid black;}")
        self.bottomContentLayout = QVBoxLayout(self.bottomContentContainer)
        self.outerLayout.addWidget(self.bottomContentContainer,3)
        self.bottomContentLayout.setSpacing(0)
        self.bottomContentLayout.setContentsMargins(0, 0, 0, 0)

        self.bottomContentContainer.setStyleSheet("""
        #BottomContentWidget {
            background-color: #1e3059;
        }
        """)

        # All bottom contents
        self.bottomContents["Premier_GameOptions"] = PremierGameOptions()

        #endregion === Bottom Content ===

        #region === Menu Bar ===

        menuBar = self.menuBar()
        premierMenu = menuBar.addMenu("Premier")
        premierMenu_playAction = premierMenu.addAction("Play")
        premierMenu_playAction.triggered.connect(self.goto_premier_picker)
        premierMenu_capAction = premierMenu.addAction("Create Player(s)")
        premierMenu_capAction.triggered.connect(self.goto_premier_cap)

        gauntletMenu = menuBar.addMenu("Gauntlet")
        gauntletMenu.addAction("Hub")
        gauntletMenu.addAction("God Room")

        #endregion === Menu Bar ===


    # Helper methods to update specific content areas with the given content ID. #TODO modify these later to support contents that need to be reinitialized on update
    def updateMiddleContent(self,contentID):
        if(contentID not in self.middleContents.keys() and contentID is not None):
            raise ValueError(f"Middle content '{contentID}' does not exist or has not yet been initialized!")

        # Clear the layout
        while self.middleContentLayout.count():
            thisItem = self.middleContentLayout.takeAt(0)
            widget = thisItem.widget()
            if widget:
                widget.setParent(None)

        if(contentID is not None):
            self.middleContentLayout.addWidget(self.middleContents[contentID])
    def updateBottomContent(self,contentID):
        if(contentID not in self.bottomContents.keys() and contentID is not None):
            raise ValueError(f"Bottom content '{contentID}' does not exist or has not yet been initialized!")

        # Clear the layout
        while self.bottomContentLayout.count():
            thisItem = self.bottomContentLayout.takeAt(0)
            widget = thisItem.widget()
            if widget:
                widget.setParent(None)

        if(contentID is not None):
            self.bottomContentLayout.addWidget(self.bottomContents[contentID])

    # All menu functions for navigation
    def goto_premier_picker(self):
        self.updateMiddleContent("Premier_Picker")
        self.updateBottomContent("Premier_GameOptions")
    def goto_premier_cap(self):
        self.updateMiddleContent("Premier_CAP")
        self.updateBottomContent(None)