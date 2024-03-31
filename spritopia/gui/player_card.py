from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage import data_storage as d
from spritopia.utilities import misc
from spritopia.gui import const
from spritopia.gui import utils

# Simple, classy widget for displaying a player's info in a compact way.
class PlayerCard(QWidget):

    NAME_FONT = QFont("Arial",24)
    NAME_FONT.setUnderline(True)
    GAMES_FONT = QFont("Arial",7)

    # Basic setup init method.
    def __init__(self,parent=None,spriteID = None):
        super().__init__(parent)

        self.setObjectName("playerCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.backgroundColor = "grey"
        self.borderColor = "black"

        self.spriteID = spriteID

        self.setMinimumHeight(120)
        self.setMaximumHeight(120)
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

        self.outerLayout = QVBoxLayout(self)
        self.upperHalfLayout = QVBoxLayout()
        self.lowerHalfLayout = QVBoxLayout()
        self.outerLayout.addLayout(self.upperHalfLayout)
        self.outerLayout.addLayout(self.lowerHalfLayout)

        # Upper half config
        self.playerLabelLayout = QHBoxLayout()
        self.playerLabelLayout.setContentsMargins(4,1,4,1)
        self.archetypeLabel = QLabel()
        self.archetypeLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.heightLabel = QLabel()
        self.heightLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.nameLayout = QVBoxLayout()
        self.nameLayout.setSpacing(0)
        self.nameLabel = QLabel()
        self.nameLabel.setMaximumWidth(0.817 * self.width())
        self.nameLabel.setFont(self.NAME_FONT)
        self.nameLabel.setStyleSheet("color: black")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.gamesLabel = QLabel()
        self.gamesLabel.setMaximumWidth(self.nameLabel.maximumWidth())
        self.gamesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.gamesLabel.setFont(self.GAMES_FONT)
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.gamesLabel)
        self.playerLabelLayout.addWidget(self.archetypeLabel)
        self.playerLabelLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.playerLabelLayout.addLayout(self.nameLayout)
        self.playerLabelLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.playerLabelLayout.addWidget(self.heightLabel)

        self.upperHalfLayout.addLayout(self.playerLabelLayout)

        # Lower half config
        self.statsLabel = QLabel()
        self.statsLabel.setMaximumWidth(self.maximumWidth())
        self.statsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.attributeLabel = QLabel()
        self.attributeLabel.setMaximumWidth(self.maximumWidth())
        self.attributeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lowerHalfLayout.addWidget(self.statsLabel)
        self.lowerHalfLayout.addWidget(self.attributeLabel)
        self.lowerHalfLayout.setContentsMargins(1,0,1,1)


        self.outerLayout.setContentsMargins(1, 1, 1, 2)
        self.configureStyle()
        self.setSpriteID(self.spriteID)

    archetypeStatsToShow = {"Slayer" : {""}}
    # This method sets the player to the given SpriteID, and updates the contents.
    def setSpriteID(self,spriteID):
        self.spriteID = spriteID
        if(self.spriteID is None):
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

            self.nameLabel.setText(d.d.players[spriteID].getFullName())
            utils.dynamicallyResizeFont(self.nameLabel,baseFont=self.NAME_FONT)

            try:
                self.gamesLabel.setText(f"Games: {d.d.stats['Players'][spriteID]['Totals']['GamesPlayed']} (<i>{d.d.stats['Players'][spriteID]['Averages']['Wins']*100:.1f}%</i> W/L)")
            except KeyError:
                self.gamesLabel.setText(f"0 <i>(0.0%)</i>")
            utils.dynamicallyResizeFont(self.gamesLabel,baseFont=self.GAMES_FONT)

            self.statsLabel.setText(" | ".join(statStrings[statType] for statType in archetypeStatLabels[archetypeName]))
            self.attributeLabel.setText(" | ".join(attributeStrings[attributeType] for attributeType in archetypeAttributeLabels[archetypeName]))
            utils.dynamicallyResizeFont(self.statsLabel)
            utils.dynamicallyResizeFont(self.attributeLabel)

    # Helper method to reconfigure the stylesheet of the PlayerCard.
    def configureStyle(self,backgroundColor=None,borderColor=None):
        if(backgroundColor):
            self.backgroundColor = backgroundColor
        if(borderColor):
            self.borderColor = borderColor
        self.setStyleSheet(f".PlayerCard#playerCard {{ border: 3px solid {self.borderColor}; "
                           f"background: {self.backgroundColor}; "
                           f"padding: 3px; }}")
