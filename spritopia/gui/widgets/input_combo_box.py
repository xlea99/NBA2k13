from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow
from PySide6.QtCore import Qt


class InputComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.lineEdit().textEdited.connect(self.filterItems)

        self.all_items = []

    def addItem(self, icon, text, userData = ...):
        super().addItem(icon,text,userData)
        self.all_items.append({"icon": icon,"text": text,"userData": userData})

    # Method to handle filtering based on input
    def filterItems(self, text):
        # Temporarily disconnect the signal to avoid infinite recursion
        self.lineEdit().textEdited.disconnect()

        self.clear()
        filtered_items = [item for item in self.all_items if text.lower() in item["icon"].lower()]
        if(filtered_items):
            for filtered_item in filtered_items:
                super().addItem(filtered_item["icon"],filtered_item["text"],filtered_item["userData"])
        else:
            for thisItem in self.all_items:
                super().addItem(thisItem["icon"],thisItem["text"],thisItem["userData"])

        # Restore the text and cursor position
        self.lineEdit().setText(text)
        self.lineEdit().setCursorPosition(len(text))

        # Reconnect the signal
        self.lineEdit().textEdited.connect(self.filterItems)