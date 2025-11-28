"""
Borrower's Forum Platform - Configuration Management
=====================================================

Framework Applied: security_excellence_framework.md + uncle_bob_platform_frameworks.md
Principle: Centralized configuration with environment-based settings
Why: Makes deployment easy, keeps secrets out of code, follows 12-factor app principles
"""

from pydantic_settings import BaseSettings
from pydantic import validator, Field
from typing import Optional, List
from pathlib import Path
import os


class Settings(BaseSettings):
    """
    Application settings with security best practices.
    
    Framework: Security Excellence Framework
    - All sensitive data comes from environment variables
    - No hardcoded credentials in source code
    - Production safety validations
    
    Framework: Clean Architecture (Uncle Bob)
    - Single source of truth for all configuration
    - Easy to test (can override settings)
    """
    
    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    APP_NAME: str = "Borrower's Forum Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # ============================================
    # API SETTINGS
    # Framework: API Design & Integration Framework
    # ============================================
    API_V1_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS settings for frontend integration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # ============================================
    # DATABASE SETTINGS
    # Framework: Database Design Excellence Framework
    # ============================================
    DATABASE_URL: str = "sqlite:///./database/borrowers_forum.db"
    DATABASE_ECHO: bool = False
    
    # Connection pool settings (for production PostgreSQL)
    DATABASE_POOL_SIZE: int = Field(default=5, ge=1, le=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=10, ge=0, le=50)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=5)
    
    # ============================================
    # SECURITY SETTINGS
    # Framework: Security Excellence Framework
    # CRITICAL: Change SECRET_KEY in production!
    # ============================================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # ============================================
    # DATA COLLECTION SETTINGS
    # Framework: Data Engineering Excellence Framework
    # ============================================
    SCRAPING_DELAY_SECONDS: int = 2
    SCRAPING_TIMEOUT_SECONDS: int = 30
    USER_AGENT: str = "BorrowersForum-Research/1.0"
    
    IMF_API_BASE_URL: str = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
    WORLD_BANK_API_BASE_URL: str = "http://api.worldbank.org/v2"
    PARIS_CLUB_BASE_URL: str = "https://clubdeparis.org"
    
    # ============================================
    # CACHING SETTINGS
    # Framework: Performance & Scalability Framework
    # ============================================
    REDIS_URL: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600
    ENABLE_CACHING: bool = False
    
    # ============================================
    # MONITORING SETTINGS
    # Framework: Monitoring & Observability Framework
    # ============================================
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_FORMAT: str = "json"  # json or text
    LOG_TO_FILE: bool = True
    LOG_TO_CONSOLE: bool = True
    
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = True
    
    # ============================================
    # FILE PATHS
    # Framework: Data Engineering Excellence
    # ============================================
    @property
    def BASE_DIR(self) -> Path:
        """Get base directory of the project."""
        return Path(__file__).resolve().parent.parent.parent
    
    @property
    def DATA_DIR(self) -> Path:
        """Data directory path."""
        return self.BASE_DIR / "data"
    
    @property
    def RAW_DATA_DIR(self) -> Path:
        """Raw data directory path."""
        return self.DATA_DIR / "raw"
    
    @property
    def PROCESSED_DATA_DIR(self) -> Path:
        """Processed data directory path."""
        return self.DATA_DIR / "processed"
    
    @property
    def DATABASE_DIR(self) -> Path:
        """Database directory path."""
        return self.BASE_DIR / "database"
    
    @property
    def LOGS_DIR(self) -> Path:
        """Logs directory path."""
        return self.BASE_DIR / "logs"
    
    @property
    def OUTPUTS_DIR(self) -> Path:
        """Outputs directory path."""
        return self.BASE_DIR / "outputs"
    
    # ============================================
    # EXTERNAL API KEYS
    # Framework: Security Excellence Framework
    # ============================================
    IMF_API_KEY: Optional[str] = None
    WORLD_BANK_API_KEY: Optional[str] = None
    
    # ============================================
    # FEATURE FLAGS
    # ============================================
    ENABLE_ASYNC_UPDATES: bool = True
    ENABLE_RATE_LIMITING: bool = True
    
    # ============================================
    # VALIDATORS (Security & Safety)
    # Framework: Security Excellence + Data Engineering
    # ============================================
    
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v, values):
        """
        Ensure secret key is strong enough in production.
        
        Framework: Security Excellence Framework
        Why: Weak secrets = security vulnerability
        """
        env = values.get('ENVIRONMENT', 'development')
        
        if env == 'production':
            if len(v) < 32:
                raise ValueError(
                    'SECRET_KEY must be at least 32 characters in production. '
                    'Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"'
                )
            if v == 'your-secret-key-change-in-production':
                raise ValueError('Must set actual SECRET_KEY in production')
        
        return v
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v, values):
        """
        Ensure database URL matches environment.
        
        Framework: Database Design Excellence Framework
        Why: SQLite not suitable for production scale
        """
        env = values.get('ENVIRONMENT', 'development')
        
        if env == 'production' and 'sqlite' in v.lower():
            raise ValueError(
                'SQLite not recommended for production. '
                'Use PostgreSQL: postgresql://user:pass@host:5432/dbname'
            )
        
        return v
    
    @validator('CORS_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        """
        Parse CORS origins from string or list.
        
        Framework: API Design & Integration Framework
        Why: Flexible configuration, proper type handling
        """
        if isinstance(v, str):
            # Split comma-separated string from env var
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# ============================================
# SINGLETON PATTERN
# Framework: Uncle Bob's Clean Architecture
# ============================================
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings (singleton pattern).
    
    This ensures we only load configuration once and reuse it,
    following Clean Code principles.
    
    Usage:
        from src.config.settings import get_settings
        settings = get_settings()
        print(settings.DATABASE_URL)
    
    Returns:
        Settings: Application settings object
    """
    global _settings
    
    if _settings is None:
        _settings = Settings()
        
        # Create necessary directories if they don't exist
        # Framework: Data Engineering Excellence - Ensure infrastructure exists
        for directory in [
            _settings.DATA_DIR,
            _settings.RAW_DATA_DIR,
            _settings.PROCESSED_DATA_DIR,
            _settings.DATABASE_DIR,
            _settings.LOGS_DIR,
            _settings.OUTPUTS_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
    
    return _settings


# ============================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# Why: Different settings for dev/staging/production
# ============================================
class DevelopmentSettings(Settings):
    """
    Development environment settings.
    
    Optimized for developer experience:
    - Verbose logging
    - SQL query echoing
    - Debug mode enabled
    """
    DEBUG: bool = True
    DATABASE_ECHO: bool = True
    LOG_LEVEL: str = "DEBUG"


class ProductionSettings(Settings):
    """
    Production environment settings.
    
    Optimized for performance and security:
    - Minimal logging
    - No SQL echoing
    - Debug mode disabled
    - Requires critical environment variables
    """
    DEBUG: bool = False
    DATABASE_ECHO: bool = False
    LOG_LEVEL: str = "WARNING"


def get_settings_for_environment(env: str = "development") -> Settings:
    """
    Get settings for specific environment.
    
    Args:
        env: Environment name (development, production)
    
    Returns:
        Settings: Settings object for the specified environment
    
    Example:
        settings = get_settings_for_environment("production")
    """
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()