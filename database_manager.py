"""
Database management module for barangay registration system.
Handles all database operations including CRUD operations.
"""
import sqlite3


class DatabaseManager:
    """Handles all database operations"""

    def __init__(self, db_name="barangay_registration.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Create the database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                firstname TEXT NOT NULL,
                middlename TEXT,
                sex TEXT,
                dob TEXT,
                age INTEGER,
                birthplace TEXT,
                civil_status TEXT,
                nationality TEXT,
                street TEXT,
                contact_number TEXT,
                email TEXT,
                years_residency INTEGER,
                voter_id TEXT,
                household_relation TEXT,
                emergency_name TEXT,
                emergency_relation TEXT,
                emergency_contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def add_record(self, record):
        """Insert a new record into the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO residents (
                surname, firstname, middlename, sex, dob, age, birthplace,
                civil_status, nationality, street, contact_number, email,
                years_residency, voter_id, household_relation, emergency_name,
                emergency_relation, emergency_contact
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['surname'], record['firstname'], record['middlename'],
            record['sex'], record['dob'], record['age'], record['birthplace'],
            record['civil_status'], record['nationality'], record['street'],
            record['contact_number'], record['email'], record['years_residency'],
            record['voter_id'], record['household_relation'], record['emergency_name'],
            record['emergency_relation'], record['emergency_contact']
        ))

        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    def get_all_records(self):
        """Retrieve all records from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM residents ORDER BY id DESC')
        rows = cursor.fetchall()

        records = [self._row_to_dict(row) for row in rows]

        conn.close()
        return records

    def update_record(self, record_id, record):
        """Update an existing record"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE residents
            SET surname = ?, firstname = ?, middlename = ?, sex = ?,
                dob = ?, age = ?, birthplace = ?, civil_status = ?,
                nationality = ?, street = ?, contact_number = ?, email = ?,
                years_residency = ?, voter_id = ?, household_relation = ?,
                emergency_name = ?, emergency_relation = ?, emergency_contact = ?
            WHERE id = ?
        ''', (
            record['surname'], record['firstname'], record['middlename'],
            record['sex'], record['dob'], record['age'], record['birthplace'],
            record['civil_status'], record['nationality'], record['street'],
            record['contact_number'], record['email'], record['years_residency'],
            record['voter_id'], record['household_relation'], record['emergency_name'],
            record['emergency_relation'], record['emergency_contact'], record_id
        ))

        conn.commit()
        conn.close()

    def delete_record(self, record_id):
        """Delete a record from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM residents WHERE id = ?', (record_id,))

        conn.commit()
        conn.close()

    def search_records(self, search_term):
        """Search records by surname or firstname only"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        search_pattern = f'%{search_term}%'
        cursor.execute('''
            SELECT * FROM residents
            WHERE surname LIKE ? OR firstname LIKE ?
            ORDER BY id DESC
        ''', (search_pattern, search_pattern))

        rows = cursor.fetchall()
        records = [self._row_to_dict(row) for row in rows]

        conn.close()
        return records

    @staticmethod
    def _row_to_dict(row):
        """Convert database row to dictionary"""
        return {
            'id': row[0],
            'surname': row[1],
            'firstname': row[2],
            'middlename': row[3],
            'sex': row[4],
            'dob': row[5],
            'age': row[6],
            'birthplace': row[7],
            'civil_status': row[8],
            'nationality': row[9],
            'street': row[10],
            'contact_number': row[11],
            'email': row[12],
            'years_residency': row[13],
            'voter_id': row[14],
            'household_relation': row[15],
            'emergency_name': row[16],
            'emergency_relation': row[17],
            'emergency_contact': row[18]
        }