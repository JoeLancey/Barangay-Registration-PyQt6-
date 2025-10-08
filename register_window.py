"""
Registration form window for new resident records.
diri mag register ang mga tao
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from styles import Styles
import re


class RegisterWindow(QWidget):
    """Registration form window"""

    def __init__(self, db_manager, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.main_window = main_window
        self.setWindowTitle("Barangay Registration Form")
        self.showMaximized()
        self.setStyleSheet("background-color: white; font-family: 'Segoe UI'; font-size: 18px;")
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(0)

        # Title
        title = QLabel("Barangay Registration Form")
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #0D47A1;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Scroll Area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        # Form container
        form_container = QWidget()
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(6)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_container.setLayout(form_layout)

        # Enhanced form field style with explicit black text for all states
        form_container.setStyleSheet(Styles.FORM_FIELD_STYLE + """
            QLineEdit {
                color: black !important;
                background-color: white;
            }
            QLineEdit:focus {
                color: black !important;
            }
            QSpinBox {
                color: black !important;
                background-color: white;
            }
            QSpinBox:focus {
                color: black !important;
            }
            QComboBox {
                color: black !important;
                background-color: white;
            }
            QComboBox:focus {
                color: black !important;
            }
            QComboBox:editable {
                color: black !important;
            }
            QComboBox QAbstractItemView {
                color: black !important;
                background-color: white;
                selection-background-color: #E3F2FD;
                selection-color: black !important;
            }
            QTextEdit {
                color: black !important;
                background-color: white;
            }
            QTextEdit:focus {
                color: black !important;
            }
        """)

        # Create all form sections
        self._create_form_fields(form_layout)

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

    def _create_form_fields(self, form_layout):
        """Create all form input fields organized by section"""
        row = 0

        # Personal Information Section
        row = self._add_section_header("Personal Information", form_layout, row)

        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Enter surname")
        form_layout.addWidget(QLabel("Surname: *"), row, 0)
        form_layout.addWidget(self.surname, row, 1)

        self.firstname = QLineEdit()
        self.firstname.setPlaceholderText("Enter first name")
        form_layout.addWidget(QLabel("First Name: *"), row, 2)
        form_layout.addWidget(self.firstname, row, 3)

        row += 1
        self.middlename = QLineEdit()
        self.middlename.setPlaceholderText("Enter middle name (optional)")
        form_layout.addWidget(QLabel("Middle Name:"), row, 0)
        form_layout.addWidget(self.middlename, row, 1)

        # Sex selection
        sex_widget = self._create_sex_selection()
        form_layout.addWidget(QLabel("Sex: *"), row, 2)
        form_layout.addWidget(sex_widget, row, 3)

        row += 1
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("dd/MM/yyyy")
        self.dob.setDate(QDate.currentDate())
        self.dob.setMinimumHeight(28)
        # Style the calendar popup for visibility
        self.dob.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #999999;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: black;
            }
            QDateEdit:focus {
                border: 2px solid #1976D2;
            }
            QCalendarWidget {
                background-color: white;
                border: 2px solid #1976D2;
            }
            QCalendarWidget QWidget {
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                background-color: white;
                selection-background-color: #E3F2FD;
                selection-color: black;
                border: 1px solid #1976D2;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #BDBDBD;
            }
            QCalendarWidget QToolButton {
                color: black;
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #E3F2FD;
                border: 1px solid #1976D2;
            }
            QCalendarWidget QMenu {
                background-color: white;
                color: black;
            }
            QCalendarWidget QSpinBox {
                background-color: white;
                color: black;
                selection-background-color: #E3F2FD;
                selection-color: black;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
            }
        """)
        form_layout.addWidget(QLabel("Date of Birth: *"), row, 0)
        form_layout.addWidget(self.dob, row, 1)

        self.age = QSpinBox()
        self.age.setRange(0, 120)
        form_layout.addWidget(QLabel("Age:"), row, 2)
        form_layout.addWidget(self.age, row, 3)

        row += 1
        self.birthplace = QLineEdit()
        self.birthplace.setPlaceholderText("e.g., Davao City")
        form_layout.addWidget(QLabel("Place of Birth:"), row, 0)
        form_layout.addWidget(self.birthplace, row, 1)

        self.civil_status = QComboBox()
        self.civil_status.addItems(["Select Civil Status", "Single", "Married", "Widowed", "Separated", "Divorced"])
        self.civil_status.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Civil Status:"), row, 2)
        form_layout.addWidget(self.civil_status, row, 3)

        row += 1
        # Changed to ComboBox with common nationalities
        self.nationality = QComboBox()
        self.nationality.addItems([
            "Filipino", "American", "Chinese", "Japanese", "Korean",
            "British", "Australian", "Canadian", "Indian", "Other"
        ])
        self.nationality.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Nationality:"), row, 0)
        form_layout.addWidget(self.nationality, row, 1)

        # Contact Information Section
        row = self._add_section_header("Contact Information", form_layout, row + 1)

        self.street = QComboBox()
        self.street.addItems([
            "Select Street", "Gold Street", "Bronze Street", "Silver Street",
            "Platinum Street", "Diamond Street", "Pearl Street", "Ruby Street",
            "Emerald Street", "Sapphire Street", "Jade Street"
        ])
        self.street.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Street: *"), row, 0)
        form_layout.addWidget(self.street, row, 1, 1, 3)

        row += 1
        # Contact Number with validation (11 digits, starts with 09)
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("09XXXXXXXXX (11 digits)")
        self.contact_number.setMaxLength(11)
        # Only allow digits
        contact_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.contact_number.setValidator(contact_validator)
        form_layout.addWidget(QLabel("Contact Number: *"), row, 0)
        form_layout.addWidget(self.contact_number, row, 1)

        # Email with placeholder
        self.email = QLineEdit()
        self.email.setPlaceholderText("example@email.com")
        form_layout.addWidget(QLabel("Email Address:"), row, 2)
        form_layout.addWidget(self.email, row, 3)

        # Residency Information Section
        row = self._add_section_header("Residency Information", form_layout, row + 1)

        self.years_residency = QSpinBox()
        self.years_residency.setRange(0, 120)
        form_layout.addWidget(QLabel("Years of Residency:"), row, 0)
        form_layout.addWidget(self.years_residency, row, 1)

        # Voter's ID with validation (format: XXXX-XXXX-XXXX or numbers only)
        self.voter_id = QLineEdit()
        self.voter_id.setPlaceholderText("1234-5678-9012 or 123456789012")
        self.voter_id.setMaxLength(20)
        form_layout.addWidget(QLabel("Voter's ID / No.:"), row, 2)
        form_layout.addWidget(self.voter_id, row, 3)

        row += 1
        # Household Relation as ComboBox
        self.household_relation = QComboBox()
        self.household_relation.addItems([
            "Select Relation", "Head of Family", "Spouse", "Son", "Daughter",
            "Father", "Mother", "Brother", "Sister", "Grandfather", "Grandmother",
            "Grandson", "Granddaughter", "Uncle", "Aunt", "Nephew", "Niece",
            "Cousin", "Son-in-law", "Daughter-in-law", "Other"
        ])
        self.household_relation.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Household Relation:"), row, 0)
        form_layout.addWidget(self.household_relation, row, 1)

        # Emergency Contact Section
        row = self._add_section_header("Emergency Contact", form_layout, row + 1)

        self.emergency_name = QLineEdit()
        self.emergency_name.setPlaceholderText("Full name of emergency contact")
        form_layout.addWidget(QLabel("Name:"), row, 0)
        form_layout.addWidget(self.emergency_name, row, 1)

        # Emergency Relation as ComboBox
        self.emergency_relation = QComboBox()
        self.emergency_relation.addItems([
            "Select Relation", "Spouse", "Parent", "Sibling", "Child",
            "Grandparent", "Grandchild", "Uncle/Aunt", "Cousin",
            "Friend", "Neighbor", "Other"
        ])
        self.emergency_relation.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Relationship:"), row, 2)
        form_layout.addWidget(self.emergency_relation, row, 3)

        row += 1
        # Emergency Contact with same validation
        self.emergency_contact = QLineEdit()
        self.emergency_contact.setPlaceholderText("09XXXXXXXXX (11 digits)")
        self.emergency_contact.setMaxLength(11)
        emergency_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.emergency_contact.setValidator(emergency_validator)
        form_layout.addWidget(QLabel("Contact Number:"), row, 0)
        form_layout.addWidget(self.emergency_contact, row, 1)

        # Action Buttons
        button_widget = self._create_action_buttons()
        form_layout.addWidget(button_widget, row, 2, 1, 2)

    def _add_section_header(self, title_text, layout, row):
        """Add a section header to the form"""
        label = QLabel(title_text)
        label.setStyleSheet("font-size: 13px; font-weight: bold; color: #1565C0; margin: 8px 0 4px 0;")
        layout.addWidget(label, row, 0, 1, 4)
        return row + 1

    def _create_sex_selection(self):
        """Create radio button widget for sex selection"""
        sex_layout = QHBoxLayout()
        sex_layout.setSpacing(20)

        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.male_radio.setChecked(True)

        sex_layout.addWidget(self.male_radio)
        sex_layout.addWidget(self.female_radio)
        sex_layout.addStretch()

        sex_widget = QWidget()
        sex_widget.setLayout(sex_layout)
        sex_widget.setMinimumHeight(35)
        sex_widget.setStyleSheet("QWidget { background-color: transparent; border: none; padding: 5px; }")

        return sex_widget

    def _create_action_buttons(self):
        """Create action buttons (Add Record and Back)"""
        self.add_btn = QPushButton("Add Record")
        self.back_btn = QPushButton("Back")

        self.add_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        self.back_btn.setStyleSheet(Styles.BUTTON_DANGER)

        self.back_btn.clicked.connect(self.go_back)
        self.add_btn.clicked.connect(self.add_record)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.back_btn)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        return button_widget

    def _show_message(self, icon, title, text, buttons=QMessageBox.StandardButton.Ok):
        """Helper for styled QMessageBox with black text"""
        msg = QMessageBox(icon, title, text, buttons, self)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0D47A1;
            }
        """)
        return msg.exec()

    def _validate_contact_number(self, number, field_name):
        """Validate Philippine mobile number format"""
        if not number:
            return True  # Optional field

        if len(number) != 11:
            self._show_message(QMessageBox.Icon.Warning,
                               "Invalid Contact Number",
                               f"{field_name} must be exactly 11 digits.")
            return False

        if not number.startswith('09'):
            self._show_message(QMessageBox.Icon.Warning,
                               "Invalid Contact Number",
                               f"{field_name} must start with '09'.")
            return False

        return True

    def _validate_email(self, email):
        """Validate email format"""
        if not email:
            return True  # Optional field

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self._show_message(QMessageBox.Icon.Warning,
                               "Invalid Email",
                               "Please enter a valid email address.\nExample: user@example.com")
            return False
        return True

    def _validate_voter_id(self, voter_id):
        """Validate voter's ID format"""
        if not voter_id:
            return True  # Optional field

        # Remove hyphens for validation
        voter_id_clean = voter_id.replace('-', '').replace(' ', '')

        # Check if it contains only digits
        if not voter_id_clean.isdigit():
            self._show_message(QMessageBox.Icon.Warning,
                               "Invalid Voter's ID",
                               "Voter's ID should contain only numbers and hyphens.\nExample: 1234-5678-9012")
            return False

        # Check length (typically 12 digits for Philippine voter ID)
        if len(voter_id_clean) < 10 or len(voter_id_clean) > 20:
            self._show_message(QMessageBox.Icon.Warning,
                               "Invalid Voter's ID",
                               "Voter's ID should be between 10-20 digits.")
            return False

        return True

    def _validate_required_dropdowns(self):
        """Validate that required dropdowns are selected"""
        if self.street.currentText() == "Select Street":
            self._show_message(QMessageBox.Icon.Warning,
                               "Missing Information",
                               "Please select a street.")
            return False
        return True

    def add_record(self):
        """Validate and save new record to database"""
        # Required fields validation
        if not self.surname.text().strip():
            self._show_message(QMessageBox.Icon.Warning,
                               "Missing Information",
                               "Surname is required.")
            self.surname.setFocus()
            return

        if not self.firstname.text().strip():
            self._show_message(QMessageBox.Icon.Warning,
                               "Missing Information",
                               "First Name is required.")
            self.firstname.setFocus()
            return

        # Validate required dropdowns
        if not self._validate_required_dropdowns():
            return

        # Validate contact number
        if not self._validate_contact_number(self.contact_number.text(), "Contact Number"):
            self.contact_number.setFocus()
            return

        # Validate emergency contact
        if self.emergency_contact.text():
            if not self._validate_contact_number(self.emergency_contact.text(), "Emergency Contact Number"):
                self.emergency_contact.setFocus()
                return

        # Validate email
        if not self._validate_email(self.email.text()):
            self.email.setFocus()
            return

        # Validate voter ID
        if not self._validate_voter_id(self.voter_id.text()):
            self.voter_id.setFocus()
            return

        # Get values from ComboBoxes
        nationality_value = self.nationality.currentText()
        household_relation_value = self.household_relation.currentText()
        if household_relation_value == "Select Relation":
            household_relation_value = ""

        emergency_relation_value = self.emergency_relation.currentText()
        if emergency_relation_value == "Select Relation":
            emergency_relation_value = ""

        record = {
            'surname': self.surname.text().strip(),
            'firstname': self.firstname.text().strip(),
            'middlename': self.middlename.text().strip(),
            'sex': 'Male' if self.male_radio.isChecked() else 'Female',
            'dob': self.dob.date().toString("dd/MM/yyyy"),
            'age': self.age.value(),
            'birthplace': self.birthplace.text().strip(),
            'civil_status': self.civil_status.currentText(),
            'nationality': nationality_value,
            'street': self.street.currentText(),
            'contact_number': self.contact_number.text().strip(),
            'email': self.email.text().strip(),
            'years_residency': self.years_residency.value(),
            'voter_id': self.voter_id.text().strip(),
            'household_relation': household_relation_value,
            'emergency_name': self.emergency_name.text().strip(),
            'emergency_relation': emergency_relation_value,
            'emergency_contact': self.emergency_contact.text().strip()
        }

        self.db_manager.add_record(record)
        self._show_message(QMessageBox.Icon.Information, "Success", "Successfully Registered!")
        self.clear_form()

    def clear_form(self):
        """Reset all form fields to default values"""
        self.surname.clear()
        self.firstname.clear()
        self.middlename.clear()
        self.male_radio.setChecked(True)
        self.dob.setDate(QDate.currentDate())
        self.age.setValue(0)
        self.birthplace.clear()
        self.civil_status.setCurrentIndex(0)
        self.nationality.setCurrentIndex(0)  # Reset to "Filipino"
        self.street.setCurrentIndex(0)
        self.contact_number.clear()
        self.email.clear()
        self.years_residency.setValue(0)
        self.voter_id.clear()
        self.household_relation.setCurrentIndex(0)  # Reset to "Select Relation"
        self.emergency_name.clear()
        self.emergency_relation.setCurrentIndex(0)  # Reset to "Select Relation"
        self.emergency_contact.clear()

    def go_back(self):
        """Return to main window"""
        self.close()
        self.main_window.show()
