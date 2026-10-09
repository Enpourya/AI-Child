"""
AIChild — Main Entry Point
A growing AI companion that learns and evolves with you
"""

import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.database import init_db, is_first_run, log_operation
from ui.styles import DARK_STYLE


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AIChild")
    app.setOrganizationName("AIChild")
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_STYLE)

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Initialize database
    init_db()

    # First run?
    if is_first_run():
        from ui.welcome_dialog import WelcomeDialog
        welcome = WelcomeDialog()
        welcome.setStyleSheet(DARK_STYLE)
        result = welcome.exec()
        if result != welcome.DialogCode.Accepted:
            sys.exit(0)

    # Launch main window
    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    log_operation("INFO", f"AIChild launched | Python {sys.version.split()[0]}")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
