import sqlite3

def check_database():
    try:
        with sqlite3.connect('resume_tracker.db') as conn:
            cursor = conn.cursor()
            
            # Check table structure
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='resume_submission'")
            schema = cursor.fetchone()
            if schema:
                print("Current table schema:")
                print(schema[0])
            else:
                print("Table 'resume_submission' not found!")
                
            # List columns
            cursor.execute("PRAGMA table_info(resume_submission)")
            columns = cursor.fetchall()
            print("\nCurrent columns:")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_database()
