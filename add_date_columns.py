import sqlite3

def add_date_columns():
    try:
        with sqlite3.connect('resume_tracker.db') as conn:
            cursor = conn.cursor()
            
            # Check if columns exist
            cursor.execute("PRAGMA table_info(resume_submission)")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Add interview_date if it doesn't exist
            if 'interview_date' not in columns:
                print("Adding interview_date column...")
                cursor.execute("ALTER TABLE resume_submission ADD COLUMN interview_date DATETIME")
            
            # Add follow_up_date if it doesn't exist
            if 'follow_up_date' not in columns:
                print("Adding follow_up_date column...")
                cursor.execute("ALTER TABLE resume_submission ADD COLUMN follow_up_date DATETIME")
            
            # Verify the changes
            cursor.execute("PRAGMA table_info(resume_submission)")
            print("\nUpdated columns:")
            for col in cursor.fetchall():
                print(f"- {col[1]} ({col[2]})")
            
            conn.commit()
            print("\nColumns added successfully!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    add_date_columns()
