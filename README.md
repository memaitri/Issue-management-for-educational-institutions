# Issue Management for Educational Institutions

A Flask-based web application for managing and tracking issues in educational institutions. This system allows students, faculty, and administrators to report, track, and resolve issues efficiently. Live at https://issue-management-for-educational.onrender.com/

## Features

- **User Authentication**: Role-based login system for students, faculty, and administrators
- **Issue Reporting**: Students can report issues (technical, academic, facility)
- **Issue Tracking**: Track issue status from pending to resolved
- **Faculty Response**: Faculty members can respond to and resolve issues
- **Admin Dashboard**: Administrators can view all issues and manage the system
- **Feedback System**: Users can provide feedback and ratings on issue resolutions

## Roles

- **Student**: Can report issues and view their own issues
- **Faculty**: Can view and respond to issues
- **Admin**: Full system access and management capabilities

## Prerequisites

- Python 3.8+
- Flask 3.0.0
- SQLAlchemy 3.1.1

## Installation

1. Clone the repository:
```bash
git clone https://github.com/memaitri/Issue-management-for-educational-institutions.git
cd Issue-management-for-educational-institutions
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Users

The application creates default users for testing:

| Username | Password | Role |
|----------|----------|------|
| student1 | student123 | Student |
| faculty1 | faculty123 | Faculty |
| admin1 | admin123 | Admin |

**Note**: Change these credentials in production!

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── instance/              # Instance folder for database
├── static/
│   └── style.css         # CSS styling
└── templates/
    ├── index.html        # Home page
    ├── login.html        # Login page
    ├── dashboard.html    # User dashboard
    ├── student_dashboard.html
    ├── faculty_dashboard.html
    ├── admin_dashboard.html
    └── report_issue.html # Issue reporting page
```

## Database Models

### User
- id: Integer (Primary Key)
- username: String (Unique)
- password: String
- role: String (student, faculty, admin)

### Issue
- id: Integer (Primary Key)
- title: String
- description: Text
- type: String (technical, academic, facility)
- status: String (pending, in_progress, resolved)
- faculty_response: Text
- created_at: DateTime

### Feedback
- id: Integer (Primary Key)
- rating: Integer (1-5)
- comment: Text
- submitted_at: DateTime

## Security Notes

⚠️ **Important**: Before deploying to production:
- Change the SECRET_KEY in `app.py`
- Use environment variables for sensitive configuration
- Update default user credentials
- Enable HTTPS
- Configure proper database backups
- Review and harden security settings

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please reach out to the project maintainers.
