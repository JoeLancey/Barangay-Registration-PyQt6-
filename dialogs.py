"""
Dialog windows for the barangay registration system.
Contains login and record update dialogs.
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from styles import Styles
import re


class AdminLoginWindow(QDialog):
    """Admin authentication dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Login")
        self.setFixedSize(400, 250)
        self.setModal(True)
        self._center_on_parent(parent)
        self.setStyleSheet(Styles.DIALOG_BASE)
        self._setup_ui()

    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 400) // 2
            y = parent_geo.y() + (parent_geo.height() - 250) // 2
            self.move(x, y)

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Admin Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #0D47A1;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)

        # Form fields
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter username")
        self.username_field.setMinimumHeight(40)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Enter password")
        self.password_field.setMinimumHeight(40)

        self.username_field.setStyleSheet(Styles.LOGIN_FIELD_STYLE)
        self.password_field.setStyleSheet(Styles.LOGIN_FIELD_STYLE)

        label_style = "font-weight: 600; color: #333333; font-size: 14px;"
        username_label = QLabel("Username:")
        password_label = QLabel("Password:")
        username_label.setStyleSheet(label_style)
        password_label.setStyleSheet(label_style)

        form_layout.addRow(username_label, self.username_field)
        form_layout.addRow(password_label, self.password_field)
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.cancel_btn = QPushButton("Cancel")

        self.login_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        self.cancel_btn.setStyleSheet(Styles.BUTTON_DANGER)

        button_layout.addStretch()
        button_layout.addWidget(self.login_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        # Connect signals
        self.login_btn.clicked.connect(self.login)
        self.cancel_btn.clicked.connect(self.reject)
        self.password_field.returnPressed.connect(self.login)
        self.username_field.returnPressed.connect(self.password_field.setFocus)
        self.username_field.setFocus()

    def login(self):
        """Validate credentials and accept if valid"""
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()

        if username == "admin" and password == "admin123":
            self.accept()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Login Failed")
            msg.setText("Invalid username or password!\nPlease check your credentials and try again.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel { 
                    color: black; 
                }
                QPushButton {
                    background-color: #0D47A1;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)
            msg.exec()

            self.password_field.clear()
            self.username_field.setFocus()
            self.username_field.selectAll()


class UpdateRecordDialog(QDialog):
    """Dialog for updating existing resident records"""

    def __init__(self, record, parent=None):
        super().__init__(parent)
        self.record = record.copy()
        self.setWindowTitle("Update Record")
        self.setModal(True)
        self.resize(800, 600)
        self._center_on_parent(parent)
        self.setStyleSheet("QDialog { background-color: white; font-family: 'Segoe UI'; }")
        self._setup_ui()

    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 800) // 2
            y = parent_geo.y() + (parent_geo.height() - 600) // 2
            self.move(x, y)

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # Title
        title = QLabel("Update Registration Record")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0D47A1; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(8)
        form_widget.setStyleSheet(Styles.FORM_FIELD_STYLE)

        self._create_form_fields(form_layout)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Changes")
        cancel_btn = QPushButton("Cancel")

        save_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        cancel_btn.setStyleSheet(Styles.BUTTON_DANGER)

        save_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def _add_section_header(self, title_text, layout, row):
        """Add a section header to the form"""
        label = QLabel(title_text)
        label.setStyleSheet("font-size: 13px; font-weight: bold; color: #1565C0; margin: 8px 0 4px 0; padding: 0;")
        layout.addWidget(label, row, 0, 1, 4)
        return row + 1

    def _create_form_fields(self, form_layout):
        """Create all form input fields"""
        row = 0

        # Personal Information Section
        row = self._add_section_header("Personal Information", form_layout, row)

        self.surname = QLineEdit(self.record['surname'])
        self.surname.setPlaceholderText("Enter surname")
        form_layout.addWidget(QLabel("Surname: *"), row, 0)
        form_layout.addWidget(self.surname, row, 1)

        self.firstname = QLineEdit(self.record['firstname'])
        self.firstname.setPlaceholderText("Enter first name")
        form_layout.addWidget(QLabel("First Name: *"), row, 2)
        form_layout.addWidget(self.firstname, row, 3)

        row += 1
        self.middlename = QLineEdit(self.record['middlename'])
        self.middlename.setPlaceholderText("Enter middle name (optional)")
        form_layout.addWidget(QLabel("Middle Name:"), row, 0)
        form_layout.addWidget(self.middlename, row, 1)

        # Sex selection
        sex_layout = QHBoxLayout()
        sex_layout.setSpacing(20)
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")

        if self.record['sex'] == 'Male':
            self.male_radio.setChecked(True)
        else:
            self.female_radio.setChecked(True)

        sex_layout.addWidget(self.male_radio)
        sex_layout.addWidget(self.female_radio)
        sex_layout.addStretch()

        sex_widget = QWidget()
        sex_widget.setLayout(sex_layout)
        sex_widget.setMinimumHeight(35)
        sex_widget.setStyleSheet("QWidget { background-color: transparent; border: none; padding: 5px; }")

        form_layout.addWidget(QLabel("Sex: *"), row, 2)
        form_layout.addWidget(sex_widget, row, 3)

        row += 1
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("dd/MM/yyyy")
        self.dob.setDate(QDate.fromString(self.record['dob'], "dd/MM/yyyy"))
        self.dob.setMinimumHeight(28)
        # Apply consistent styling with register_window
        self.dob.setStyleSheet("""
            QDateEdit {
                padding: 8px 12px;
                border: 2px solid #999999;
                border-radius: 6px;
                font-size: 12px;
                background-color: white;
                color: black;
                min-width: 200px;
                min-height: 20px;
            }
            QDateEdit:focus {
                border: 2px solid #1976D2;
                background-color: #ffffff;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
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
        """)
        form_layout.addWidget(QLabel("Date of Birth: *"), row, 0)
        form_layout.addWidget(self.dob, row, 1)

        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setValue(self.record['age'])
        form_layout.addWidget(QLabel("Age:"), row, 2)
        form_layout.addWidget(self.age, row, 3)

        row += 1
        self.birthplace = QLineEdit(self.record['birthplace'])
        self.birthplace.setPlaceholderText("e.g., Davao City")
        form_layout.addWidget(QLabel("Place of Birth:"), row, 0)
        form_layout.addWidget(self.birthplace, row, 1)

        self.civil_status = QComboBox()
        self.civil_status.addItems(["Single", "Married", "Widowed", "Separated", "Divorced"])
        self.civil_status.setCurrentText(self.record['civil_status'])
        self.civil_status.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Civil Status:"), row, 2)
        form_layout.addWidget(self.civil_status, row, 3)

        row += 1
        self.nationality = QLineEdit(self.record['nationality'])
        self.nationality.setPlaceholderText("e.g., Filipino")
        form_layout.addWidget(QLabel("Nationality:"), row, 0)
        form_layout.addWidget(self.nationality, row, 1, 1, 3)

        # Contact Information Section
        row = self._add_section_header("Contact Information", form_layout, row + 1)

        self.street = QComboBox()
        self.street.addItems([
            "Select Street", "Gold Street", "Bronze Street", "Silver Street",
            "Platinum Street", "Diamond Street", "Pearl Street", "Ruby Street",
            "Emerald Street", "Sapphire Street", "Jade Street"
        ])
        self.street.setCurrentText(self.record['street'])
        self.street.setMinimumHeight(35)
        form_layout.addWidget(QLabel("Street: *"), row, 0)
        form_layout.addWidget(self.street, row, 1, 1, 3)

        row += 1
        self.contact_number = QLineEdit(self.record['contact_number'])
        self.contact_number.setPlaceholderText("09XXXXXXXXX (11 digits)")
        self.contact_number.setMaxLength(11)
        # Only allow digits
        contact_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.contact_number.setValidator(contact_validator)
        form_layout.addWidget(QLabel("Contact Number: *"), row, 0)
        form_layout.addWidget(self.contact_number, row, 1)

        self.email = QLineEdit(self.record['email'])
        self.email.setPlaceholderText("example@email.com")
        form_layout.addWidget(QLabel("Email Address:"), row, 2)
        form_layout.addWidget(self.email, row, 3)

        # Residency Information Section
        row = self._add_section_header("Residency Information", form_layout, row + 1)

        self.years_residency = QSpinBox()
        self.years_residency.setRange(0, 120)
        self.years_residency.setValue(self.record['years_residency'])
        form_layout.addWidget(QLabel("Years of Residency:"), row, 0)
        form_layout.addWidget(self.years_residency, row, 1)

        self.voter_id = QLineEdit(self.record['voter_id'])
        self.voter_id.setPlaceholderText("1234-5678-9012 or 123456789012")
        self.voter_id.setMaxLength(20)
        form_layout.addWidget(QLabel("Voter's ID / No.:"), row, 2)
        form_layout.addWidget(self.voter_id, row, 3)

        row += 1
        self.household_relation = QLineEdit(self.record['household_relation'])
        self.household_relation.setPlaceholderText("e.g., Head of Family, Spouse")
        form_layout.addWidget(QLabel("Household Relation:"), row, 0)
        form_layout.addWidget(self.household_relation, row, 1, 1, 3)

        # Emergency Contact Section
        row = self._add_section_header("Emergency Contact", form_layout, row + 1)

        self.emergency_name = QLineEdit(self.record['emergency_name'])
        self.emergency_name.setPlaceholderText("Full name of emergency contact")
        form_layout.addWidget(QLabel("Name:"), row, 0)
        form_layout.addWidget(self.emergency_name, row, 1)

        self.emergency_relation = QLineEdit(self.record['emergency_relation'])
        self.emergency_relation.setPlaceholderText("e.g., Spouse, Parent, Sibling")
        form_layout.addWidget(QLabel("Relationship:"), row, 2)
        form_layout.addWidget(self.emergency_relation, row, 3)

        row += 1
        self.emergency_contact = QLineEdit(self.record['emergency_contact'])
        self.emergency_contact.setPlaceholderText("09XXXXXXXXX (11 digits)")
        self.emergency_contact.setMaxLength(11)
        emergency_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.emergency_contact.setValidator(emergency_validator)
        form_layout.addWidget(QLabel("Contact Number:"), row, 0)
        form_layout.addWidget(self.emergency_contact, row, 1, 1, 3)

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

    def save_changes(self):
        """Validate and save updated record"""
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
            self.street.setFocus()
            return

        # Validate contact number (required field)
        if not self.contact_number.text().strip():
            self._show_message(QMessageBox.Icon.Warning,
                               "Missing Information",
                               "Contact Number is required.")
            self.contact_number.setFocus()
            return

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

        # If all validations pass, accept the dialog
        self.accept()

    def get_updated_record(self):
        """Return dictionary of updated field values"""
        return {
            'surname': self.surname.text(),
            'firstname': self.firstname.text(),
            'middlename': self.middlename.text(),
            'sex': 'Male' if self.male_radio.isChecked() else 'Female',
            'dob': self.dob.date().toString("dd/MM/yyyy"),
            'age': self.age.value(),
            'birthplace': self.birthplace.text(),
            'civil_status': self.civil_status.currentText(),
            'nationality': self.nationality.text(),
            'street': self.street.currentText(),
            'contact_number': self.contact_number.text(),
            'email': self.email.text(),
            'years_residency': self.years_residency.value(),
            'voter_id': self.voter_id.text(),
            'household_relation': self.household_relation.text(),
            'emergency_name': self.emergency_name.text(),
            'emergency_relation': self.emergency_relation.text(),
            'emergency_contact': self.emergency_contact.text()
        }
