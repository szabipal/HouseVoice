# Deployment

The simplest cloud target is Render, Railway, or Fly.io using the included Dockerfile.

## Environment

Set these variables in the platform dashboard:

```text
DATABASE_URL=sqlite:///data/kitchen_assistant.db
TELEGRAM_TOKEN=
TELEGRAM_WEBHOOK_SECRET=
OPENAI_API_KEY=
DEMO_API_KEY=
PORT=8000
```

Use strong values for `TELEGRAM_WEBHOOK_SECRET` and `DEMO_API_KEY` before exposing the service.

## Start Command

The Dockerfile runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Health Check

Use:

```text
/health
```

Expected response:

```json
{"status":"ok"}
```

## Database

SQLite is fine for local demos. For a real multi-user deployment, use managed Postgres and run migrations before startup.

Run migrations with:

```bash
alembic upgrade head
```
