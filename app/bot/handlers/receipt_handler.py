from sqlalchemy.orm import Session

from app.bot.telegram_client import TelegramClient
from app.services.receipt_service import ReceiptService


class ReceiptHandler:
    def __init__(self, session: Session, telegram_client: TelegramClient | None = None) -> None:
        self.session = session
        self.telegram = telegram_client or TelegramClient()

    def handle(self, message: dict, household_id: int, user_id: int) -> str:
        photos = message.get("photo") or []
        if not photos:
            return "Could not find a receipt photo in that message."

        best = max(photos, key=lambda photo: photo.get("file_size", 0))
        file_id = best.get("file_id")
        if not file_id:
            return "Could not read the receipt photo."

        image_bytes = self.telegram.download_file(file_id)
        items = ReceiptService(self.session).ingest_receipt_image(household_id, user_id, image_bytes)
        if not items:
            return "No grocery items were found in that receipt."

        names = [item.name for item in items[:10]]
        extra = len(items) - len(names)
        lines = [f"Added {len(items)} item(s) from receipt:"]
        lines.extend(f"- {name}" for name in names)
        if extra:
            lines.append(f"...and {extra} more")
        return "\n".join(lines)
