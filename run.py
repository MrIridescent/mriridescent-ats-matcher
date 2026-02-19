import uvicorn
import os
import sys
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Adding the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.config import settings

def main():
    # Ensuring data directories exist
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "jds"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "resumes"), exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)
    
    print("Starting MrIridescent ATS Resume Matcher...")
    
    # Checking database type
    if "postgresql" in settings.DATABASE_URL.lower():
        print("Database: PostgreSQL (Production Ready)")
    elif "sqlite" in settings.DATABASE_URL.lower():
        print("Database: SQLite (Development Mode)")
    else:
        print("Database: Unknown")
    
    print(f"Server will be available at: http://localhost:8000")
    
    # Running the application
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()
