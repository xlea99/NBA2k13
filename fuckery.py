from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QPushButton, QApplication
import sys
import BaseFunctions as b

class FunWidget1(QWidget):
    def __init__(self, parent=None):
        super(FunWidget1, self).__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("I am Fun Widget 1")
        layout.addWidget(label)
        self.setLayout(layout)

class FunWidget2(QWidget):
    def __init__(self, parent=None):
        super(FunWidget2, self).__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("I am Fun Widget 2")
        layout.addWidget(label)
        self.setLayout(layout)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # Main Holder as Central Widget
        self.mainHolder1 = QFrame(self)
        self.setCentralWidget(self.mainHolder1)
        self.mainLayout = QVBoxLayout()
        self.mainHolder1.setLayout(self.mainLayout)

        # Initialize the current widget to None
        self.currentWidget = None

        # Button to swap widgets
        self.button1 = QPushButton("Load FunWidget1")
        self.button2 = QPushButton("Load FunWidget2")

        self.button1.clicked.connect(self.load_funWidget1)
        self.button2.clicked.connect(self.load_funWidget2)

        self.mainLayout.addWidget(self.button1)
        self.mainLayout.addWidget(self.button2)

    def remove_current_widget(self):
        if self.currentWidget is not None:
            self.currentWidget.deleteLater()
        self.currentWidget = None

    def load_funWidget1(self):
        self.remove_current_widget()
        self.currentWidget = FunWidget1(self)
        self.mainLayout.addWidget(self.currentWidget)

    def load_funWidget2(self):
        self.remove_current_widget()
        self.currentWidget = FunWidget2(self)
        self.mainLayout.addWidget(self.currentWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())