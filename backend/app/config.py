import json
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict, Any

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:sum12345@localhost:5432/mriridescent_ats_resume_matcher"
    
    # Ollama Configuration
    USE_OLLAMA: bool = True
    OLLAMA_BASE_URL: str = "https://indoor-boom-stick-determination.trycloudflare.com/"
    OLLAMA_MODEL: str = "gemma3:27b"
    OLLAMA_TIMEOUT: int = 300
    
    # API Keys
    PERPLEXITY_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Settings
    DEBUG: bool = False
    UPLOAD_DIR: str = "./data/uploads"
    MAX_FILE_SIZE: int = 10485760  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "doc", "docx"]
    
    # AI Logic
    USE_AGENTIC_AI: bool = False
    USE_GROQ: bool = False
    USE_PERPLEXITY: bool = True
    PERPLEXITY_MODEL: str = "sonar-pro"

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Default Users (JSON string in .env)
    DEFAULT_USERS: str = "[]"

    @property
    def parsed_default_users(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.DEFAULT_USERS)
        except:
            return []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()



# Validation on startup
if settings.USE_OLLAMA:
    print("\n" + "="*60)
    print("🤖 OLLAMA INFERENCE MODE ENABLED")
    print("="*60)
    print(f"   Endpoint: {settings.OLLAMA_BASE_URL}")
    print(f"   Model: {settings.OLLAMA_MODEL}")
    print(f"   Timeout: {settings.OLLAMA_TIMEOUT}s")
    print("="*60 + "\n")
else:
    print("⚠️ WARNING: Ollama is disabled in config!")