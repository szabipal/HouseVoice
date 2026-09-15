# GitHub, Cloud, and Interview Readiness Plan

This plan turns the current local prototype into a clean public project, deployable service, and interview-ready portfolio piece. It covers the requested priority sequence: clean git state and first commit, fix tests and CI, add deployment/repo hygiene, secure webhook and APIs, then add cloud deployment and migrations.

## Execution Rules

- Work one thematic branch at a time.
- Each branch must start from the latest `main`.
- Each branch must end with tests passing before merge.
- Merge into `main` only after the branch goal and acceptance tests pass.
- After each merge, update local `main`, then create the next branch from that updated `main`.
- Do not commit local/private artifacts: `.env`, `venv/`, `data/`, `logs/`, `vaults/`, `.pytest_cache`, `.DS_Store`, `*.bak`.
- If no remote exists, create the GitHub repository first, then add `origin` before the first push.

Recommended branch flow:

```bash
git switch main
git status --short --branch

# If no remote is configured:
git remote add origin <github-repo-url>

# For each phase:
git switch main
git pull --ff-only origin main
git switch -c <branch-name>

# After implementation and passing tests:
git add <intended files only>
git commit -m "<clear commit message>"
git push -u origin <branch-name>

# After review/approval:
git switch main
git merge --ff-only <branch-name>
git push origin main
```

## Phase 1: Repository Hygiene and First Commit

Branch: `chore/repo-baseline`

Goal:

Create a clean, truthful baseline commit that contains the current intended application structure and excludes local runtime/private artifacts.

Scope:

- Resolve the staged/unstaged mismatch between legacy flat modules and the newer structured app.
- Decide whether the current project identity is `Kitchen Household Assistant` or `HouseVoice`, then make docs consistent.
- Remove local-only files from the git index if staged by mistake.
- Keep `.env.example`; exclude `.env`.
- Confirm `.gitignore` covers generated files, secrets, databases, caches, logs, and local vaults.
- Add `.dockerignore` so Docker builds do not include secrets, virtualenvs, caches, logs, databases, or local vault data.
- Remove or rewrite `CLAUDE.md` if it exposes personal/local context or describes the wrong architecture.

Implementation Notes:

- Prefer the newer structured code layout under `app/api`, `app/db`, `app/domain`, `app/services`, `app/llm`, `app/vision`, and `app/bot`.
- Treat `app/db.py` and `app/llm.py` as legacy unless inspection proves they are still required.
- Use `git status --short --branch`, `git diff --cached --name-status`, and `git diff --name-status` before committing.

Tests and Verification:

```bash
git status --short --branch
git ls-files | rg '(^\.env$|^venv/|^data/|^logs/|^vaults/|\.pytest_cache|\.DS_Store|\.bak$)' && exit 1 || true
venv/bin/python -c "from app.main import app; print(app.title)"
venv/bin/python -c "from fastapi.testclient import TestClient; from app.main import app; c=TestClient(app); r=c.get('/health'); assert r.status_code == 200; assert r.json() == {'status': 'ok'}"
```

Acceptance Criteria:

- `git status` shows only intentional files before commit.
- No private/local artifacts are tracked.
- Project name and architecture story are consistent across README and docs.
- The app imports successfully.
- `/health` returns `200`.

Commit:

```bash
git add .gitignore .dockerignore README.md docs app tests Dockerfile docker-compose.yml requirements.txt pytest.ini .env.example
git commit -m "chore: establish clean project baseline"
git push -u origin chore/repo-baseline
```

Merge Gate:

- Merge only if the verification commands pass and the tracked file list is clean.

## Phase 2: Test Environment and CI

Branch: `ci/test-suite`

Goal:

Make the test suite reproducible from a fresh environment and enforce it in GitHub Actions.

Scope:

- Investigate and fix the current `venv/bin/pytest` exit code `139`.
- Create a fresh virtual environment to distinguish local environment corruption from code/test failure.
- Pin dependencies or move to a minimal `pyproject.toml` with explicit runtime and dev dependencies.
- Add GitHub Actions CI for Python 3.11.
- Fix Pydantic v2 config warnings by replacing `orm_mode` with `from_attributes`.
- Ensure unit and integration tests can run with an isolated SQLite database.

Implementation Notes:

- If the segfault disappears in a fresh venv, rebuild local `venv` and document setup.
- If the segfault persists, isolate by running individual test files.
- Keep dependency versions conservative and compatible with the codebase.

Tests and Verification:

```bash
python3.11 -m venv /tmp/telegram-agent-test-venv
/tmp/telegram-agent-test-venv/bin/python -m pip install --upgrade pip
/tmp/telegram-agent-test-venv/bin/python -m pip install -r requirements.txt
/tmp/telegram-agent-test-venv/bin/python -m pytest -q
venv/bin/python -m pytest -q
```

Acceptance Criteria:

- Fresh environment install works from documented files.
- `pytest -q` passes without segfault.
- No Pydantic v2 warning appears during app import/tests.
- GitHub Actions workflow exists and runs tests on push/PR.

Commit:

```bash
git add requirements.txt pytest.ini .github/workflows/ci.yml app tests README.md
git commit -m "ci: add reproducible test suite"
git push -u origin ci/test-suite
```

Merge Gate:

- Local tests pass.
- GitHub Actions passes on the branch.

## Phase 3: GitHub Presentation Polish

Branch: `docs/github-presentation`

Goal:

Make the repository understandable and impressive to a reviewer within five minutes.

Scope:

- Rewrite README as a polished public-facing project page.
- Add a clear feature list, architecture overview, tech stack, setup, test, Docker, and demo flow.
- Add API examples for the main vertical slice.
- Add a small architecture diagram in text or Mermaid.
- Add `LICENSE`.
- Add a short `docs/demo_script.md` for interview walkthroughs.
- Add `docs/engineering_decisions.md` covering privacy-aware inventory, LLM validation boundaries, and layered architecture.
- Clearly mark incomplete features as roadmap, not broken functionality.

Implementation Notes:

- Avoid overselling mocked/deterministic LLM/OCR behavior.
- The strongest demo path is: create user, create household, add shared/private inventory, create recipe, check can-make, log meal, verify inventory deduction.

Tests and Verification:

```bash
python -m pytest -q
python -c "from pathlib import Path; required=['README.md','LICENSE','docs/demo_script.md','docs/engineering_decisions.md']; missing=[p for p in required if not Path(p).exists()]; assert not missing, missing"
rg -n 'HouseVoice|CLAUDE|/Users/g|telegram_agent/venv|OPENAI_API_KEY=.*\\S|TELEGRAM_TOKEN=.*\\S' README.md docs/*.md .env.example -g '!docs/github_cloud_interview_readiness_plan.md' && exit 1 || true
```

Acceptance Criteria:

- README explains what the project is, why it matters, how to run it, and how to demo it.
- Docs are consistent with the current app architecture.
- No personal paths, real secrets, or obsolete project names remain in public docs.
- Tests still pass.

Commit:

```bash
git add README.md LICENSE docs
git commit -m "docs: polish project for public presentation"
git push -u origin docs/github-presentation
```

Merge Gate:

- Tests pass.
- README can be followed from a clean clone.

## Phase 4: Webhook and API Security

Branch: `feat/webhook-security`

Goal:

Prevent unauthenticated public mutation of the Telegram webhook and demo APIs.

Scope:

- Enforce `TELEGRAM_WEBHOOK_SECRET` on `/telegram/webhook`.
- Validate Telegram secret token header, expected as `X-Telegram-Bot-Api-Secret-Token`.
- Return `403` for missing or invalid webhook secrets when a secret is configured.
- Add tests for accepted/rejected webhook requests.
- Decide and implement a minimal demo-safe API authentication strategy for non-Telegram mutation endpoints.
- At minimum, document that the HTTP APIs are demo/internal unless protected behind auth or private networking.

Implementation Notes:

- Keep local development ergonomic: if `TELEGRAM_WEBHOOK_SECRET` is empty, webhook auth may be disabled for local-only use.
- Avoid hardcoding secrets.
- Do not expose `user_id` trust as production-ready auth.

Tests and Verification:

```bash
python -m pytest -q tests/unit tests/integration
python -m pytest -q tests/integration/test_api_vertical_slice.py
python -c "from app.config import get_settings; s=get_settings(); assert hasattr(s, 'telegram_webhook_secret')"
```

Add or update tests to cover:

- Webhook succeeds with correct secret.
- Webhook fails with missing secret when configured.
- Webhook fails with incorrect secret.
- Public mutation route behavior is documented or guarded.

Acceptance Criteria:

- Webhook secret config is actually enforced.
- Security behavior is covered by tests.
- README/deployment docs explain how to set the Telegram webhook secret.
- Tests pass.

Commit:

```bash
git add app tests README.md docs .env.example
git commit -m "feat: secure telegram webhook"
git push -u origin feat/webhook-security
```

Merge Gate:

- Security tests pass.
- Existing vertical slice tests pass.

## Phase 5: Cloud Deployment Readiness

Branch: `chore/cloud-deploy`

Goal:

Make the app deployable to a cloud provider with documented environment variables, health checks, and persistent storage assumptions.

Scope:

- Update Dockerfile for production-readiness.
- Support `PORT` environment variable if targeting platforms like Render/Railway/Fly.
- Add deployment docs for one chosen provider.
- Document required environment variables.
- Add a production database recommendation.
- Add startup command examples.
- Add health check guidance using `/health`.
- Ensure Docker build context excludes local/private files via `.dockerignore`.

Implementation Notes:

- Choose one primary deployment target before implementation, for example Render, Railway, Fly.io, or a VPS.
- SQLite can remain the local default, but cloud docs should recommend Postgres for persistent multi-user deployments.
- If using Postgres, add the required driver dependency.

Tests and Verification:

```bash
docker build -t telegram-agent-readiness .
docker run --rm -p 8000:8000 --env-file .env.example telegram-agent-readiness
```

In a separate terminal or CI step:

```bash
curl -fsS http://127.0.0.1:8000/health
```

Also verify:

```bash
python -m pytest -q
```

Acceptance Criteria:

- Docker image builds successfully.
- Container starts successfully.
- `/health` works from the running container.
- Deployment docs are specific enough to follow.
- Tests pass.

Commit:

```bash
git add Dockerfile docker-compose.yml .dockerignore README.md docs requirements.txt app
git commit -m "chore: prepare cloud deployment"
git push -u origin chore/cloud-deploy
```

Merge Gate:

- Docker build passes.
- Container health check passes.
- Tests pass.

## Phase 6: Database Migrations

Branch: `feat/database-migrations`

Goal:

Replace prototype-only schema creation with a migration workflow suitable for cloud deployment and future schema changes.

Scope:

- Add Alembic.
- Generate initial migration from current SQLAlchemy models.
- Document migration commands.
- Keep local developer setup simple.
- Decide whether app startup still calls `create_all()` in development or whether migrations are required before app startup.

Implementation Notes:

- Prefer explicit migrations for production.
- If keeping `create_all()` for local demos, document that production deploys must run migrations.
- Ensure tests still create isolated in-memory schemas without needing Alembic unless integration tests explicitly cover migrations.

Tests and Verification:

```bash
python -m pytest -q
alembic upgrade head
python -c "from app.main import app; print(app.title)"
```

If using a temporary SQLite database:

```bash
DATABASE_URL=sqlite:////tmp/telegram-agent-migration-test.db alembic upgrade head
DATABASE_URL=sqlite:////tmp/telegram-agent-migration-test.db python -c "from app.db.session import init_database; init_database(); print('ok')"
```

Acceptance Criteria:

- Alembic config exists.
- Initial migration creates the current schema.
- Migration docs exist.
- Tests pass.
- App imports after migrations.

Commit:

```bash
git add alembic.ini alembic app README.md docs requirements.txt tests
git commit -m "feat: add database migrations"
git push -u origin feat/database-migrations
```

Merge Gate:

- Migration from empty database succeeds.
- Tests pass.

## Phase 7: Interview Demo Hardening

Branch: `feat/interview-demo`

Goal:

Create a polished, repeatable demo that showcases backend design, privacy rules, LLM boundaries, tests, and deployment readiness.

Scope:

- Add seed/demo data or a demo script.
- Add a single command or documented sequence to run the vertical slice.
- Add tests for the demo flow.
- Ensure private/shared inventory behavior is visible in the demo.
- Add a short “What I would improve next” section to the README or demo docs.
- Optionally add screenshots of OpenAPI docs or terminal/API output if appropriate.

Implementation Notes:

- Keep demo deterministic.
- Avoid requiring real Telegram/OpenAI credentials for the main demo.
- Real Telegram/OCR can be an optional extended demo.

Tests and Verification:

```bash
python -m pytest -q
python -m pytest -q tests/integration
```

Add or update tests to cover:

- Full API demo path.
- Private item visibility.
- Recipe availability check.
- Meal logging and inventory deduction.

Acceptance Criteria:

- A reviewer can run the demo without real external service credentials.
- The demo highlights the best engineering parts of the project.
- Tests pass.
- README points to the demo.

Commit:

```bash
git add README.md docs tests app
git commit -m "feat: add interview-ready demo flow"
git push -u origin feat/interview-demo
```

Merge Gate:

- Demo instructions work from a clean environment.
- Full test suite passes.

## Final Release Check

Run this on `main` after all branches have merged:

```bash
git switch main
git pull --ff-only origin main
git status --short --branch
python -m pytest -q
docker build -t telegram-agent-final .
docker run --rm -p 8000:8000 --env-file .env.example telegram-agent-final
```

In another terminal:

```bash
curl -fsS http://127.0.0.1:8000/health
```

Final acceptance criteria:

- `main` is clean.
- CI passes.
- Tests pass locally.
- Docker build and health check pass.
- README and docs are public-ready.
- No private files are tracked.
- A cloud deployment path is documented.
- The interview demo can be run without external credentials.

## Later Execution Checklist

Use this checklist at the start of each future execution session:

- Confirm current branch is `main`.
- Confirm working tree is clean or intentionally dirty.
- Confirm latest `main` is pulled from `origin`.
- Create the next branch named in this plan.
- Implement only that branch's scope.
- Run that branch's tests and verification commands.
- Commit with the planned commit message or a clearer equivalent.
- Push the branch.
- Merge only after passing tests.
- Return to updated `main` before starting the next branch.
