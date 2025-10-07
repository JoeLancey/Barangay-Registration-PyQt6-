"""
Dialog windows for the barangay registration system.
Contains login and record update dialogs.
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from styles import Styles


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
            msg.setStyleSheet("QLabel { color: black; }")
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
        self.setStyleSheet(Styles.DIALOG_BASE)
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

        # Title
        title = QLabel("Update Registration Record")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0D47A1; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setSpacing(10)
        form_widget.setStyleSheet(Styles.FIELD_STYLE)

        self._create_form_fields(form_layout)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Changes")
        cancel_btn = QPushButton("Cancel")

        save_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        cancel_btn.setStyleSheet(Styles.BUTTON_DANGER)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def _create_form_fields(self, form_layout):
        """Create all form input fields"""
        row = 0

        # Personal Information
        self.surname = QLineEdit(self.record['surname'])
        form_layout.addWidget(QLabel("Surname:"), row, 0)
        form_layout.addWidget(self.surname, row, 1)

        self.firstname = QLineEdit(self.record['firstname'])
        form_layout.addWidget(QLabel("First Name:"), row, 2)
        form_layout.addWidget(self.firstname, row, 3)

        row += 1
        self.middlename = QLineEdit(self.record['middlename'])
        form_layout.addWidget(QLabel("Middle Name:"), row, 0)
        form_layout.addWidget(self.middlename, row, 1)

        # Sex selection
        sex_layout = QHBoxLayout()
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
        form_layout.addWidget(QLabel("Sex:"), row, 2)
        form_layout.addWidget(sex_widget, row, 3)

        row += 1
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("dd/MM/yyyy")
        self.dob.setDate(QDate.fromString(self.record['dob'], "dd/MM/yyyy"))
        form_layout.addWidget(QLabel("Date of Birth:"), row, 0)
        form_layout.addWidget(self.dob, row, 1)

        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setValue(self.record['age'])
        form_layout.addWidget(QLabel("Age:"), row, 2)
        form_layout.addWidget(self.age, row, 3)

        row += 1
        self.birthplace = QLineEdit(self.record['birthplace'])
        form_layout.addWidget(QLabel("Place of Birth:"), row, 0)
        form_layout.addWidget(self.birthplace, row, 1)

        self.civil_status = QComboBox()
        self.civil_status.addItems(["Single", "Married", "Widowed", "Separated", "Divorced"])
        self.civil_status.setCurrentText(self.record['civil_status'])
        form_layout.addWidget(QLabel("Civil Status:"), row, 2)
        form_layout.addWidget(self.civil_status, row, 3)

        row += 1
        self.nationality = QLineEdit(self.record['nationality'])
        form_layout.addWidget(QLabel("Nationality:"), row, 0)
        form_layout.addWidget(self.nationality, row, 1, 1, 3)

        # Contact Information
        row += 1
        self.street = QComboBox()
        self.street.addItems([
            "Select Street", "Gold Street", "Bronze Street", "Silver Street",
            "Platinum Street", "Diamond Street", "Pearl Street", "Ruby Street",
            "Emerald Street", "Sapphire Street", "Jade Street"
        ])
        self.street.setCurrentText(self.record['street'])
        form_layout.addWidget(QLabel("Street:"), row, 0)
        form_layout.addWidget(self.street, row, 1, 1, 3)

        row += 1
        self.contact_number = QLineEdit(self.record['contact_number'])
        form_layout.addWidget(QLabel("Contact Number:"), row, 0)
        form_layout.addWidget(self.contact_number, row, 1)

        self.email = QLineEdit(self.record['email'])
        form_layout.addWidget(QLabel("Email:"), row, 2)
        form_layout.addWidget(self.email, row, 3)

        # Residency Information
        row += 1
        self.years_residency = QSpinBox()
        self.years_residency.setRange(0, 120)
        self.years_residency.setValue(self.record['years_residency'])
        form_layout.addWidget(QLabel("Years of Residency:"), row, 0)
        form_layout.addWidget(self.years_residency, row, 1)

        self.voter_id = QLineEdit(self.record['voter_id'])
        form_layout.addWidget(QLabel("Voter's ID:"), row, 2)
        form_layout.addWidget(self.voter_id, row, 3)

        row += 1
        self.household_relation = QLineEdit(self.record['household_relation'])
        form_layout.addWidget(QLabel("Household Relation:"), row, 0)
        form_layout.addWidget(self.household_relation, row, 1, 1, 3)

        # Emergency Contact
        row += 1
        self.emergency_name = QLineEdit(self.record['emergency_name'])
        form_layout.addWidget(QLabel("Emergency Name:"), row, 0)
        form_layout.addWidget(self.emergency_name, row, 1)

        self.emergency_relation = QLineEdit(self.record['emergency_relation'])
        form_layout.addWidget(QLabel("Emergency Relation:"), row, 2)
        form_layout.addWidget(self.emergency_relation, row, 3)

        row += 1
        self.emergency_contact = QLineEdit(self.record['emergency_contact'])
        form_layout.addWidget(QLabel("Emergency Contact:"), row, 0)
        form_layout.addWidget(self.emergency_contact, row, 1, 1, 3)

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