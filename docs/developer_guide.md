# Resume Tracker - Developer Guide

## Development Environment Setup

### Prerequisites
1. Python 3.8 or higher
2. Git (for version control)
3. Visual Studio Code (recommended) or your preferred IDE

### Initial Setup
1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture

The application follows a modern web application architecture:

- **Backend**: Flask (Python)
- **Frontend**: JavaScript (ES6+), Bootstrap 5
- **Database**: SQLite with SQLAlchemy ORM
- **Template Engine**: Jinja2

## Key Components

### Backend (app.py)

- RESTful API endpoints for CRUD operations
- CSRF protection using Flask-WTF
- Database models and migrations
- Error handling and validation
- JSON response formatting

### Frontend (main.js)

- Modern JavaScript with async/await
- Event-driven architecture
- Real-time DOM updates
- Form handling and validation
- Modal dialog management
- Accessibility features

### Database

- SQLite database with SQLAlchemy ORM
- Models for submissions and related data
- Automatic schema migrations
- Data validation and constraints

## API Endpoints

### GET Endpoints

- `/` - Main application page
- `/submissions` - Get all submissions
- `/get_csrf_token` - Get CSRF token for form submissions

### POST Endpoints

- `/add` - Add new submission
- `/edit/<id>` - Edit existing submission
- `/delete/<id>` - Delete submission

## Frontend Architecture

### Modal Dialog Implementation

```javascript
// Modal state management
function handleModalState(modalElement, isOpen) {
    if (!modalElement) return;
    
    if (isOpen) {
        modalElement.removeAttribute('inert');
    } else {
        modalElement.setAttribute('inert', '');
        // Remove lingering focus
        const focusedElements = modalElement.querySelectorAll('button, input, textarea, select, a');
        focusedElements.forEach(element => {
            element.blur();
        });
    }
}
```

### Form Submission

```javascript
async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const token = getCookie('csrf_token');
    
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': token },
        body: formData,
        credentials: 'same-origin'
    });
}
```

## Accessibility Implementation

### Modal Dialog

- Uses `inert` attribute for proper focus management
- ARIA labels for all interactive elements
- Keyboard navigation support
- Focus trap in modal
- Screen reader announcements

### Form Controls

- Proper label associations
- Error message announcements
- Required field indicators
- Focus management
- Keyboard navigation

## Error Handling

### Backend

- Proper HTTP status codes
- Detailed error messages
- Validation error handling
- Database error handling
- CSRF token validation

### Frontend

- Form validation
- API error handling
- User feedback
- Network error handling
- State management errors

## Testing

### Unit Tests

- Backend API endpoints
- Database operations
- Form validation
- Error handling

### Integration Tests

- End-to-end workflows
- Form submissions
- Modal interactions
- Search functionality

### Accessibility Tests

- Screen reader compatibility
- Keyboard navigation
- Focus management
- ARIA implementation

## Security Measures

- CSRF protection
- Input validation
- SQL injection prevention
- XSS prevention
- Secure modal implementation

## Future Improvements

1. **Authentication & Authorization**
   - User accounts
   - Role-based access
   - Session management

2. **Enhanced Features**
   - File attachments
   - Email notifications
   - Status tracking
   - Analytics dashboard

3. **Technical Improvements**
   - TypeScript migration
   - Test coverage increase
   - Performance optimization
   - API documentation

4. **UI/UX Enhancements**
   - Dark mode
   - Mobile optimization
   - Customizable themes
   - Keyboard shortcuts

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
python -m pytest
```

4. Start development server:
```bash
flask run --debug
```

## Coding Standards

- PEP 8 for Python code
- ESLint for JavaScript
- Prettier for formatting
- JSDoc for documentation

## Version Control

- Feature branches
- Semantic versioning
- Descriptive commit messages
- Pull request reviews

## Documentation

- Keep this guide updated
- Document all API endpoints
- Update user guide
- Maintain changelog

## Database Schema

```python
class ResumeSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_firm = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    recruiter_name = db.Column(db.String(100), nullable=False)
    recruiter_contact = db.Column(db.String(200), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_id = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False, default='Not Specified')
    rate = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
```

## Troubleshooting

### Database Issues
```bash
# Reset database
python migrate_db.py --reset

# Backup database
python migrate_db.py --backup

# Restore database
python migrate_db.py --restore
```

### Common Issues
- Port conflicts: Change port in `flask run`
- Database locked: Restart application
- Missing dependencies: Check requirements.txt

## Project Structure
```
ResumeTracker-app/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/            # Static assets
│   ├── css/          # CSS styles
│   └── js/           # JavaScript files
├── templates/         # HTML templates
├── tests/            # Test files
└── docs/             # Documentation
```

## API Documentation

### Endpoints
- `GET /` - Main page
- `POST /add` - Add new submission
- `POST /update/<id>` - Update submission
- `POST /delete/<id>` - Delete submission
- `GET /search` - Search submissions

## Architecture Overview

The Resume Submission Tracker is built using:
- Backend: Flask (Python web framework)
- Database: SQLite with SQLAlchemy ORM
- Frontend: HTML5, Bootstrap 5, and JavaScript
- Security: Flask-WTF for CSRF protection

### Directory Structure

```
ResumeTracker-app/
├── app.py                 # Main Flask application
├── initialize_db.py       # Database initialization
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # Frontend JavaScript
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main application page
│   └── error.html        # Error page
├── docs/                 # Documentation
└── tests/               # Test files
```

## Backend Components

### Database Schema

The main table `resume_submission` has the following structure:

```python
class ResumeSubmission(db.Model):
    __tablename__ = 'resume_submission'

    id = db.Column(db.Integer, primary_key=True)
    recruiter_firm = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    recruiter_name = db.Column(db.String(100), nullable=False)
    recruiter_contact = db.Column(db.String(200), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False)
    job_id = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    follow_up_date = db.Column(db.DateTime, nullable=True)
```

### API Endpoints

#### GET Routes
- `/` - Main application page
- `/search` - Search submissions
- `/get_csrf_token` - Get CSRF token for forms

#### POST Routes
- `/add` - Add new submission
- `/edit/<int:id>` - Edit existing submission
- `/delete/<int:id>` - Delete submission

### Error Handling

The application implements comprehensive error handling:
- Form validation errors
- Database errors
- CSRF token errors
- General HTTP errors

## Frontend Components

### JavaScript Architecture

The `main.js` file contains several key functions:

```javascript
// CSRF token handling
getCsrfToken()
postWithCsrf(url, formData)

// Form handling
handleFormSubmit(event)
populateEditForm(button)

// Table management
refreshTable()
attachEventListeners()

// Delete functionality
handleDelete(id)

// Contact formatting
formatContactInfo(contact)
```

### Event Handling

Event listeners are attached to:
- Form submission
- Edit buttons
- Delete buttons
- Search input
- Modal events

### Modal Management

The submission modal handles both new submissions and edits:
- Form reset on close
- Proper data population for edits
- Validation feedback
- Error handling

## Security Implementation

### CSRF Protection

- Flask-WTF CSRF tokens
- Token refresh mechanism
- Secure token transmission
- Token validation on all POST requests

### Input Validation

- Server-side validation
- Client-side validation
- SQL injection prevention
- XSS protection

### Error Handling

- Graceful error recovery
- User-friendly error messages
- Detailed server logs
- Transaction rollback on errors

## Development Setup

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python initialize_db.py
```

5. Run development server:
```bash
python app.py
```

## Testing

### Running Tests

```bash
python -m pytest tests/
```

### Test Coverage

Tests cover:
- Database operations
- Form validation
- API endpoints
- Error handling
- CSRF protection

## Deployment

### Production Setup

1. Set secure SECRET_KEY
2. Configure production database
3. Set up logging
4. Configure WSGI server
5. Set up reverse proxy

### Environment Variables

Required environment variables:
- `FLASK_ENV`
- `SECRET_KEY`
- `DATABASE_URL`

## Contributing

### Code Style

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Follow Bootstrap conventions for HTML/CSS

### Pull Request Process

1. Create feature branch
2. Write tests
3. Update documentation
4. Submit PR with description

### Version Control

- Use semantic versioning
- Keep clean commit history
- Write descriptive commit messages

## Maintenance

### Database Maintenance

- Regular backups
- Schema migrations
- Data cleanup
- Performance optimization

### Logging

- Application errors
- User actions
- Performance metrics
- Security events

### Monitoring

- Server health
- Database performance
- Error rates
- User activity

## Troubleshooting

### Common Issues

1. Database connection errors
   - Check connection string
   - Verify database exists
   - Check permissions

2. CSRF token errors
   - Clear browser cache
   - Check token expiration
   - Verify token transmission

3. Form submission issues
   - Validate input data
   - Check CSRF token
   - Verify database constraints

### Debug Tools

- Flask debug mode
- Browser developer tools
- Database client
- Log analysis tools

## Future Enhancements

Planned features:
- Email notifications
- File attachments
- Advanced search filters
- Data export
- API authentication
- Batch operations
