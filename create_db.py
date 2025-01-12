import sqlite3
import os

def create_database():
    db_path = 'resume_tracker.db'
    
    # Delete existing database if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create new database and table
    print("Creating new database...")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create the resume_submission table
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
        
        # Verify the table structure
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='resume_submission';")
        schema = cursor.fetchone()
        print("\nCreated table schema:")
        print(schema[0])
        
        cursor.execute("PRAGMA table_info(resume_submission);")
        columns = cursor.fetchall()
        print("\nTable columns:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        conn.commit()
        print("\nDatabase creation completed successfully!")

if __name__ == '__main__':
    create_database()
