from PySide6.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtCore import Qt


# This class provides text that automatically resizes itself to fit the maximum height
# and width of the label it exists in.
class AutoResizeLabel(QLabel):

    def __init__(self, text="", parent=None,baseFont=None):
        super().__init__(text, parent)

        if(baseFont is None):
            self.baseFont = self.font()
        else:
            self.baseFont = baseFont
        self.adjustFontSize()

    def adjustFontSize(self):
        # Create a QFont based on the current label font
        font = QFont(self.baseFont)

        lines = self.text().split('\n')

        # Start with a existing font size and decrease it until the text fits
        for font_size in range(font.pointSize(), 1, -1):
            font.setPointSize(font_size)
            # QFontMetrics gives us information about how the text will be rendered
            fm = QFontMetrics(font)

            # Measure each line's width and find the maximum
            maxLineWidth = max(fm.horizontalAdvance(line) for line in lines)

            # Check if the widest line fits within the current label size
            if maxLineWidth <= self.maximumWidth() and fm.height() * len(lines) <= self.maximumHeight():
                super().setFont(font)
                break

    # Override setFont to ensure this remembers the baseFont to refer back to.
    def setFont(self,font):
        super().setFont(font)
        self.baseFont = font

    def resizeEvent(self, event):
        # Call the base class method to ensure proper event handling
        super().resizeEvent(event)
        # Adjust the font size whenever the label is resized
        self.adjustFontSize()