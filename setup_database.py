from app import app, db, ResumeSubmission
import sqlite3
import os
import time

def setup_database():
    db_path = 'resume_tracker.db'
    temp_db = 'temp_resume_tracker.db'
    
    # Backup existing data if database exists
    if os.path.exists(db_path):
        print("Backing up existing data...")
        backup_data = []
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM resume_submission")
                backup_data = cursor.fetchall()
                cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='resume_submission'")
                old_columns = [col[1] for col in cursor.execute("PRAGMA table_info(resume_submission)").fetchall()]
                print(f"Backed up {len(backup_data)} records")
        except:
            print("No existing data to backup or error reading data")
    
    print("\nCreating new database with updated schema...")
    # Create new database with temporary name
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        
        # Create the table with all required columns
        cursor.execute('''
        CREATE TABLE resume_submission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recruiter_firm TEXT NOT NULL,
            client_name TEXT NOT NULL,
            recruiter_name TEXT NOT NULL,
            recruiter_contact TEXT NOT NULL,
            submission_date DATETIME NOT NULL,
            job_id TEXT NOT NULL,
            position TEXT NOT NULL DEFAULT 'Not Specified',
            rate TEXT,
            interview_date DATETIME,
            follow_up_date DATETIME,
            notes TEXT
        )
        ''')
        
        # Verify the schema
        cursor.execute("PRAGMA table_info(resume_submission)")
        columns = cursor.fetchall()
        print("\nVerified table columns:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        # Restore backed up data if exists
        if backup_data:
            print("\nRestoring backed up data...")
            # Map old data to new schema
            for record in backup_data:
                # Create a dict of old data
                old_record = dict(zip(old_columns, record))
                
                # Insert with new schema
                cursor.execute('''
                INSERT INTO resume_submission (
                    recruiter_firm, client_name, recruiter_name, recruiter_contact,
                    submission_date, job_id, position, rate, notes,
                    interview_date, follow_up_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)
                ''', (
                    old_record.get('recruiter_firm', ''),
                    old_record.get('client_name', ''),
                    old_record.get('recruiter_name', ''),
                    old_record.get('recruiter_contact', ''),
                    old_record.get('submission_date', ''),
                    old_record.get('job_id', ''),
                    old_record.get('position', 'Not Specified'),
                    old_record.get('rate', ''),
                    old_record.get('notes', '')
                ))
            
            print(f"Restored {len(backup_data)} records")
        
        conn.commit()
    
    # Try to replace the old database with the new one
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
            os.rename(temp_db, db_path)
            print("\nDatabase setup completed successfully!")
            break
        except Exception as e:
            attempt += 1
            if attempt == max_attempts:
                print(f"\nError: Could not replace database after {max_attempts} attempts.")
                print("Please ensure no other processes are using the database and try again.")
                return
            print(f"\nAttempt {attempt}: Could not replace database, waiting 2 seconds...")
            time.sleep(2)

if __name__ == '__main__':
    with app.app_context():
        setup_database()
