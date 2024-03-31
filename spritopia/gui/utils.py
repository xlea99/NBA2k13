from PySide6.QtGui import *
from PySide6.QtWidgets import *



# Helper method to dynamically resize font based on label width.
def dynamicallyResizeFont(label: QLabel,baseFont = None):
    # Retrieve the text from the QLabel
    text = label.text()

    # Use the current width of the label
    current_width = label.maximumWidth()

    # Initial font and font size
    if(baseFont):
        label.setFont(baseFont)
    font = label.font()


    # Create QFontMetrics for measuring text width
    fm = QFontMetrics(font)

    # Check if the text width is within the bounds of current width
    text_width = fm.horizontalAdvance(text)
    while text_width > current_width and font.pointSize() > 1:  # Ensure the font size never goes below 1
        # Decrease font size
        font.setPointSize(font.pointSize() - 1)
        # Update QFontMetrics with the new font size
        fm = QFontMetrics(font)
        # Recalculate text width
        text_width = fm.horizontalAdvance(text)

    # Set the adjusted font to the label
    label.setFont(font)