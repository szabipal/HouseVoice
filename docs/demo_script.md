# Demo Script

This script is designed for a short portfolio walkthrough. It shows the API surface first, then the Telegram interface.

Run the app:

```bash
uvicorn app.main:app --reload
```

Create a user:

```bash
curl -s -X POST http://127.0.0.1:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"display_name":"Alex","telegram_id":1001}'
```

Create a household:

```bash
curl -s -X POST http://127.0.0.1:8000/households \
  -H 'Content-Type: application/json' \
  -d '{"name":"Home","owner_user_id":1}'
```

Add shared inventory:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/inventory \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"pasta","quantity":500,"unit":"g","visibility":"shared"}'
```

Add private inventory:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/inventory \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"chocolate","quantity":1,"unit":"piece","visibility":"private"}'
```

Create a recipe:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/recipes \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"name":"Pasta","servings":2,"ingredients":[{"name":"pasta","quantity":200,"unit":"g"}]}'
```

Check if it can be cooked:

```bash
curl -s 'http://127.0.0.1:8000/households/1/recipes/1/can-make?user_id=1'
```

Log the meal:

```bash
curl -s -X POST http://127.0.0.1:8000/households/1/recipes/1/meal-logs \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"recipe_id":1,"servings":2,"notes":"demo"}'
```

List inventory:

```bash
curl -s 'http://127.0.0.1:8000/households/1/inventory?user_id=1'
```

## Telegram Demo

With a deployed service and Telegram webhook configured, send these messages to the bot:

```text
/help
add milk 1 l shared
add chocolate 1 piece private
show inventory
```

Then send a receipt photo. If `OPENAI_API_KEY` is configured, the receipt image is sent through the OpenAI-backed receipt extraction path. Without a key, the app uses deterministic fallback behavior so the rest of the workflow can still be tested.

## What To Point Out

- Routes are thin and delegate to services.
- Services use repositories rather than embedding persistence logic in handlers.
- Inventory visibility is enforced in the domain/service layer.
- Telegram is an interface on top of the same backend workflows, not a separate application.
- External AI behavior is isolated behind `app/llm/client.py` and validated before it mutates inventory.
