from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from spritopia.data_storage import data_storage as d
from spritopia.gui.app_state import globalAppState



# This is one of the bottom half widgets that displays stats info. It displays all relevant player stats.
class PlayerStatsDisplay(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setup_stats_display()

        # connect global SpriteID change
        globalAppState.currentSpriteIDChanged.connect(self.update_stats)
        self.update_stats(globalAppState.currentSpriteID)

    def setup_stats_display(self):
        self.statsFrame = QFrame(self)
        self.statsFrame.setFrameShape(QFrame.StyledPanel)
        self.statsLayout = QGridLayout(self.statsFrame)

        # Header labels for the grid
        self.headerLabels = ["Stat Name", "Total", "Average"]
        for col, text in enumerate(self.headerLabels):
            label = QLabel(text)
            self.statsLayout.addWidget(label, 0, col)

        # Thick, translucent line
        headerLine = QFrame()
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setStyleSheet("border: 2px solid rgba(0, 0, 0, 50);")  # Adjust color and opacity here
        self.statsLayout.addWidget(headerLine, 1, 0, 1, -1)  # Span across all columns

        self.displayedStatNames = [
            "Games Played",
            "Points",
            "Defensive Rebounds",
            "Offensive Rebounds",
            "Points Per Assist",
            "Assist Count",
            "Steals",
            "Blocks",
            "Turnovers",
            "Insides Made",
            "Insides Attempted",
            "Threes Made",
            "Threes Attempted",
            "Fouls",
            "Dunks",
            "Layups"
        ]

        self.statsLabels = {}
        row_offset = 2  # Adjust for header and thick line
        for i, statName in enumerate(self.displayedStatNames, row_offset):
            rowIndex = i * 2  # Double the row index for each stat to accommodate separators
            self.statsLabels[statName] = {
                "TotalLabel": QLabel("N/A"),
                "AverageLabel": QLabel("N/A")
            }
            self.statsLayout.addWidget(QLabel(statName), rowIndex, 0)
            self.statsLayout.addWidget(self.statsLabels[statName]["TotalLabel"], rowIndex, 1)
            self.statsLayout.addWidget(self.statsLabels[statName]["AverageLabel"], rowIndex, 2)

            # Hazy, semi-transparent line after each row
            if i < len(self.displayedStatNames) + row_offset - 1:  # Avoid adding at the very end
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.setStyleSheet("border: 1px solid rgba(0, 0, 0, 25);")  # Adjust color and opacity here
                self.statsLayout.addWidget(separator, rowIndex + 1, 0, 1, -1)  # Span across all columns

        self.layout.addWidget(self.statsFrame)

    def update_stats(self, spriteID):
        if spriteID not in d.d.stats["Players"]:
            for statName in self.displayedStatNames:
                self.statsLabels[statName]["TotalLabel"].setText("0")
                if(statName == "Games Played"):
                    self.statsLabels[statName]["AverageLabel"].setText(f"-")
                else:
                    self.statsLabels[statName]["AverageLabel"].setText("0.00")
        else:
            for statName in self.displayedStatNames:
                totalValue = d.d.stats["Players"][spriteID]["Totals"].get(statName.replace(" ",""), 0)
                averageValue = d.d.stats["Players"][spriteID]["Averages"].get(statName.replace(" ",""), 0)
                self.statsLabels[statName]["TotalLabel"].setText(str(totalValue))
                if(statName == "Games Played"):
                    self.statsLabels[statName]["AverageLabel"].setText(f"-")
                else:
                    self.statsLabels[statName]["AverageLabel"].setText(f"{averageValue:.2f}")