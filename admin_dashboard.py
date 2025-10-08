
"""
Admin dashboard maka view and manage records.

naa diri table view naay search, update, and delete na function.
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from styles import Styles
from dialogs import UpdateRecordDialog


class AdminDashboard(QWidget):
    """Admin dashboard window for managing resident records"""

    def __init__(self, db_manager, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.main_window = main_window
        self.setWindowTitle("Admin Dashboard")
        self.showMaximized()
        self.setStyleSheet("background-color: #f5f5f5; font-family: 'Segoe UI';")
        self._setup_ui()
        self.load_table_data()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Registration Records")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #0D47A1;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #333;")

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search by surname or first name...")
        self.search_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #999999;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-width: 300px;
                color: black;  /* Set text color to black */
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """)
        self.search_field.textChanged.connect(self.search_records)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_field)
        search_layout.addStretch()
        layout.addLayout(search_layout)

        # Table
        self.table = self._create_table()
        layout.addWidget(self.table)

        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)

    def _create_table(self):
        """Create and configure the records table"""
        table = QTableWidget()
        table.setColumnCount(17)
        table.setHorizontalHeaderLabels([
            "ID", "Surname", "First Name", "Middle Name", "Sex", "Date of Birth",
            "Age", "Place of Birth", "Civil Status", "Nationality",
            "Street", "Contact Number", "Email", "Years of Residency",
            "Voter's ID", "Household Relation", "Emergency Contact"
        ])

        table.setStyleSheet(Styles.TABLE_STYLE)
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        return table

    def _create_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()

        delete_btn = QPushButton("Delete Record")
        delete_btn.setStyleSheet(Styles.BUTTON_DANGER + """
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        delete_btn.clicked.connect(self.delete_record)

        update_btn = QPushButton("Update Record")
        update_btn.setStyleSheet(Styles.BUTTON_WARNING)
        update_btn.clicked.connect(self.update_record)

        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.setStyleSheet(Styles.BUTTON_SUCCESS)
        refresh_btn.clicked.connect(self.load_table_data)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.setStyleSheet(Styles.BUTTON_SECONDARY)
        back_btn.clicked.connect(self.go_back)

        button_layout.addWidget(delete_btn)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(back_btn)

        return button_layout

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

    def load_table_data(self):
        """Load registration records from database into the table"""
        self.table.setRowCount(0)
        self.search_field.clear()
        records = self.db_manager.get_all_records()
        self._populate_table(records)

    def search_records(self):
        """Search and filter records based on search field"""
        search_term = self.search_field.text().strip()
        self.table.setRowCount(0)

        if search_term:
            records = self.db_manager.search_records(search_term)
        else:
            records = self.db_manager.get_all_records()

        self._populate_table(records)

    def _populate_table(self, records):
        """Fill table with record data"""
        for record in records:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(str(record['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(record['surname']))
            self.table.setItem(row_position, 2, QTableWidgetItem(record['firstname']))
            self.table.setItem(row_position, 3, QTableWidgetItem(record['middlename']))
            self.table.setItem(row_position, 4, QTableWidgetItem(record['sex']))
            self.table.setItem(row_position, 5, QTableWidgetItem(record['dob']))
            self.table.setItem(row_position, 6, QTableWidgetItem(str(record['age'])))
            self.table.setItem(row_position, 7, QTableWidgetItem(record['birthplace']))
            self.table.setItem(row_position, 8, QTableWidgetItem(record['civil_status']))
            self.table.setItem(row_position, 9, QTableWidgetItem(record['nationality']))
            self.table.setItem(row_position, 10, QTableWidgetItem(record['street']))
            self.table.setItem(row_position, 11, QTableWidgetItem(record['contact_number']))
            self.table.setItem(row_position, 12, QTableWidgetItem(record['email']))
            self.table.setItem(row_position, 13, QTableWidgetItem(str(record['years_residency'])))
            self.table.setItem(row_position, 14, QTableWidgetItem(record['voter_id']))
            self.table.setItem(row_position, 15, QTableWidgetItem(record['household_relation']))
            self.table.setItem(row_position, 16, QTableWidgetItem(
                f"{record['emergency_name']} ({record['emergency_relation']}) - {record['emergency_contact']}"
            ))

        self.table.resizeColumnsToContents()

    def delete_record(self):
        """Delete the selected record from database"""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a record to delete.")
            return

        record_id = int(self.table.item(selected_row, 0).text())

        confirm_box = QMessageBox(QMessageBox.Icon.Question,
                                  "Confirm Delete",
                                  "Are you sure you want to delete this record?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  self)
        confirm_box.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: black; font-size: 13px; }
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #0D47A1; }
        """)
        reply = confirm_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_record(record_id)
            self.load_table_data()
            self._show_message(QMessageBox.Icon.Information, "Success", "Record deleted successfully!")

    def update_record(self):
        """Update the selected record in database"""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self._show_message(QMessageBox.Icon.Warning, "No Selection", "Please select a record to update.")
            return

        record_id = int(self.table.item(selected_row, 0).text())
        records = self.db_manager.get_all_records()
        record = next((r for r in records if r['id'] == record_id), None)

        if not record:
            self._show_message(QMessageBox.Icon.Warning, "Error", "Record not found!")
            return

        dialog = UpdateRecordDialog(record, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_record = dialog.get_updated_record()
            self.db_manager.update_record(record_id, updated_record)
            self.load_table_data()
            self._show_message(QMessageBox.Icon.Information, "Success", "Record updated successfully!")

    def go_back(self):
        """Return to main window"""
        self.close()
        self.main_window.show()
