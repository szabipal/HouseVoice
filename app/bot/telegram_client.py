import requests

from app.config import get_settings


class TelegramClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token if token is not None else get_settings().telegram_token
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id: int, text: str) -> None:
        if not self.token:
            return
        requests.post(
            f"{self.base_url}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )

    def download_file(self, file_id: str) -> bytes:
        if not self.token:
            raise RuntimeError("TELEGRAM_TOKEN is not configured")

        file_info = requests.get(
            f"{self.base_url}/getFile",
            params={"file_id": file_id},
            timeout=15,
        )
        file_info.raise_for_status()
        file_path = file_info.json()["result"]["file_path"]

        download = requests.get(
            f"https://api.telegram.org/file/bot{self.token}/{file_path}",
            timeout=30,
        )
        download.raise_for_status()
        return download.content
