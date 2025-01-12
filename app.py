from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os
import sqlite3
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

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

    def to_dict(self):
        return {
            'id': self.id,
            'recruiter_firm': self.recruiter_firm,
            'client_name': self.client_name,
            'recruiter_name': self.recruiter_name,
            'recruiter_contact': self.recruiter_contact,
            'submission_date': self.submission_date.strftime('%Y-%m-%d') if self.submission_date else None,
            'position': self.position,
            'rate': self.rate,
            'job_id': self.job_id,
            'notes': self.notes,
            'interview_date': self.interview_date.strftime('%Y-%m-%d') if self.interview_date else None,
            'follow_up_date': self.follow_up_date.strftime('%Y-%m-%d') if self.follow_up_date else None
        }

def ensure_database():
    try:
        db_path = 'resume_tracker.db'
        if not os.path.exists(db_path):
            logger.info("Database does not exist. Creating...")
            with app.app_context():
                db.create_all()
                logger.info("Database created successfully")
        else:
            logger.info("Database exists. Verifying schema...")
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(resume_submission)")
                columns = [col[1] for col in cursor.fetchall()]
                logger.info(f"Current columns: {columns}")
                
                if 'interview_date' not in columns:
                    logger.info("Adding interview_date column...")
                    cursor.execute("ALTER TABLE resume_submission ADD COLUMN interview_date DATETIME")
                if 'follow_up_date' not in columns:
                    logger.info("Adding follow_up_date column...")
                    cursor.execute("ALTER TABLE resume_submission ADD COLUMN follow_up_date DATETIME")
                
                conn.commit()
                logger.info("Database schema verified and updated if needed")
    except Exception as e:
        logger.error(f"Error in ensure_database: {str(e)}\n{traceback.format_exc()}")
        raise

# Ensure database is properly set up
with app.app_context():
    ensure_database()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-CSRF-Token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Expose-Headers', 'X-CSRF-Token')
    return response

@app.route('/')
def index():
    try:
        logger.info("Loading index page...")
        submissions = ResumeSubmission.query.order_by(ResumeSubmission.submission_date.desc()).all()
        logger.info(f"Found {len(submissions)} submissions")
        return render_template('index.html', submissions=submissions)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}\n{traceback.format_exc()}")
        return render_template('error.html', error=str(e)), 500

@app.route('/add', methods=['POST'])
def add_submission():
    try:
        if not request.form:
            raise ValueError("No form data received")
            
        required_fields = ['recruiter_firm', 'client_name', 'recruiter_name', 'recruiter_contact', 
                          'submission_date', 'position', 'job_id']
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
        data = request.form
        
        # Parse dates, allowing them to be optional
        try:
            submission_date = datetime.strptime(data['submission_date'], '%Y-%m-%d')
        except (KeyError, ValueError):
            raise ValueError("Invalid submission date format")
            
        interview_date = None
        if data.get('interview_date'):
            try:
                interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid interview date format")
                
        follow_up_date = None
        if data.get('follow_up_date'):
            try:
                follow_up_date = datetime.strptime(data['follow_up_date'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid follow-up date format")
        
        submission = ResumeSubmission(
            recruiter_firm=data['recruiter_firm'],
            client_name=data['client_name'],
            recruiter_name=data['recruiter_name'],
            recruiter_contact=data['recruiter_contact'],
            submission_date=submission_date,
            position=data['position'],
            rate=data['rate'],
            job_id=data['job_id'],
            interview_date=interview_date,
            follow_up_date=follow_up_date,
            notes=data.get('notes', '')
        )
        db.session.add(submission)
        db.session.commit()
        logger.info(f"Added new submission: {submission.to_dict()}")
        return jsonify({'status': 'success', 'data': submission.to_dict()})
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Error adding submission: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to add submission. Please try again.'}), 500

@app.route('/edit/<int:id>', methods=['POST'])
def edit_submission(id):
    try:
        if not request.form:
            raise ValueError("No form data received")
            
        required_fields = ['recruiter_firm', 'client_name', 'recruiter_name', 'recruiter_contact', 
                          'submission_date', 'position', 'job_id']
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
        submission = ResumeSubmission.query.get_or_404(id)
        data = request.form
        
        # Parse dates, allowing them to be optional
        try:
            submission_date = datetime.strptime(data['submission_date'], '%Y-%m-%d')
        except (KeyError, ValueError):
            raise ValueError("Invalid submission date format")
            
        interview_date = None
        if data.get('interview_date'):
            try:
                interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid interview date format")
                
        follow_up_date = None
        if data.get('follow_up_date'):
            try:
                follow_up_date = datetime.strptime(data['follow_up_date'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid follow-up date format")
        
        submission.recruiter_firm = data['recruiter_firm']
        submission.client_name = data['client_name']
        submission.recruiter_name = data['recruiter_name']
        submission.recruiter_contact = data['recruiter_contact']
        submission.submission_date = submission_date
        submission.position = data['position']
        submission.rate = data['rate']
        submission.job_id = data['job_id']
        submission.interview_date = interview_date
        submission.follow_up_date = follow_up_date
        submission.notes = data.get('notes', '')
        
        db.session.commit()
        logger.info(f"Updated submission {id}: {submission.to_dict()}")
        return jsonify({'status': 'success', 'data': submission.to_dict()})
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Error editing submission: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to update submission. Please try again.'}), 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete_submission(id):
    try:
        submission = ResumeSubmission.query.get_or_404(id)
        db.session.delete(submission)
        db.session.commit()
        logger.info(f"Deleted submission with id {id}")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error deleting submission: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to delete submission. Please try again.'}), 500

@app.route('/search')
def search():
    try:
        query = request.args.get('query', '').lower()
        submissions = ResumeSubmission.query.filter(
            db.or_(
                ResumeSubmission.recruiter_firm.ilike(f'%{query}%'),
                ResumeSubmission.client_name.ilike(f'%{query}%'),
                ResumeSubmission.recruiter_name.ilike(f'%{query}%'),
                ResumeSubmission.recruiter_contact.ilike(f'%{query}%'),
                ResumeSubmission.job_id.ilike(f'%{query}%'),
                ResumeSubmission.position.ilike(f'%{query}%'),
                ResumeSubmission.rate.ilike(f'%{query}%')
            )
        ).order_by(ResumeSubmission.submission_date.desc()).all()
        logger.info(f"Found {len(submissions)} submissions matching query '{query}'")
        return jsonify([submission.to_dict() for submission in submissions])
    except Exception as e:
        logger.error(f"Error searching submissions: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': 'Failed to search submissions. Please try again.'}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        logger.info(f"Serving static file: {filename}")
        return send_from_directory('static', filename)
    except Exception as e:
        logger.error(f"Error serving static file: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 404

@app.route('/get_csrf_token')
def get_csrf_token():
    try:
        token = generate_csrf()
        logger.info("Generated new CSRF token")
        response = jsonify({'csrf_token': token})
        response.headers.set('X-CSRF-Token', token)
        return response
    except Exception as e:
        logger.error(f"Error generating CSRF token: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
