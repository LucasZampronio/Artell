from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "Artell"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Groq Configuration
    GROQ_API_KEY: str
    GROQ_IMAGE_API_KEY: str
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017/artell"
    MONGODB_DB_NAME: str = "artell"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Groq Model Configuration
    GROQ_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    GROQ_MAX_TOKENS: int = 1000
    GROQ_TEMPERATURE: float = 0.7

    GROQ_VISION_MODEL: str = '"meta-llama/llama-4-maverick-17b-128e-instruct"'
    GROQ_VISION_MAX_TOKENS: int = 1000
    GROQ_VISION_TEMPERATURE: float = 0.7


    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()
