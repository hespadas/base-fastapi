from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_URL: str = "daily"
    # DB_HOST: str = "localhost"
    # DB_PORT: int = 5432
    # DB_NAME: str = "mydatabase"
    # DB_USER: str
