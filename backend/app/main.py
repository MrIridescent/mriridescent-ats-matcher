"""
MRIRIDESCENT ATS RESUME MATCHER - CORE API ENTRY POINT
Developed by David Akpoviroro Oke (MrIridescent)
Digital Polymath & Systems Architect (Coding since Aug 2004)

Architecture:
- Framework: FastAPI (Asynchronous)
- Database: SQLAlchemy ORM (PostgreSQL/SQLite)
- AI Intelligence: Multi-Agent CrewAI + spaCy Semantic Matching
- Frontend: Vanilla JS + Chart.js (Served as Static Files)
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os
import uvicorn
import logging
import time
from backend.app.config import settings
from backend.app.utils.logging_config import setup_logging

# Configure logging
logger = setup_logging()

# Performance Middleware to log request time
class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI(
    title="MrIridescent ATS Resume Matcher API",
    description="RESTful API for AI-powered ATS Resume Matching System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted Host (add more hosts in production)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"] 
)

# Request processing time
app.add_middleware(ProcessTimeMiddleware)

# Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc) if settings.DEBUG else "Something went wrong"},
    )

os.makedirs(os.path.join(settings.UPLOAD_DIR, "jds"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "resumes"), exist_ok=True)
os.makedirs("./data/processed", exist_ok=True)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/css", StaticFiles(directory="frontend/static/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/static/js"), name="js")



@app.get("/", include_in_schema=False)
async def serve_login():
    """Serve login page at root - Frontend entry point"""
    return FileResponse("frontend/templates/login.html")


@app.get("/app", include_in_schema=False)
async def serve_app():
    """Serve main application after login"""
    return FileResponse("frontend/templates/index.html")


@app.get("/login", include_in_schema=False)
async def serve_login_alt():
    """Alternative login URL"""
    return FileResponse("frontend/templates/login.html")



@app.get("/api")
async def api_root():
    """API root - shows API information"""
    return {
        "name": "MrIridescent ATS Resume Matcher API",
        "version": "1.0.0",
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "authentication": "/api/users",
            "job_descriptions": "/api/jd",
            "jd_library": "/api/jd-library",
            "resumes": "/api/resumes",
            "matching": "/api/match",
            "history": "/api/history",
            "interviews": "/api/interviews"
        }
    }


@app.get("/api/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "MrIridescent ATS API",
        "version": "1.0.0"
    }


@app.get("/api/status")
async def api_status():
    """Detailed API status"""
    return {
        "status": "online",
        "database": "connected",
        "api_version": "1.0.0",
        "endpoints_count": 26,
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check_legacy():
    """Legacy health check"""
    return {"status": "healthy"}



@app.on_event("startup")
async def create_tables():
    """Initialize database tables on startup"""
    try:
        from backend.app.models.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")



try:
    from backend.app.api import (
        jd_routes,
        resume_routes,
        matching_routes,
        interview_routes,
        history_routes,
        user_routes,
        jd_library_routes,  
    )

    app.include_router(user_routes.router, tags=["Authentication"])
    app.include_router(jd_routes.router)
    app.include_router(jd_library_routes.router, tags=["JD Library"]) 
    app.include_router(resume_routes.resume_router, prefix='/api/resumes', tags=["Resumes"])
    app.include_router(matching_routes.router, tags=["Matching"])
    app.include_router(history_routes.router, tags=["History"])
    app.include_router(interview_routes.router, tags=["Interviews"])

    print("All API routes loaded successfully!")

except Exception as e:
    print(f"Error loading API routes: {e}")
    import traceback
    traceback.print_exc()


# Global setting for Increasing max upload size to 500MB
app.max_request_size = 500 * 1024 * 1024  # 500 MB



# Main entry point
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 Starting MrIridescent ATS Resume Matcher API...")
    print("=" * 70)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
        limit_max_request_size=500 * 1024 * 1024  # Ensures 500MB limit in Uvicorn too
    )
