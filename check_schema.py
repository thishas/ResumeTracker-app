import sqlite3

def check_schema():
    with sqlite3.connect('resume_tracker.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='resume_submission';")
        print("Table Schema:")
        print(cursor.fetchone()[0])
        
        cursor.execute("PRAGMA table_info(resume_submission);")
        print("\nColumns:")
        for col in cursor.fetchall():
            print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, DefaultVal: {col[4]}")

if __name__ == '__main__':
    check_schema()
