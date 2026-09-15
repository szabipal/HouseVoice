from sqlalchemy.orm import Session

from app.bot.handlers.inventory_handler import InventoryHandler
from app.bot.telegram_client import TelegramClient
from app.services.household_service import HouseholdService


class MessageHandler:
    """Telegram interface layer. Business workflows live in services."""

    def __init__(self, session: Session, telegram_client: TelegramClient | None = None) -> None:
        self.session = session
        self.telegram = telegram_client or TelegramClient()

    def handle_update(self, update: dict) -> None:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        sender = message.get("from", {})
        telegram_id = sender.get("id")

        if not chat_id or not telegram_id:
            return

        text = message.get("text", "")

        display_name = sender.get("first_name") or sender.get("username") or "Telegram user"
        household_service = HouseholdService(self.session)
        user = household_service.get_or_create_telegram_user(telegram_id, display_name)
        household = household_service.get_or_create_default_household(user.id)

        if message.get("photo"):
            from app.bot.handlers.receipt_handler import ReceiptHandler

            try:
                response = ReceiptHandler(self.session, self.telegram).handle(message, household.id, user.id)
            except Exception as exc:
                response = f"Could not process that receipt: {exc}"
            self.telegram.send_message(chat_id, response)
            return

        if not text:
            return

        inventory_response = InventoryHandler(self.session).handle(text, household.id, user.id)
        if inventory_response:
            self.telegram.send_message(chat_id, inventory_response)
            return

        if text.startswith("/recipe"):
            from app.bot.handlers.recipe_handler import RecipeHandler

            RecipeHandler(self.session).handle(message)
            self.telegram.send_message(chat_id, "Recipe commands are scaffolded but not wired yet.")
            return

        self.telegram.send_message(
            chat_id,
            "Try: add milk 1 l shared, add chocolate 1 piece private, or show inventory.",
        )
