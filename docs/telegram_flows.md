# Telegram Flows

Telegram is an interface layer.

Expected flow:

1. Telegram sends webhook update.
2. `telegram_webhook` route passes the update to a handler.
3. Handler chooses the relevant service.
4. Service performs workflow and returns a result.
5. Telegram client sends the response.

Handlers must not contain business logic.
