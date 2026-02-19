---
description: Repository Information Overview
alwaysApply: true
---

# SentientGeeks ATS Resume Matcher Information

## Summary
An AI-powered Applicant Tracking System (ATS) that matches resumes against job descriptions, ranks candidates based on skills and experience, and provides structured insights for recruiters. It features JD processing, skill weightage, bulk resume upload, AI parsing, and interview question generation.

## Structure
- **backend/**: FastAPI application containing API routes, models, services (PDF/JD/Resume processing), and utilities.
- **frontend/**: Web interface built with Vanilla JavaScript, HTML, and CSS.
- **tests/**: Test suite for JD/Resume processing, matching logic, and agentic AI services.
- **data/**: Storage for uploaded JDs, resumes, and processed results.
- **.zencoder/ / .zenflow/**: Automation workflows.

## Language & Runtime
**Language**: Python 3.x, JavaScript (Frontend)  
**Framework**: FastAPI (Backend)  
**Database**: PostgreSQL (Production), SQLite (Development)  
**AI/ML**: spaCy, scikit-learn, LangChain, CrewAI, Perplexity Pro API, Groq API (Agentic)

## Dependencies
**Main Dependencies**:
- `fastapi`, `uvicorn`, `sqlalchemy`, `alembic` (Backend Framework)
- `pandas`, `numpy`, `scikit-learn` (Data Science)
- `spacy`, `PyMuPDF` (NLP & PDF Processing)
- `crewai`, `langchain`, `pydantic` (AI/Agentic Frameworks)
- `psycopg2-binary`, `asyncpg` (Database Drivers)

**Development Dependencies**:
- `python-dotenv`, `pytest` (likely used for testing though not explicitly in requirements.txt)

## Build & Installation
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database (creates tables and default users)
python init_db.py

# 4. Run the application
python run.py
```

## Main Files & Resources
- **backend/app/main.py**: FastAPI entry point and API route configuration.
- **run.py**: Main startup script for the local development server.
- **init_db.py**: Script to initialize database tables and seed initial users.
- **create_jd_library_tables.py**: Utility for JD library setup.
- **frontend/templates/login.html**: Frontend entry point (login page).
- **frontend/static/js/**: Core frontend logic (matcher.js, jd-processor.js, etc.).

## Testing
**Framework**: Python `unittest` style or `pytest` (inferred from file structure)
**Test Location**: `tests/` directory
**Naming Convention**: `test_*.py`
**Run Command**:
```bash
# Run specific test files
python tests/test_agentic.py
python tests/test_matching.py
```
