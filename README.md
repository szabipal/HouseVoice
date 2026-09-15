# Kitchen Household Assistant

FastAPI backend for a Telegram-based kitchen assistant that helps a household track inventory, recipes, receipt ingestion, and private versus shared food visibility.

## Why It Exists

Kitchen inventory is messy because items are shared, personal, expiring, and often entered from receipts. This project models those workflows as a small production-style backend with clear service boundaries and deterministic tests.

## Features

- Create users and households
- Add shared or private inventory items
- List only the inventory visible to a user
- Create recipes with ingredients
- Check whether a recipe can be cooked from visible inventory
- Log a meal and deduct used ingredients
- Record inventory transactions for auditability
- Receive Telegram webhook updates through an interface layer
- Keep OCR/LLM behavior behind validated interfaces

OCR and LLM behavior is deterministic by default so the core backend can be tested without external credentials.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- pytest
- Docker

## Architecture

```text
Telegram / HTTP
  -> FastAPI routes
  -> Telegram handlers
  -> services
  -> repositories
  -> SQLAlchemy models
  -> SQLite locally
```

Business rules live in `app/domain/rules`. Services orchestrate workflows. Repositories own database access. LLM and OCR integrations live behind `app/llm` and `app/vision`.

## Run Locally

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Tests

```bash
python -m pytest -q
```

## Demo Flow

The core interview demo is documented in [docs/demo_script.md](docs/demo_script.md). It walks through user creation, household setup, private/shared inventory, recipe checks, and meal logging.

## Configuration

```text
DATABASE_URL=sqlite:///data/kitchen_assistant.db
TELEGRAM_TOKEN=
TELEGRAM_WEBHOOK_SECRET=
OPENAI_API_KEY=
```

`TELEGRAM_TOKEN` and `OPENAI_API_KEY` are optional for the local API demo. They are only needed for real Telegram and OpenAI integrations.

## Status

This is a portfolio backend, not a hosted production service yet. Next steps are webhook security, deployment docs, and database migrations.
