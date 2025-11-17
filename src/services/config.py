"""
Configuration service for managing application settings.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Application settings
    APP_NAME: str = "CV Analysis API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cv_analysis.db"
    )
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
    
    # File upload settings
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default
    ALLOWED_FILE_EXTENSIONS: list = os.getenv(
        "ALLOWED_FILE_EXTENSIONS",
        "pdf,doc,docx"
    ).split(",")
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Create global settings instance
settings = Settings()


class ConfigService:
    """Service for accessing configuration"""
    
    @staticmethod
    def get_settings() -> Settings:
        """Get application settings"""
        return settings
    
    @staticmethod
    def get_database_url() -> str:
        """Get database URL"""
        return settings.DATABASE_URL
    
    @staticmethod
    def get_secret_key() -> str:
        """Get secret key for JWT tokens"""
        return settings.SECRET_KEY
    
    @staticmethod
    def is_debug() -> bool:
        """Check if application is in debug mode"""
        return settings.DEBUG
    
    @staticmethod
    def get_cors_origins() -> list:
        """Get CORS allowed origins"""
        return settings.CORS_ORIGINS
    
    @staticmethod
    def get_max_upload_size() -> int:
        """Get maximum file upload size in bytes"""
        return settings.MAX_UPLOAD_SIZE
    
    @staticmethod
    def get_allowed_file_extensions() -> list:
        """Get allowed file extensions for uploads"""
        return settings.ALLOWED_FILE_EXTENSIONS

