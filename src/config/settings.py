from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "PDF Extractext"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "pdf_extractext"
    MONGODB_TIMEOUT: int = 5000
    
    # API
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"]
    
    # File handling
    MAX_FILE_SIZE_MB: int = 100
    UPLOAD_DIR: str = "./uploads"
    
    # Feature flags (for future expansion)
    ENABLE_AUTH: bool = False
    ENABLE_RATE_LIMITING: bool = False

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_value(cls, value):
        """Support common environment aliases for debug mode."""
        if isinstance(value, str):
            normalized_value = value.strip().lower()
            if normalized_value in {"debug", "dev", "development", "true", "1", "yes", "on"}:
                return True
            if normalized_value in {"release", "prod", "production", "false", "0", "no", "off"}:
                return False
        return value

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings instance (singleton pattern)."""
    return Settings()
