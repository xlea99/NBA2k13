from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
import string


class HoverableImageLabel(QLabel):
    """
    A QLabel that shows an enlarged preview card when hovered, containing a title,
    an image, and a description.

    The preview_position parameter determines where the preview card will appear relative
    to the original widget:
      - "top_left": The card’s bottom-right aligns with the widget's top-left.
      - "top_right": The card’s bottom-left (with an offset) aligns with the widget's top-right.
    """

    def __init__(self, defaultSize: QSize, hoverSize: QSize, preview_position="top_left", parent=None):
        super().__init__(parent)
        self.defaultSize = defaultSize
        self.hoverSize = hoverSize  # used for scaling the image in the hover card
        self.preview_position = preview_position  # "top_left" (default) or "top_right"

        # Set the initial fixed size to the default size.
        self.setFixedSize(self.defaultSize)
        self.originalPixmap = None
        self.title = ""
        self.description = ""

        # Create a widget for the enlarged preview card.
        self.previewWidget = QWidget(None)
        self.previewWidget.setWindowFlags(Qt.ToolTip)
        self.previewWidget.setAttribute(Qt.WA_TransparentForMouseEvents)
        # Style the card with a border, background, and text color.
        self.previewWidget.setStyleSheet("border: 2px solid #444444; background-color: #2e2e2e; color: white;")

        # Set up a vertical layout for the preview card.
        layout = QVBoxLayout(self.previewWidget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)

        # Title label (displayed above the image).
        self.titleLabel = QLabel(self.previewWidget)
        self.titleLabel.setStyleSheet("font-weight: bold;")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        layout.addWidget(self.titleLabel)

        # Image label (the enlarged image).
        self.imageLabel = QLabel(self.previewWidget)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)

        # Description label (displayed below the image).
        self.descLabel = QLabel(self.previewWidget)
        self.descLabel.setWordWrap(True)
        self.descLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.descLabel)

        self.previewWidget.hide()

        # Enable mouse tracking so hover events are received.
        self.setMouseTracking(True)

    def setPixmap(self, pixmap: QPixmap):
        """
        Save the original pixmap and display the scaled default version in this label.
        """
        self.originalPixmap = pixmap
        scaled = pixmap.scaled(self.defaultSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super().setPixmap(scaled)

    def setTitle(self, title: str):
        """
        Set the title for the preview card.
        """
        self.title = title

    def setDescription(self, description: str):
        """
        Set the description for the preview card.
        """
        self.description = description

    def setCardData(self, pixmap: QPixmap, title: str, description: str):
        """
        Set the data for the hover preview card, including the image, title, and description.
        """
        self.setPixmap(pixmap)
        self.setTitle(title)
        self.setDescription(description)

    def enterEvent(self, event):
        """
        When the mouse enters the widget, show the enlarged preview card near it.
        The popup's width is forced to be as wide as the image (if one exists).
        """
        if self.originalPixmap:
            # Scale the original pixmap for the hover card.
            scaled = self.originalPixmap.scaled(self.hoverSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel.setPixmap(scaled)
            pixmap_width = scaled.width()

            # Update the title and description on the card.
            self.titleLabel.setText(self.title)
            self.descLabel.setText(self.description)

            # Restrict the title and description to not exceed the image's width.
            self.titleLabel.setMaximumWidth(pixmap_width)
            self.descLabel.setMaximumWidth(pixmap_width)

            # Calculate the total width (image width plus layout margins) and set it.
            margins = self.previewWidget.layout().contentsMargins()
            total_width = pixmap_width + margins.left() + margins.right()
            self.previewWidget.setFixedWidth(total_width)

            # Update the widget size to the content.
            self.previewWidget.adjustSize()

            # Determine the global position of this widget and calculate where the card should appear.
            if self.preview_position == "top_right":
                # Position so that the card's bottom-left aligns with the widget's top-right (with a horizontal offset).
                globalPos = self.mapToGlobal(self.rect().topRight())
                movePos = QPoint(globalPos.x() + 10, globalPos.y() - self.previewWidget.height())
            else:
                # Default ("top_left"): position so that the card's bottom-right aligns with the widget's top-left.
                globalPos = self.mapToGlobal(self.rect().topLeft())
                movePos = QPoint(globalPos.x() - self.previewWidget.width(),
                                 globalPos.y() - self.previewWidget.height())

            self.previewWidget.move(movePos)
            self.previewWidget.show()

        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        Hide the enlarged preview card when the mouse leaves.
        """
        self.previewWidget.hide()
        super().leaveEvent(event)
