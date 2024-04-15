from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
import sys
import os

for thisPath in os.listdir("C:\\Crap\\Coding\\Python\\NBA2k13\\data\\music\\songs\\nba"):
    print(thisPath.split(".json")[0])

