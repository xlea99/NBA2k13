from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
import sys

# Create an instance of QApplication
app = QApplication(sys.argv)

# Get a list of all available font families directly from the QFontDatabase class
available_fonts = QFontDatabase.families()

# Print the list of available fonts
for font in available_fonts:
    print(font)