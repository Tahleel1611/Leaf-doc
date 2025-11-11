"""Application configuration using pydantic-settings."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App metadata
    APP_NAME: str = "LeafDoc"
    API_PREFIX: str = "/api"
    LOG_LEVEL: str = "INFO"
    
    # Model configuration
    MODEL_PATH: str = "models/leafdoc_mobilev3.ts"
    STORAGE_DIR: str = "storage"
    
    # Database
    DATABASE_URL: str = "sqlite:///./leafdoc.db"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS as a list."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def images_dir(self) -> str:
        """Path to images directory."""
        return f"{self.STORAGE_DIR}/images"
    
    @property
    def heatmaps_dir(self) -> str:
        """Path to heatmaps directory."""
        return f"{self.STORAGE_DIR}/heatmaps"


# Global settings instance
settings = Settings()
