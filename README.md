# Kitchen Household Assistant

Production-style Python backend for a Telegram-based household kitchen and grocery assistant.

## Current Scope

This foundation implements a small vertical slice:

- Create users
- Create households
- Add shared or private inventory items
- List inventory visible to a user
- Create recipes
- Check whether a recipe can be made from visible inventory
- Log a cooked recipe and deduct ingredients
- Record inventory transactions for inventory changes

OCR and LLM behavior is currently deterministic and mocked behind clear interfaces.

## Stack

- FastAPI
- SQLAlchemy
- Pydantic
- pytest
- Docker / docker-compose

## Run Locally

```bash
python -m venv venv
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
pytest
```

## Architecture

Telegram handlers are interface-only. Workflows live in services, database access lives in repositories, deterministic logic lives in domain rules, and AI/OCR integrations are isolated behind `app/llm` and `app/vision`.
