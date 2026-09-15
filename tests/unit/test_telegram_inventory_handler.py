from app.bot.handlers.inventory_handler import parse_inventory_command
from app.bot.handlers.message_handler import MessageHandler
from app.bot.telegram_client import TelegramClient
from app.domain.enums import Visibility
from app.llm.schemas import ReceiptExtractionResult


class FakeTelegramClient:
    def __init__(self) -> None:
        self.messages: list[tuple[int, str]] = []

    def send_message(self, chat_id: int, text: str) -> None:
        self.messages.append((chat_id, text))


def telegram_update(text: str) -> dict:
    return {
        "message": {
            "chat": {"id": 999},
            "from": {"id": 123, "first_name": "Alex"},
            "text": text,
        }
    }


def telegram_photo_update(file_id: str = "file-123") -> dict:
    return {
        "message": {
            "chat": {"id": 999},
            "from": {"id": 123, "first_name": "Alex"},
            "photo": [{"file_id": file_id, "file_size": 100}],
        }
    }


def test_parse_add_inventory_command():
    command = parse_inventory_command("add milk 1 l private")
    assert command is not None
    assert command.action == "add"
    assert command.name == "milk"
    assert command.quantity == 1
    assert command.unit == "l"
    assert command.visibility == Visibility.PRIVATE


def test_telegram_add_and_show_inventory(session):
    telegram = FakeTelegramClient()
    handler = MessageHandler(session, telegram_client=telegram)

    handler.handle_update(telegram_update("add milk 1 l shared"))
    handler.handle_update(telegram_update("show inventory"))

    assert telegram.messages[0] == (999, "Added milk: 1 l (shared).")
    assert telegram.messages[1][0] == 999
    assert "Visible inventory:" in telegram.messages[1][1]
    assert "milk: 1 l" in telegram.messages[1][1]


def test_telegram_help_describes_supported_commands(session):
    telegram = FakeTelegramClient()
    handler = MessageHandler(session, telegram_client=telegram)

    handler.handle_update(telegram_update("/help"))

    assert telegram.messages[0][0] == 999
    assert "Kitchen assistant commands:" in telegram.messages[0][1]
    assert "add milk 1 l shared" in telegram.messages[0][1]
    assert "show inventory" in telegram.messages[0][1]
    assert "receipt photo" in telegram.messages[0][1]


def test_telegram_receipt_photo_uses_receipt_service(session, monkeypatch):
    telegram = FakeTelegramClient()
    telegram.download_file = lambda file_id: b"receipt-bytes"

    def fake_extract(self, image_bytes):
        assert image_bytes == b"receipt-bytes"
        return ReceiptExtractionResult(items=[
            {"name": "eggs", "quantity": 6, "unit": "piece"},
            {"name": "bread", "quantity": 1, "unit": "piece"},
        ])

    monkeypatch.setattr("app.llm.client.LLMClient.extract_receipt_items_from_image", fake_extract)

    handler = MessageHandler(session, telegram_client=telegram)
    handler.handle_update(telegram_photo_update())
    handler.handle_update(telegram_update("show inventory"))

    assert "Added 2 item(s) from receipt:" in telegram.messages[0][1]
    assert "- eggs" in telegram.messages[0][1]
    assert "eggs: 6 piece" in telegram.messages[1][1]


def test_telegram_client_requires_token():
    client = TelegramClient(token="")
    try:
        client.send_message(999, "hello")
    except RuntimeError as exc:
        assert str(exc) == "TELEGRAM_TOKEN is not configured"
    else:
        raise AssertionError("expected missing token to fail visibly")
