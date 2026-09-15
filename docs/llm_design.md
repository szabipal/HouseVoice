# LLM Design

LLM behavior is isolated under `app/llm`.

Planned responsibilities:

- Receipt item extraction
- Recipe parsing
- Telegram command interpretation
- Food photo estimation

Every model output must pass through Pydantic validation before services use it.
Uncertain AI actions should create confirmation prompts rather than direct inventory mutations.
