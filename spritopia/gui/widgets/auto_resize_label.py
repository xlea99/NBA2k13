from PySide6.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtCore import Qt
import re
import sys

# This class provides text that automatically resizes itself to fit the maximum height
# and width of the label it exists in. AutoWrap automatically ensures only one word is on
# each wrapped line.
class AutoResizeLabel(QLabel):

    def __init__(self, text="", parent=None, baseFont=None, autoWrap=False):
        super().__init__(text, parent)
        self.autoWrap = autoWrap
        self.setWordWrap(self.autoWrap)
        self.baseFont = baseFont if baseFont is not None else self.font()
        self.adjustFontSize()

    def adjustFontSize(self):
        if not self.text():
            return

        # Prepare the font and metrics
        font = QFont(self.baseFont)
        fm = QFontMetrics(font)

        # Define a range for font sizes with a more practical minimum size
        min_size, max_size = 8, 100  # Increased minimum size for readability
        last_good_size = max(self.font().pointSize(), min_size)  # Start from the current font size

        while min_size < max_size:
            font_size = (min_size + max_size) // 2
            font.setPointSize(font_size)
            fm = QFontMetrics(font)

            if self.autoWrap:
                rect = fm.boundingRect(0, 0, self.width(), 10000, Qt.TextWordWrap | Qt.TextExpandTabs, self.text())
            else:
                rect = fm.boundingRect(self.text())

            if rect.height() <= self.height() and rect.width() <= self.width():
                last_good_size = font_size
                min_size = font_size + 1
            else:
                max_size = font_size

        # Apply last good size ensuring it doesn't drop below min_size
        font.setPointSize(max(last_good_size, min_size) - 2)
        self.setFont(font)

    def setText(self, text):
        super().setText(text)
        self.adjustFontSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustFontSize()
