# Deployment

The simplest cloud target for this repo is Railway using the included Dockerfile and managed Postgres.

Render or Fly.io can also run the same container, but Railway is the primary documented path.

## Environment

Set these variables in the platform dashboard:

```text
DATABASE_URL=<Railway Postgres DATABASE_URL>
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
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
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

SQLite is still the local default. Cloud deployments should use managed Postgres.

The container runs migrations before app startup. To run them manually:

```bash
alembic upgrade head
```

## Railway Steps

1. Create a Railway project from the GitHub repo.
2. Add a Postgres service.
3. Set the app service `DATABASE_URL` to the Postgres `DATABASE_URL`.
4. Set the remaining environment variables listed above.
5. Generate a public domain.
6. Check `/health`.
7. Register the Telegram webhook:

```bash
curl "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" \
  -d "url=https://YOUR_DOMAIN/telegram/webhook" \
  -d "secret_token=$TELEGRAM_WEBHOOK_SECRET"
```
