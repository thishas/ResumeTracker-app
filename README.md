# Resume Submission Tracker

A web application to track job application submissions, built with Flask and SQLAlchemy.

## Features

- Track resume submissions with detailed information
- Record recruiter and client details
- Track submission dates, interview dates, and follow-up dates
- Search functionality across all fields
- Easy-to-use web interface
- CSRF protection for secure form submissions
- Responsive design using Bootstrap

## Requirements

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-WTF
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ResumeTracker-app.git
cd ResumeTracker-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python initialize_db.py
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Adding a New Submission
1. Click the "New Submission" button
2. Fill in the required fields:
   - Recruiter Firm
   - Client Name
   - Recruiter Name
   - Recruiter Contact
   - Submission Date
   - Position
   - Job ID
3. Optional fields:
   - Rate
   - Interview Date
   - Follow-up Date
   - Notes
4. Click "Save"

### Editing a Submission
1. Click the pencil icon next to the submission you want to edit
2. Update the desired fields
3. Click "Save"

### Deleting a Submission
1. Click the trash icon next to the submission you want to delete
2. Confirm the deletion

### Searching Submissions
- Type in the search box
- Results update automatically as you type
- Searches across all fields

## Documentation

For more detailed information, see:
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)
- [Testing Guide](docs/testing_guide.md)

## Security Features

- CSRF protection for all forms
- Input validation and sanitization
- Secure date handling
- Error logging and handling

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
