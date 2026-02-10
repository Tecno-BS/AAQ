from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str = "postgresql+asyncpg://user:password@localhost:5432/aaq"
    REDIS_URL : str = "redis://localhost:6379/0"
    ENV: str = "development"
    DEBUG: bool = False
    FILES_STORAGE_PATH: Path = Path("./storage")
    OPENAI_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()