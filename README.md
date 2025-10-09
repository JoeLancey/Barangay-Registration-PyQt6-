Barangay Registration System
A comprehensive resident registration and management system built with PyQt6 and SQLite for barangay (village) administration in the Philippines.
Overview
The Barangay Registration System is a desktop application designed to streamline resident data management for Philippine barangay offices. It provides an integrated solution for registration, data management, and demographic analysis with an intuitive interface and robust validation mechanisms.
Key Features
Main Dashboard
The landing page provides centralized access to three core modules:

Resident Registration
Administrative Management
Statistical Analysis

Registration Module
Comprehensive data capture organized into logical sections:
Personal Information

Full name (surname, first name, middle name)
Sex, date of birth, and age
Place of birth
Civil status
Nationality

Contact Information

Street address (predefined list of barangay streets)
Contact number with Philippine format validation
Email address

Residency Information

Years of residency in the barangay
Voter's identification number
Household relationship

Emergency Contact

Emergency contact person details
Relationship to resident
Contact number

The registration form includes real-time validation for Philippine mobile numbers, email addresses, and voter ID formats. Required fields are clearly marked, and the system prevents submission of incomplete or invalid data.
Administrative Dashboard
Secure access to resident records with the following capabilities:

View all registered residents in a sortable table format
Search functionality filtering by surname or first name
Update existing records through a dedicated dialog
Delete records with confirmation prompts
Refresh data to reflect latest database state

All 17 data fields are displayed in an organized table view with proper column headers and responsive resizing.
Statistics Module
Visual representation of demographic data including:

Summary cards displaying total population, male count, and female count
Gender distribution pie chart with percentage breakdowns
Age group distribution bar chart covering five categories (0-17, 18-30, 31-45, 46-60, 61+)

Charts are rendered using custom QPainter implementations for precise control over appearance and styling.
Technical Architecture
Technology Stack

Framework: PyQt6 for GUI development
Database: SQLite3 for data persistence
Language: Python


Project Structure
barangay-registration-system

main.py                    # Application entry point and initialization
database_manager.py        # Database operations and CRUD functions
main_window.py             # Main dashboard and navigation
register_window.py         # Registration form interface
admin_dashboard.py         # Administrative panel with table view
statistics_window.py       # Data visualization components
dialogs.py                 # Login and update dialogs
styles.py                  # Centralized stylesheet definitions
barangay_registration.db   # SQLite database (auto-generated)

Database Schema

The system uses a single residents table with the following structure:
sqlCREATE TABLE residents (
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

Validation Rules
Contact Number Validation

Must be exactly 11 digits
Must start with '09' (Philippine mobile format)
Example: 09171234567

Email Validation

Standard RFC-compliant email format
Pattern matching for user@domain.extension structure

Voter ID Validation

Accepts 10-20 digit formats
Allows hyphen separators (e.g., 1234-5678-9012)
Validates numeric content after separator removal

Required Fields
The following fields are mandatory for registration:

Surname
First name
Street address
Contact number

Usage Guide
Registering a New Resident

Select "REGISTER" from the main menu
Complete all required fields marked with asterisks
Optional fields may be left blank if information is unavailable
Click "Add Record" to save the registration
The form automatically clears upon successful submission

Managing Existing Records

Select "ADMIN" from the main menu
Authenticate using admin credentials (default: admin/admin123)
Use the search field to filter records by name
Select a record row to enable management options:

Click "Update Record" to modify information
Click "Delete Record" to remove the entry (requires confirmation)
Click "Refresh Data" to reload the table from the database

Viewing Statistical Data

Select "STATISTICS" from the main menu
Review demographic summary cards at the top
Analyze gender distribution in the pie chart
Examine age group distribution in the bar chart
All visualizations update automatically based on current database state

Error Handling
All user interactions include appropriate error handling:

Input validation with user-friendly error messages
Confirmation dialogs for destructive operations
Graceful handling of database errors
Clear feedback for successful operations

Security Considerations

Administrative functions require password authentication
All user inputs are validated and sanitized before database insertion
SQL injection protection through parameterized queries
Confirmation prompts before record deletion

Known Limitations

Single-user desktop application (no concurrent access)
No built-in backup functionality
Administrative credentials stored in plaintext
No audit trail for record modifications

SCREENSHOTS OF SYSTEM RUNNING
