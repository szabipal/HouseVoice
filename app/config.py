from functools import lru_cache
import os
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _database_url_from_env() -> str:
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{Path('data/kitchen_assistant.db')}")
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""

    app_name: str
    database_url: str
    telegram_token: str
    telegram_webhook_secret: str
    openai_api_key: str
    demo_api_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Kitchen Household Assistant"),
        database_url=_database_url_from_env(),
        telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
        telegram_webhook_secret=os.getenv("TELEGRAM_WEBHOOK_SECRET", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        demo_api_key=os.getenv("DEMO_API_KEY", ""),
    )
