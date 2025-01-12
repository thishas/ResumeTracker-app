import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ResumeSubmission(db.Model):
    __tablename__ = 'resume_submission'

    id = db.Column(db.Integer, primary_key=True)
    recruiter_firm = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    recruiter_name = db.Column(db.String(100), nullable=False)
    recruiter_contact = db.Column(db.String(200), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False)
    job_id = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False, default='Not Specified')
    rate = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    follow_up_date = db.Column(db.DateTime, nullable=True)

def initialize_database():
    # Remove existing database if it exists
    if os.path.exists('resume_tracker.db'):
        os.remove('resume_tracker.db')
        print("Removed existing database")
    
    # Create all tables
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create tables fresh
        db.create_all()
        print("Created new database with tables")
        
        # Add sample data
        sample_data = [
            ResumeSubmission(
                recruiter_firm='Example Corp',
                client_name='Client A',
                recruiter_name='John Recruiter',
                recruiter_contact='john@example.com',
                submission_date=datetime.now(),
                job_id='JOB123',
                position='Software Engineer',
                rate='$50/hr',
                notes='Initial submission',
                interview_date=None,
                follow_up_date=None
            ),
            ResumeSubmission(
                recruiter_firm='Tech Staffing',
                client_name='Client B',
                recruiter_name='Jane Agent',
                recruiter_contact='jane@techstaffing.com',
                submission_date=datetime.now(),
                job_id='JOB456',
                position='Full Stack Developer',
                rate='$60/hr',
                notes='Follow up next week',
                interview_date=None,
                follow_up_date=None
            )
        ]
        
        # Add sample submissions to database
        for submission in sample_data:
            db.session.add(submission)
        
        try:
            # Commit changes
            db.session.commit()
            print("Added sample data")
            
            # Verify table structure
            print("\nVerifying database structure:")
            inspector = db.inspect(db.engine)
            for table_name in inspector.get_table_names():
                print(f"\nTable: {table_name}")
                for column in inspector.get_columns(table_name):
                    print(f"- {column['name']}: {column['type']}")
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    initialize_database()
