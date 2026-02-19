#!/bin/bash
set -e

echo "🔧 Setting up MrIridescent ATS Resume Matcher..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/uploads/jds
mkdir -p data/uploads/resumes
mkdir -p data/processed
mkdir -p logs

# Initialize database
echo "🗄️ Initializing database..."
python init_db.py

echo "✅ Setup complete! Run 'python run.py' to start the application."
