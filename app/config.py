from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # This configures Pydantic to look for a .env file automatically
    # Pydantic Settings will look for a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
