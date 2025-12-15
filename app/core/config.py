"""
Application configuration and environment variables
"""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings from environment variables
    """
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/mediConnectPro"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_HOURS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "6"))
    
    # App
    APP_NAME: str = "MediConnectPro API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    class Config:
        env_file = ".env"


settings = Settings()
