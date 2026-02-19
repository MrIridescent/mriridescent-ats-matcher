import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    banner = """
    ============================================================
       MRIRIDESCENT ATS MATCHER - TURNKEY SETUP WIZARD
       Creator: David Akpoviroro Oke (MrIridescent)
    ============================================================
    """
    print(banner)

def check_python():
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 10):
        print("❌ Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected.")

def install_dependencies():
    print("📦 Installing dependencies (this may take a minute)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully.")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def download_spacy_model():
    print("🧠 Downloading spaCy NLP model (en_core_web_md)...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_md"])
        print("✅ spaCy model downloaded.")
    except Exception as e:
        print(f"⚠️ Warning: Could not download en_core_web_md. Falling back to en_core_web_sm if available.")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

def create_env_file():
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating default .env file...")
        default_content = """# DATABASE CONFIG
DATABASE_URL=sqlite:///./ats_matcher.db
SECRET_KEY=renaissance_man_secret_2026
DEBUG=True

# AI BACKEND CONFIG
PERPLEXITY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
USE_AGENTIC_AI=true
USE_OLLAMA=false

# DIRECTORIES
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=104857600

# DEFAULT USER (Turnkey Setup)
DEFAULT_USERS='[{"username": "admin", "password": "AdminPassword123", "email": "admin@mriridescent.ai", "full_name": "MrIridescent Administrator", "role": "admin"}]'
"""
        with open(env_path, "w") as f:
            f.write(default_content)
        print("✅ .env created. PLEASE UPDATE IT WITH YOUR API KEYS.")
    else:
        print("✅ .env file already exists.")

def init_db():
    print("🗄️ Initializing database...")
    try:
        # Check if init_db.py exists
        if Path("init_db.py").exists():
            subprocess.check_call([sys.executable, "init_db.py"])
            print("✅ Database initialized with default tables and users.")
        else:
            print("⚠️ init_db.py not found. Skipping DB seeding.")
    except Exception as e:
        print(f"❌ DB Initialization failed: {e}")

def main():
    print_banner()
    check_python()
    
    # Create data directories
    print("📁 Creating necessary directories...")
    os.makedirs("./data/uploads/jds", exist_ok=True)
    os.makedirs("./data/uploads/resumes", exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)
    
    install_dependencies()
    download_spacy_model()
    create_env_file()
    init_db()
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("============================================================")
    print("To start the system:")
    print("1. Update .env with your API keys (if not using local Ollama).")
    print(f"2. Run: python run.py")
    print("============================================================")

if __name__ == "__main__":
    main()
