from app import app, db
import os
import sqlite3

def init_db():
    db_path = 'resume_tracker.db'
    
    # Delete existing database if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Verify the table structure
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='resume_submission';")
            schema = cursor.fetchone()
            if schema:
                print("\nCreated table schema:")
                print(schema[0])
            else:
                print("\nError: Table 'resume_submission' was not created!")
                
            cursor.execute("PRAGMA table_info(resume_submission);")
            columns = cursor.fetchall()
            print("\nTable columns:")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
        
        print("\nDatabase initialization completed!")

if __name__ == '__main__':
    init_db()
