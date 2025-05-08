"""
Configuration settings for the FastAPI application.
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Template API"
    DEBUG: bool = bool(os.getenv("DEBUG", "False") == "True")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 