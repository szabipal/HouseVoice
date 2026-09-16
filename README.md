# Kitchen Household Assistant

A FastAPI backend for a Telegram-based kitchen assistant. It tracks household inventory, private versus shared food, receipt-photo ingestion, recipe availability, and meal logging.

This is a portfolio prototype built to show production-minded backend work: layered architecture, deterministic domain rules, migrations, tests, container deployment, webhook integration, and an isolated OpenAI vision boundary.

## What It Demonstrates

- **API design:** FastAPI routes for users, households, inventory, recipes, shopping lists, health checks, and Telegram webhooks.
- **Domain modeling:** household membership, item visibility, recipe availability, meal logging, and inventory transactions.
- **Privacy rules:** shared items are visible to household members; private items stay visible only to the owner.
- **Telegram integration:** webhook updates are handled through a thin interface layer and dispatched to services.
- **AI integration:** receipt photo extraction can use OpenAI vision when `OPENAI_API_KEY` is configured, while tests remain deterministic without external credentials.
- **Deployment readiness:** Docker image, Railway/Postgres deployment notes, Alembic migrations, and GitHub Actions CI.

## Current Telegram Commands

```text
/help
add milk 1 l shared
add chocolate 1 piece private
show inventory
```

Users can also send a receipt photo. Detected grocery items are added as shared inventory.

Recipe commands are scaffolded but not fully wired through Telegram yet; the recipe workflow is available through the HTTP API.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- pytest
- Docker
- PostgreSQL on Railway, SQLite for local default development
- OpenAI API behind an adapter for receipt extraction

## Architecture

```text
Telegram / HTTP
  -> FastAPI routes
  -> Telegram handlers
  -> services
  -> repositories
  -> SQLAlchemy models
  -> SQLite locally / PostgreSQL in deployment
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

The local default database is SQLite at `data/kitchen_assistant.db`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Cloud deployment notes are in [docs/deployment.md](docs/deployment.md).

## Tests

```bash
python -m pytest -q
```

## Demo Flow

The core interview demo is documented in [docs/demo_script.md](docs/demo_script.md). It walks through user creation, household setup, private/shared inventory, recipe checks, meal logging, and Telegram commands.

## Configuration

```text
DATABASE_URL=sqlite:///data/kitchen_assistant.db
TELEGRAM_TOKEN=
TELEGRAM_WEBHOOK_SECRET=
OPENAI_API_KEY=
DEMO_API_KEY=
```

`TELEGRAM_TOKEN` and `OPENAI_API_KEY` are optional for the local API demo. They are only needed for real Telegram and OpenAI integrations.
Set `TELEGRAM_WEBHOOK_SECRET` and `DEMO_API_KEY` before exposing the app publicly.

## Deployment

Deployment notes are in [docs/deployment.md](docs/deployment.md). The expected cloud setup is a FastAPI service on Railway with managed Postgres and a Telegram webhook registered to:

```text
https://YOUR_DOMAIN/telegram/webhook
```

## Status

This is a portfolio prototype, not a polished consumer product. It is intended to demonstrate backend engineering judgment, integration work, and testable service boundaries.
