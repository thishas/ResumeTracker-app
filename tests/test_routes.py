import pytest
from app import app, db, ResumeSubmission
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index_route(client):
    """Test the main page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_submission(client):
    """Test adding a new submission"""
    data = {
        'recruiter_firm': 'Test Firm',
        'client_name': 'Test Client',
        'recruiter_name': 'John Doe',
        'recruiter_contact': 'john@example.com',
        'job_id': 'JOB123',
        'submission_date': '2025-01-09',
        'notes': 'Test notes'
    }
    response = client.post('/add', data=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_search_submissions(client):
    """Test search functionality"""
    # Add a test submission
    submission = ResumeSubmission(
        recruiter_firm='Test Firm',
        client_name='Test Client',
        recruiter_name='John Doe',
        recruiter_contact='john@example.com',
        job_id='JOB123',
        submission_date=datetime.now(),
        notes='Test notes'
    )
    with app.app_context():
        db.session.add(submission)
        db.session.commit()

    # Test search
    response = client.get('/search?query=Test')
    assert response.status_code == 200
    data = response.json
    assert len(data) > 0
    assert data[0]['recruiter_firm'] == 'Test Firm'
