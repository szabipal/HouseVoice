import logging

import requests

from app.config import get_settings

logger = logging.getLogger(__name__)


def _normalize_token(token: str) -> str:
    return token.strip().strip('"').strip("'")


def _token_info(token: str) -> dict[str, object]:
    bot_id, _, secret = token.partition(":")
    return {
        "length": len(token),
        "has_colon": bool(secret),
        "bot_id": bot_id if bot_id.isdigit() else "<invalid>",
        "secret_length": len(secret),
    }


class TelegramClient:
    def __init__(self, token: str | None = None) -> None:
        raw_token = token if token is not None else get_settings().telegram_token
        self.token = _normalize_token(raw_token)
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id: int, text: str) -> None:
        if not self.token:
            raise RuntimeError("TELEGRAM_TOKEN is not configured")
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
        if not response.ok:
            logger.error(
                "Telegram sendMessage failed: status=%s body=%s token_info=%s",
                response.status_code,
                response.text,
                _token_info(self.token),
            )
        response.raise_for_status()

    def download_file(self, file_id: str) -> bytes:
        if not self.token:
            raise RuntimeError("TELEGRAM_TOKEN is not configured")

        file_info = requests.get(
            f"{self.base_url}/getFile",
            params={"file_id": file_id},
            timeout=15,
        )
        if not file_info.ok:
            logger.error(
                "Telegram getFile failed: status=%s body=%s token_info=%s",
                file_info.status_code,
                file_info.text,
                _token_info(self.token),
            )
        file_info.raise_for_status()
        file_path = file_info.json()["result"]["file_path"]

        download = requests.get(
            f"https://api.telegram.org/file/bot{self.token}/{file_path}",
            timeout=30,
        )
        if not download.ok:
            logger.error(
                "Telegram file download failed: status=%s body=%s token_info=%s",
                download.status_code,
                download.text,
                _token_info(self.token),
            )
        download.raise_for_status()
        return download.content
