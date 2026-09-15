from fastapi import Header, HTTPException

from app.config import get_settings


def require_demo_api_key(x_api_key: str = Header(default="")) -> None:
    expected = get_settings().demo_api_key
    if expected and x_api_key != expected:
        raise HTTPException(status_code=403, detail="Invalid API key")


def require_telegram_secret(x_telegram_bot_api_secret_token: str = Header(default="")) -> None:
    expected = get_settings().telegram_webhook_secret
    if expected and x_telegram_bot_api_secret_token != expected:
        raise HTTPException(status_code=403, detail="Invalid Telegram webhook secret")
