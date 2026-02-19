# MrIridescent ATS Resume Matcher

## Development Commands
- **Run Locally**: `python run.py`
- **Initialize DB**: `python init_db.py` or `./scripts/setup.sh`
- **Database Migrations**: `alembic upgrade head`
- **Run Tests**: `pytest`
- **Linting**: `flake8 backend/app`

## Production Deployment
- **Full Deployment**: `./scripts/deploy.sh`
- **Docker Build**: `docker-compose build`
- **Docker Run**: `docker-compose up -d`
- **View Logs**: `docker-compose logs -f`
- **Stop Containers**: `docker-compose down`

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL / SQLAlchemy
- **AI/ML**: spaCy, CrewAI, LangChain, Perplexity/Groq
- **Frontend**: HTML/JS/CSS (Vanilla)
- **Containerization**: Docker / Docker Compose
- **Migrations**: Alembic

## Key Directories
- `backend/app`: Core application logic
- `frontend/templates`: HTML templates
- `frontend/static`: JS/CSS assets
- `scripts`: Deployment and setup utilities
- `alembic`: Database migration files
- `data`: Uploaded and processed data
