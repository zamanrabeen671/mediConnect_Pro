from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database URL (overridable via environment or .env)
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost/medi_connect_pro"

    SECRET_KEY: str = "mysecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 6

    # App
    APP_NAME: str = "MediConnectPro API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Pydantic v2 configuration to load .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
