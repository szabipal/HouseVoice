# Architecture

The backend is layered around FastAPI.

- `api/routes`: HTTP routes and Telegram webhook entry points
- `bot`: Telegram interface layer
- `services`: workflow orchestration
- `db/repositories`: persistence access
- `domain/rules`: deterministic business rules
- `llm`: validated AI interfaces
- `vision`: OCR and image processing interfaces

Handlers and routes should delegate quickly to services. Services should not contain raw SQL.
