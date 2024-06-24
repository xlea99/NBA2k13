from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage import data_storage as d
from spritopia.utilities import misc
from spritopia.gui import const
from spritopia.gui import utils
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel

NAME_FONT_WIDE = QFont("Arial", 24)
NAME_FONT_WIDE.setUnderline(True)
NAME_FONT_ICON = QFont("Arial", 16)
NAME_FONT_ICON.setBold(True)
GAMES_FONT = QFont("Arial", 7)

# Simple, classy widget for displaying a player's info in a compact way.
class PlayerCard(QWidget):

    # Basic setup init method.
    def __init__(self,parent=None,spriteID = None,size = "Wide"):
        super().__init__(parent)

        self.setObjectName("playerCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.backgroundColor = "grey"
        self.borderColor = "black"
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)

        #region === Name/Title ===

        self.__titleContainer = QWidget()
        self.__titleLayout = QVBoxLayout(self.__titleContainer)
        self.__titleLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.__titleContainer)
        self.__title_mainContentContainer = QWidget()
        self.__title_mainContentLayout = QHBoxLayout(self.__title_mainContentContainer)
        self.__title_mainContentLayout.setContentsMargins(0,0,0,0)
        self.__titleLayout.addWidget(self.__title_mainContentContainer)
        self.__title_extraContentContainer = QWidget()
        self.__title_extraContentLayout = QHBoxLayout(self.__title_extraContentContainer)
        self.__title_extraContentLayout.setContentsMargins(0,0,0,0)
        self.__titleLayout.addWidget(self.__title_extraContentContainer)

        # Player Name
        self.__title_playerNameLabel = AutoResizeLabel(autoWrap=True)
        self.__title_playerNameLabel.setObjectName("PlayerName")
        self.__title_playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.__title_mainContentLayout.addWidget(self.__title_playerNameLabel)

        #endregion === Name/Title ===


        self.__spriteID = spriteID
        self.__sizeID = "Wide"
        self.__sizeHint = QSize(64,64) # Should be immediately overridden
        self.setSize(size)
        self.configureStyle()
        self.setSpriteID(self.__spriteID)

    def __setToBoxSize(self):
        self.__sizeHint = QSize(300,300)
        self.setMaximumHeight(300)
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)

        #region === Name/Title ===

        self.__title_mainContentContainer.show()
        self.__title_extraContentContainer.show()
        self.__title_playerNameLabel.setMaximumWidth(0.817 * self.width())

        # endregion === Name/Title ===



        self.__sizeID = "wide"
    def __setToWideSize(self):
        self.__sizeHint = QSize(300,120)
        self.setMaximumHeight(120)
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)

        #region === Name/Title ===

        self.__title_mainContentContainer.show()
        self.__title_extraContentContainer.show()
        self.__title_playerNameLabel.setMaximumWidth(0.817 * self.width())

        # endregion === Name/Title ===

        self.__sizeID = "wide"
    def __setToIconSize(self):
        self.__sizeHint = QSize(64, 64)
        self.setMaximumHeight(64)
        self.setMaximumWidth(64)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        #region === Name/Title ===

        self.__title_mainContentContainer.show()
        self.__title_extraContentContainer.hide()
        self.__title_playerNameLabel.setMaximumWidth(0.9 * self.width())

        # endregion === Name/Title ===

        self.__sizeID = "icon"




    # This method sets the player to the given SpriteID, and updates the contents.
    def setSpriteID(self,spriteID):
        self.__spriteID = spriteID
        if(True):
            self.__title_playerNameLabel.setText(str(spriteID))
        else:
            if(self.__spriteID is None):
                self.archetypeLabel.setText("N")
                self.heightLabel.setText("")
                self.nameLabel.setText("")
                self.gamesLabel.setText("---")
                self.statsLabel.setText("")
                self.attributeLabel.setText("")
                self.configureStyle(borderColor="grey")
            else:
                try:
                    statStrings = {"W/L": f"W/L: {d.d.stats['Players'][spriteID]['Averages']['Wins'] * 100:04.1f}%",
                                   "Games": f"{d.d.stats['Players'][spriteID]['Totals']['GamesPlayed']} Games, {d.d.stats['Players'][spriteID]['Averages']['Wins'] * 100:04.1f}% W/L",
                                   "PPG": f"PPG: {d.d.stats['Players'][spriteID]['Averages']['Points']:<4.1f}",
                                   "3P%": f"3P%: {d.d.stats['Players'][spriteID]['Other']['ThreePercentage'] * 100:04.1f}%",
                                   "RPG": f"RPG: {d.d.stats['Players'][spriteID]['Averages']['OffensiveRebounds'] + d.d.stats['Players'][spriteID]['Averages']['DefensiveRebounds']:3.1f}",
                                   "TPT": f"TPT: {misc.getTimeString(d.d.stats['Players'][spriteID]['Other']['TimePerTurnover'])}",
                                   "SPG": f"SPG: {d.d.stats['Players'][spriteID]['Averages']['Steals']:.1f}",
                                   "APG": f"APG: {d.d.stats['Players'][spriteID]['Averages']['AssistCount']:.1f}",
                                   "3PA": f"3PA: {d.d.stats['Players'][spriteID]['Averages']['ThreesAttempted']:.1f}"}
                except KeyError:
                    statStrings = {"W/L": "W/L: ???",
                                   "Games": "Games: ???",
                                   "PPG": "PPG: ???",
                                   "3P%": "3P%: ???",
                                   "RPG": "RPG: ???",
                                   "TPT": "TPT: ???",
                                   "SPG": "SPG: ???",
                                   "APG": "APG: ???",
                                   "3PA": "3PA: ???"}
                attributeStrings = {"Sht3PT": f"Sht3PT: {d.d.players[spriteID]['SSht3PT']:02}",
                                    "ShtOffD": f"ShtOffD: {d.d.players[spriteID]['SShtOfD']:02}",
                                    "ShtTraff": f"ShtTraff: {d.d.players[spriteID]['SShtInT']:02}",
                                    "Speed": f"Speed: {d.d.players[spriteID]['SSpeed']:02}",
                                    "OReb": f"OReb: {d.d.players[spriteID]['SOReb']:02}",
                                    "DReb": f"DReb: {d.d.players[spriteID]['SDReb']:02}",
                                    "BSecure": f"BSecure: {d.d.players[spriteID]['SBallSec']:02}",
                                    "Hands": f"Hands: {d.d.players[spriteID]['SHands']:02}",
                                    "Consis": f"Consis: {d.d.players[spriteID]['SConsis']:02}",
                                    "DAware": f"DAware: {d.d.players[spriteID]['SDAwar']:02}",
                                    "OAware": f"OAware: {d.d.players[spriteID]['SOAwar']:02}",
                                    "Steal": f"Steal: {d.d.players[spriteID]['SSteal']:02}",
                                    "Strength": f"Strength: {d.d.players[spriteID]['SStrength']:02}",
                                    "Vertical": f"Vertical: {d.d.players[spriteID]['SVertical']:02}"}

                archetypeStatLabels = {"Slayer" : ("PPG","3P%","3PA","TPT"),
                                       "Vigilante" : ("PPG","3P%","RPG","TPT"),
                                       "Medic" : ("PPG","RPG","APG","TPT"),
                                       "Guardian" : ("PPG","RPG","3P%","TPT"),
                                       "Engineer" : ("PPG","RPG","APG","TPT"),
                                       "Director" : ("PPG","3P%","APG","TPT"),
                                       "None" : ("PPG","3P%","RPG","TPT")}
                archetypeAttributeLabels = {"Slayer" : ("Sht3PT","ShtOffD","Consis","Speed"),
                                            "Vigilante" : ("Sht3PT","ShtTraff","OReb","DReb"),
                                            "Medic" : ("OReb","DReb","Speed","Vertical"),
                                            "Guardian" : ("OReb","DReb","Sht3PT","Speed"),
                                            "Engineer" : ("BSecure","Steal","Speed","Vertical"),
                                            "Director" : ("Speed","BSecure","Steal","Sht3PT"),
                                            "None" : ("Sht3PT","Speed","OReb","DReb")}

                archetypeName = d.d.players[spriteID]['Archetype_Name']

                self.archetypeLabel.setText(f"{archetypeName[0]}")
                self.archetypeLabel.setStyleSheet(f"color: {const.ARCHETYPE_COLORS[archetypeName]}")
                self.configureStyle(borderColor=const.ARCHETYPE_COLORS[archetypeName])

                self.heightLabel.setText(f"{d.d.players[spriteID]['HeightFt']}")

                if(self.__sizeID.lower() == "wide"):
                    self.nameLabel.setText(d.d.players[spriteID].getFullName())
                elif(self.__sizeID.lower() == "icon"):
                    self.nameLabel.setText(d.d.players[spriteID].getFullName().replace(" ","\n"))


                try:
                    self.gamesLabel.setText(f"Games: {d.d.stats['Players'][spriteID]['Totals']['GamesPlayed']} (<i>{d.d.stats['Players'][spriteID]['Averages']['Wins']*100:.1f}%</i> W/L)")
                except KeyError:
                    self.gamesLabel.setText(f"0 <i>(0.0%)</i>")

                self.statsLabel.setText(" | ".join(statStrings[statType] for statType in archetypeStatLabels[archetypeName]))
                self.attributeLabel.setText(" | ".join(attributeStrings[attributeType] for attributeType in archetypeAttributeLabels[archetypeName]))

    # Helper method to reconfigure the stylesheet of the PlayerCard.
    def configureStyle(self,backgroundColor=None,borderColor=None):
        if(backgroundColor):
            self.backgroundColor = backgroundColor
        if(borderColor):
            self.borderColor = borderColor
        self.setStyleSheet(f".PlayerCard#playerCard {{ border: 3px solid {self.borderColor}; "
                           f"background: {self.backgroundColor}; "
                           f"padding: 3px; }}")

    # Sets the "size" of this player card. Sizes are preconfigured modes to display
    # more or less data depending on spatial needs.
    def setSize(self,size):
        if(size.lower() == "wide"):
            self.__setToWideSize()
        elif(size.lower() == "icon"):
            self.__setToIconSize()
        elif(size.lower() == "box"):
            self.__setToBoxSize()
        else:
            raise ValueError(f"Invalid size type: '{size}'")
        self.setSpriteID(self.__spriteID)
    # Override for the sizehint
    def sizeHint(self):
        return self.__sizeHint

