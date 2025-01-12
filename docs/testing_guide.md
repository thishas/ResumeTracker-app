# Resume Submission Tracker - Testing Guide

## Overview

This guide covers testing procedures for the Resume Submission Tracker application. It includes unit tests, integration tests, and end-to-end testing procedures.

## Test Environment Setup

1. Create a test virtual environment:
```bash
python -m venv test-venv
source test-venv/bin/activate  # On Windows: test-venv\Scripts\activate
```

2. Install test dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

3. Set up test database:
```bash
python initialize_db.py --test
```

## Running Tests

### Unit Tests

Run all unit tests:
```bash
python -m pytest tests/unit/
```

Run specific test file:
```bash
python -m pytest tests/unit/test_database.py
```

### Integration Tests

Run all integration tests:
```bash
python -m pytest tests/integration/
```

### Coverage Report

Generate coverage report:
```bash
python -m pytest --cov=app tests/
```

## Test Categories

### Database Tests

- Table creation and schema
- CRUD operations
- Data validation
- Error handling
- Transaction management

### API Endpoint Tests

- Route responses
- Data validation
- Error handling
- CSRF protection
- HTTP methods

### Form Tests

- Field validation
- Required fields
- Optional fields
- Date formatting
- Error messages

### Frontend Tests

- Form submission
- Modal behavior
- Event handlers
- AJAX requests
- UI updates

## Manual Testing Procedures

### Form Testing

1. New Submission
   - All required fields
   - Optional fields
   - Invalid data
   - Empty fields
   - Special characters

2. Edit Submission
   - Load existing data
   - Update fields
   - Cancel edit
   - Save changes

3. Delete Submission
   - Confirmation dialog
   - Successful deletion
   - Table update

### Search Testing

1. Search Functionality
   - Partial matches
   - Case sensitivity
   - Special characters
   - Empty search
   - Multiple terms

2. Results Display
   - Correct filtering
   - Update speed
   - Clear results

### Date Field Testing

1. Submission Date
   - Required field
   - Date format
   - Invalid dates
   - Past dates

2. Interview Date
   - Optional field
   - Clear field
   - Future dates
   - Invalid formats

3. Follow-up Date
   - Optional field
   - Clear field
   - Future dates
   - Invalid formats

### Error Handling

1. Form Errors
   - Missing required fields
   - Invalid formats
   - Error messages
   - Form recovery

2. Server Errors
   - Database connection
   - CSRF token
   - Invalid requests
   - Error pages

### Browser Testing

Test on major browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Test Data

### Sample Test Data

```python
test_submission = {
    'recruiter_firm': 'Test Firm',
    'client_name': 'Test Client',
    'recruiter_name': 'John Doe',
    'recruiter_contact': 'john@test.com',
    'submission_date': '2025-01-01',
    'position': 'Software Engineer',
    'job_id': 'TEST123',
    'rate': '$100/hr',
    'notes': 'Test notes',
    'interview_date': '2025-01-15',
    'follow_up_date': '2025-01-20'
}
```

### Edge Cases

1. Text Fields
   - Maximum length
   - Special characters
   - HTML tags
   - SQL injection attempts

2. Date Fields
   - Invalid formats
   - Future dates
   - Past dates
   - Empty values

3. Contact Information
   - Various email formats
   - Phone numbers
   - URLs
   - International formats

## Continuous Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          python -m pytest --cov=app tests/
```

## Performance Testing

### Load Testing

1. Setup
   - Install locust
   - Configure test scenarios
   - Set up monitoring

2. Test Scenarios
   - Concurrent users
   - Form submissions
   - Search operations
   - Database operations

### Response Time Testing

Monitor:
- Page load time
- Form submission
- Search response
- AJAX requests

## Security Testing

1. CSRF Protection
   - Token validation
   - Token expiration
   - Form submission

2. Input Validation
   - SQL injection
   - XSS attacks
   - Invalid data
   - Special characters

3. Error Handling
   - Stack traces
   - Error messages
   - Log files

## Reporting Issues

When reporting bugs:
1. Describe the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details
6. Screenshots if applicable

## Test Documentation

Maintain documentation for:
1. Test cases
2. Test results
3. Bug reports
4. Test coverage
5. Performance metrics

## Best Practices

1. Write clear test names
2. Use descriptive assertions
3. Clean up test data
4. Mock external services
5. Keep tests independent
6. Regular test maintenance
