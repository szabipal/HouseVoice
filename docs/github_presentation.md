# GitHub Presentation Checklist

Use this before sharing the repository in applications or interviews.

## Before Making Public

- Rotate any Telegram or OpenAI credentials that were used during local debugging.
- Confirm `.env`, local logs, database files, and scratch notes are not committed.
- Confirm GitHub Actions is green on `main`.
- Check that `README.md` explains the project without requiring private deployment context.

## What Reviewers Should Notice

- Layered FastAPI backend with routes, services, repositories, and domain rules.
- Telegram webhook integration deployed through a public HTTPS service.
- Alembic migrations for SQLite/Postgres-compatible development and deployment.
- Deterministic tests around privacy, inventory transactions, recipe availability, and Telegram handlers.
- OpenAI receipt extraction behind an adapter so external credentials are optional for tests.

## Suggested Application Blurb

Kitchen Household Assistant is a FastAPI and Telegram portfolio project that models shared household inventory, private food visibility, receipt-photo ingestion, recipe availability, and meal logging. It uses SQLAlchemy, Alembic, Docker, Railway/Postgres deployment, GitHub Actions, and an isolated OpenAI vision integration for receipt extraction.
