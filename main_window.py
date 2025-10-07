"""
Main window/landing page for the barangay registration system.
Provides navigation to registration and admin sections.
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from styles import Styles
from dialogs import AdminLoginWindow
from register_window import RegisterWindow
from admin_dashboard import AdminDashboard
from statistics_window import StatisticsWindow


class MainWindow(QWidget):
    """Main landing page window"""

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("REGISTRATION")
        self.resize(900, 500)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        # Background image
        self.background = QLabel(self)
        pixmap = QPixmap("Borcelle University FINAL_BACKGROUND.png")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.resize(self.size())

        # Create buttons with custom sizes
        reg_button = self._create_button("REGISTER", self.open_register_window)
        admin_button = self._create_button("ADMIN", self.open_admin_login)
        stats_button = self._create_button("STATISTICS", self.open_statistics)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()

        button_row = QHBoxLayout()
        button_row.setSpacing(20)  # Space between buttons
        button_row.addStretch()
        button_row.addWidget(reg_button)
        button_row.addWidget(admin_button)
        button_row.addWidget(stats_button)
        button_row.addStretch()

        main_layout.addLayout(button_row)
        main_layout.addSpacing(83)

    def _create_button(self, text, callback):
        """Create a styled button with shadow effect"""
        button = QPushButton(text)

        # Custom stylesheet with larger dimensions
        button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: #0D47A1;
                border: 3px solid #0D47A1;
                background-color: white;
                border-radius: 12px;
                padding: 15px 35px;
            }
            QPushButton:hover {
                background-color: #0D47A1;
                color: white;
            }
        """)

        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)

        # Set button size - THIS IS KEY
        button.setMinimumWidth(120)  # Change this value to make buttons wider
        button.setMinimumHeight(20)  # Change this value to make buttons taller

        # Or use fixed size for exact dimensions
        # button.setFixedSize(250, 70)  # Uncomment this for exact size

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(Qt.GlobalColor.gray)
        button.setGraphicsEffect(shadow)

        return button

    def resizeEvent(self, event):
        """Handle window resize to scale background"""
        self.background.resize(self.size())

    def open_register_window(self):
        """Open the registration form window"""
        self.reg_window = RegisterWindow(self.db_manager, self)
        self.reg_window.show()
        self.hide()

    def open_admin_login(self):
        """Open admin login dialog and dashboard if successful"""
        login_dialog = AdminLoginWindow(self)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            self.admin_dashboard = AdminDashboard(self.db_manager, self)
            self.admin_dashboard.show()
            self.hide()

    def open_statistics(self):
        """Open statistics window"""
        self.stats_window = StatisticsWindow(self.db_manager, self)
        self.stats_window.show()
        self.hide()