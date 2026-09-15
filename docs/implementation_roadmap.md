# Implementation Roadmap

Current state: the portfolio backend is already cleaned up, tested, Dockerized, guarded by demo/webhook secrets, and backed by Alembic migrations. Next work should improve deployability and product completeness without adding framework noise.

## Rules

- Use Ponytail full mode: smallest diff that passes the phase gate.
- Create one branch per phase from updated `main`.
- Commit each phase once unless splitting is needed for a genuinely separate risk.
- Run the listed checks before each commit.
- Merge only after checks pass.

## Done

- `chore/repo-baseline`: structured FastAPI backend baseline.
- `ci/test-suite`: reproducible tests and CI.
- `docs/github-presentation`: public README and demo docs.
- `feat/webhook-security`: Telegram webhook secret and demo API key guard.
- `chore/cloud-deploy`: Docker/cloud deployment notes.
- `feat/database-migrations`: Alembic migration workflow.
- `feat/interview-demo`: deterministic interview demo flow.
- `ci/python-version-matrix`, `ci/fix-clean-container-checks`: CI hardening.

## Phase 1: Production Database Deploy

Branch: `deploy/postgres-runtime`

Goal: make Railway/Render deployment use managed Postgres cleanly.

Scope:

- Add the smallest Postgres driver dependency.
- Run `alembic upgrade head` before Uvicorn in the container start command.
- Keep SQLite as the local default.
- Update deployment docs with one primary target, preferably Railway.

Checks:

```bash
python -m pytest -q
docker build -t kitchen-assistant .
```

Commit:

```bash
git add Dockerfile requirements.txt docs/deployment.md README.md
git commit -m "deploy: support postgres runtime"
```

## Phase 2: Telegram Reply Loop

Branch: `feat/telegram-replies`

Goal: turn webhook updates into real Telegram responses.

Scope:

- Route supported Telegram text commands to existing services.
- Send replies through `app/bot/telegram_client.py`.
- Keep handler logic thin; no business rules in bot code.
- Cover one happy path and one unknown-command path.

Checks:

```bash
python -m pytest -q tests/unit tests/integration/test_security.py
```

Commit:

```bash
git add app tests docs/telegram_flows.md
git commit -m "feat: send telegram command replies"
```

## Phase 3: Receipt Confirmation

Branch: `feat/receipt-confirmation`

Goal: prevent OCR/LLM uncertainty from mutating inventory directly.

Scope:

- Store parsed receipt items as pending confirmation.
- Add accept/reject flow through API or Telegram, whichever is already simpler.
- Validate model output with existing Pydantic schemas before storing.
- Add one integration test proving inventory changes only after confirmation.

Checks:

```bash
python -m pytest -q
```

Commit:

```bash
git add app tests docs/llm_design.md docs/privacy_and_safety.md
git commit -m "feat: require receipt confirmation"
```

## Phase 4: Shopping Lists

Branch: `feat/shopping-list-workflow`

Goal: make shopping lists useful instead of placeholder-only.

Scope:

- Create shopping lists and items.
- Add missing recipe ingredients to a list.
- Keep inventory math in services/rules.
- Add a vertical integration test.

Checks:

```bash
python -m pytest -q
```

Commit:

```bash
git add app tests docs/product_spec.md
git commit -m "feat: add shopping list workflow"
```

## Phase 5: Release Pass

Branch: `release/public-demo`

Goal: make `main` ready to share.

Scope:

- Run final local checks.
- Remove stale private-agent references or mark them historical.
- Confirm README, demo, deployment, and roadmap agree.
- Add no new features.

Checks:

```bash
python -m pytest -q
docker build -t kitchen-assistant-final .
rg -n 'HouseVoice|/Users/g|CLAUDE|OPENAI_API_KEY=.*\S|TELEGRAM_TOKEN=.*\S' README.md docs .env.example
```

Commit:

```bash
git add README.md docs
git commit -m "docs: prepare public demo release"
```

## Branch Loop

```bash
git switch main
git pull --ff-only origin main
git switch -c <phase-branch>
# edit, check, commit
git push -u origin <phase-branch>
```

Skipped: subprojects, milestones, owners, estimates. Add those only when more than one person is actively coordinating.
