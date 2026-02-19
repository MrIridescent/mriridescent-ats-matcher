#!/bin/bash
set -e

echo "🚀 Deploying MrIridescent ATS Resume Matcher..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Load environment variables if .env exists
if [ -f .env ]; then
    echo "📄 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Build and start containers
echo "🏗️ Building and starting Docker containers..."
docker-compose up --build -d

echo "✅ Deployment complete! The application is running in the background."
echo "📝 You can view logs with: docker-compose logs -f"
echo "🌐 Access the application at: http://localhost:8000"
