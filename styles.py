
"""
Centralized stylesheet definitions for the barangay registration system.
naa diri mga UI styles para ma reuse nako sya
"""


class Styles:
    """Container for all application stylesheets"""

    DIALOG_BASE = """
        QDialog {
            background-color: white;
            font-family: 'Segoe UI';
        }
    """

    FIELD_STYLE = """
        QLineEdit, QSpinBox, QDateEdit, QComboBox {
            padding: 8px;
            border: 2px solid #999999;
            border-radius: 6px;
            font-size: 13px;
            background-color: white;
            color: black;
        }
        QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QComboBox:focus {
            border: 2px solid #1976D2;
        }
        QLabel {
            font-weight: 600;
            color: #333333;
            font-size: 13px;
        }
        QRadioButton {
            font-size: 13px;
            color: black;
        }
    """

    FORM_FIELD_STYLE = """
        QLineEdit, QSpinBox, QDateEdit, QComboBox {
            background-color: white;
            color: black;
            padding: 8px 12px;
            border: 2px solid #999999;
            border-radius: 6px;
            min-width: 200px;
            min-height: 20px;
            font-size: 12px;
        }
        QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QComboBox:focus {
            border: 2px solid #1976D2;
            background-color: #ffffff;
        }
        QSpinBox::up-button, QSpinBox::down-button,
        QDateEdit::up-button, QDateEdit::down-button {
            background-color: transparent;
            border: none;
            width: 20px;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            border: 2px solid #1976D2;
            selection-background-color: #E3F2FD;
            selection-color: #1976D2;
            padding: 4px;
        }
        QComboBox QAbstractItemView::item {
            color: black;
            padding: 6px;
            min-height: 20px;
        }
        QLabel {
            font-weight: 600;
            color: #333333;
            font-size: 12px;
        }
        QRadioButton {
            font-size: 12px;
            color: black;
            font-weight: 500;
            spacing: 5px;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
        }
        QRadioButton::indicator:unchecked {
            border: 2px solid #999999;
            border-radius: 9px;
            background-color: white;
        }
        QRadioButton::indicator:checked {
            border: 2px solid #1976D2;
            border-radius: 9px;
            background-color: #1976D2;
        }
    """

    BUTTON_PRIMARY = """
        QPushButton {
            background-color: #1976D2;
            color: white;
            font-weight: 600;
            padding: 10px 30px;
            border-radius: 6px;
            font-size: 13px;
            border: none;
        }
        QPushButton:hover {
            background-color: #1565C0;
        }
    """

    BUTTON_DANGER = """
        QPushButton {
            background-color: #E53935;
            color: white;
            font-weight: 600;
            padding: 10px 30px;
            border-radius: 6px;
            font-size: 13px;
            border: none;
        }
        QPushButton:hover {
            background-color: #D32F2F;
        }
    """

    BUTTON_WARNING = """
        QPushButton {
            background-color: #FF9800;
            color: white;
            font-weight: 600;
            padding: 10px 25px;
            border-radius: 6px;
            font-size: 13px;
            min-width: 120px;
            border: none;
        }
        QPushButton:hover {
            background-color: #F57C00;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """

    BUTTON_SUCCESS = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            font-weight: 600;
            padding: 10px 25px;
            border-radius: 6px;
            font-size: 13px;
            min-width: 120px;
            border: none;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """

    BUTTON_SECONDARY = """
        QPushButton {
            background-color: #607D8B;
            color: white;
            font-weight: 600;
            padding: 10px 25px;
            border-radius: 6px;
            font-size: 13px;
            min-width: 120px;
            border: none;
        }
        QPushButton:hover {
            background-color: #546E7A;
        }
    """

    BUTTON_MAIN_WINDOW = """
        QPushButton {
            font-size: 14px;
            font-weight: bold;
            color: #0D47A1;
            border: 2px solid #0D47A1;
            background-color: white;
            border-radius: 12px;
            padding: 8px 20px;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #0D47A1;
            color: white;
        }
    """

    TABLE_STYLE = """
        QTableWidget {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 0px;
            gridline-color: #f5f5f5;
            font-size: 13px;
            font-family: 'Segoe UI', Arial;
        }
        QTableWidget::item {
            padding: 12px 15px;
            color: #333333;
            border-bottom: 1px solid #f0f0f0;
        }
        QTableWidget::item:selected {
            background-color: #f8f9fa;
            color: #1976D2;
        }
        QTableWidget::item:hover {
            background-color: #fafafa;
        }
        QHeaderView::section {
            background-color: #fafafa;
            color: #424242;
            padding: 14px 15px;
            border: none;
            border-bottom: 2px solid #e0e0e0;
            border-right: 1px solid #f0f0f0;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        QHeaderView::section:hover {
            background-color: #f5f5f5;
        }
        QTableWidget QScrollBar:vertical {
            border: none;
            background: #fafafa;
            width: 10px;
            margin: 0px;
        }
        QTableWidget QScrollBar::handle:vertical {
            background: #cccccc;
            min-height: 30px;
            border-radius: 5px;
        }
        QTableWidget QScrollBar::handle:vertical:hover {
            background: #999999;
        }
        QTableWidget QScrollBar::add-line:vertical,
        QTableWidget QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QTableWidget QScrollBar:horizontal {
            border: none;
            background: #fafafa;
            height: 10px;
            margin: 0px;
        }
        QTableWidget QScrollBar::handle:horizontal {
            background: #cccccc;
            min-width: 30px;
            border-radius: 5px;
        }
        QTableWidget QScrollBar::handle:horizontal:hover {
            background: #999999;
        }
        QTableWidget QScrollBar::add-line:horizontal,
        QTableWidget QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """

    LOGIN_FIELD_STYLE = """
        QLineEdit {
            padding: 10px;
            border: 2px solid #999999;
            border-radius: 6px;
            font-size: 14px;
            min-width: 200px;
            background-color: white;
            color: #333333;
            selection-background-color: #0D47A1;
            selection-color: white;
        }
        QLineEdit:focus {
            border: 2px solid #0D47A1;
            background-color: #ffffff;
        }
        QLineEdit::placeholder {
            color: #888888;
            font-style: italic;
        }
    """
