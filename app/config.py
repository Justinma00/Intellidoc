import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:  # Fallback for environments without pydantic-settings
    from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./intellidoc.db"
    redis_url: str = "redis://localhost:6379"
    huggingface_api_key: Optional[str] = None
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    upload_dir: str = "./uploads"
    chroma_persist_dir: str = "./chroma_db"
    
    class Config:
        env_file = ".env"

settings = Settings()