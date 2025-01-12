import os
import sys
import webbrowser
from threading import Timer
from app import app, db

def init_db():
    """Initialize the database if it doesn't exist"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'resume_tracker.db')
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open('http://127.0.0.1:5000/')

def run_app():
    """Initialize database and run the application"""
    try:
        # Initialize the database
        init_db()
        
        # Open browser after 1.5 seconds
        Timer(1.5, open_browser).start()
        
        # Run the Flask application
        app.run(port=5000)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    run_app()
