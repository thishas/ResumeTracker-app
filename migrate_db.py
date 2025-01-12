import sqlite3
import os
import shutil
from datetime import datetime
from app import app, db, ResumeSubmission

def get_table_name(cursor):
    """Get the first table name from the database"""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        return tables[0][0]
    return None

def migrate_database():
    instance_dir = 'instance'
    backup_file = 'resume_tracker.db.backup'
    new_db = os.path.join(instance_dir, 'resume_tracker.db')
    
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} not found")
        return False
    
    print(f"Using backup file: {backup_file}")
    
    try:
        # Connect to the backup database
        old_conn = sqlite3.connect(backup_file)
        old_cursor = old_conn.cursor()
        
        # Get the table name from the old database
        table_name = get_table_name(old_cursor)
        if not table_name:
            print("No tables found in the backup database")
            return False
            
        print(f"Found table: {table_name}")
        
        # Get all data from the old database
        old_cursor.execute(f"SELECT * FROM {table_name}")
        old_data = old_cursor.fetchall()
        
        # Get column names from the old database
        old_cursor.execute(f"PRAGMA table_info({table_name})")
        old_columns = [column[1] for column in old_cursor.fetchall()]
        
        print(f"Found {len(old_data)} records in the backup database")
        print(f"Columns in backup: {', '.join(old_columns)}")
        
        # Create new database connection
        os.makedirs(instance_dir, exist_ok=True)
        
        # Create a temporary database
        temp_db = 'temp_resume_tracker.db'
        if os.path.exists(temp_db):
            os.remove(temp_db)
        
        new_conn = sqlite3.connect(temp_db)
        new_cursor = new_conn.cursor()
        
        # Create new table with updated schema
        new_cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_submission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recruiter_firm TEXT NOT NULL,
            client_name TEXT NOT NULL,
            recruiter_name TEXT NOT NULL,
            recruiter_contact TEXT NOT NULL,
            submission_date DATETIME NOT NULL,
            job_id TEXT NOT NULL,
            position TEXT NOT NULL DEFAULT 'Not Specified',
            rate TEXT,
            notes TEXT,
            interview_date DATE,
            follow_up_date DATE
        )
        """)
        
        # Map old data to new schema
        for row in old_data:
            # Create a dictionary of old column names and values
            old_record = dict(zip(old_columns, row))
            
            # Print the first record for debugging
            if row == old_data[0]:
                print("\nFirst record from backup:")
                for col, val in old_record.items():
                    print(f"{col}: {val}")
            
            # Insert into new database with new schema
            new_cursor.execute("""
            INSERT INTO resume_submission (
                recruiter_firm, client_name, recruiter_name, recruiter_contact,
                submission_date, job_id, position, rate, notes, interview_date, follow_up_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                old_record['recruiter_firm'],
                old_record['client_name'],
                old_record['recruiter_name'],
                old_record['recruiter_contact'],
                old_record['submission_date'],
                old_record['job_id'],
                'Not Specified',  # Default value for new position field
                '',              # Default empty value for new rate field
                old_record.get('notes', ''),
                None,            # Default value for new interview_date field
                None            # Default value for new follow_up_date field
            ))
        
        # Commit changes and close connections
        new_conn.commit()
        print(f"\nSuccessfully migrated {len(old_data)} records to the new database")
        
        # Close connections
        old_conn.close()
        new_conn.close()
        
        # Move the new database to the instance directory
        if os.path.exists(new_db):
            os.remove(new_db)
        shutil.move(temp_db, new_db)
        
        with app.app_context():
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                # Check if interview_date column exists
                result = conn.execute("PRAGMA table_info(resume_submission)")
                columns = [row[1] for row in result.fetchall()]
                
                if 'interview_date' not in columns:
                    conn.execute('ALTER TABLE resume_submission ADD COLUMN interview_date DATE')
                
                if 'follow_up_date' not in columns:
                    conn.execute('ALTER TABLE resume_submission ADD COLUMN follow_up_date DATE')
            
            # Commit the changes
            db.session.commit()
            print("Database migration completed successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    migrate_database()
