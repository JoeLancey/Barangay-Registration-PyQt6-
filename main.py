"""

mao ni sya ang entry point og mag initialize sa app sa main window
"""
import sys
from PyQt6.QtWidgets import QApplication
from database_manager import DatabaseManager
from main_window import MainWindow


def main():
    """Initialize and run the application"""
    # Create application instance
    app = QApplication(sys.argv)


    # Initialize database manager
    db_manager = DatabaseManager()

    # Create and show main window
    main_window = MainWindow(db_manager)
    main_window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()