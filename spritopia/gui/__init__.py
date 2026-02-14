"""
Spritopia GUI - PySide6 Application

This package provides the graphical user interface for Spritopia.
"""

from spritopia.gui.main_window import MainWindow


def run():
    """Run the Spritopia GUI application."""
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Spritopia")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
