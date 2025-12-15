# devboard-backend
Backend for DevBoard — backend API for managing Projects and Tasks (MVP). Built with **FastAPI**.

Quickstart for contributors

1. Read the docs:
	- `docs/project-spec.md` — product requirements
	- `docs/backend-architecture-spec.md` — architecture and conventions
	- `docs/oas.yml` — OpenAPI contract (source of truth)

2. Developer setup (local)

Prerequisites
- Python 3.10+ (3.12 recommended)
- pip, virtualenv
- Docker & docker-compose (for running MySQL in tests)

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy environment example and edit as needed:

```bash
cp .env.example .env
# Edit .env and set DB connection values for local dev/test if necessary
```

3. Running the app (development)

Start the app locally with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# API docs: http://127.0.0.1:8000/docs
```

4. Tests

Unit tests do not require Docker. Integration tests use MySQL defined in `docker/docker-compose.test.yml`.

Start the test DB (MySQL) in detached mode:

```bash
docker compose -f docker/docker-compose.test.yml up -d
# wait until MySQL is ready
```

Run the full test suite with coverage:

```bash
PYTHONPATH="$(pwd)" .venv/bin/pytest -q --maxfail=1 --cov=app
```

Run a single test file (example):

```bash
PYTHONPATH="$(pwd)" .venv/bin/pytest tests/unit/test_logging_decorator.py -q
```

Tip: `scripts/test.sh` contains a helper wrapper used in CI; you can inspect or reuse it.

5. Observability & logging

- Service-level decorator: `app/utils/logging_decorator.py` provides `@service_log` to log entry/exit/errors for service methods; logs to `service_logger`.
- Structured logging and request correlation are recommended for production (see `docs/backend-architecture-spec.md`).

6. Contributing

Please follow `CONTRIBUTING.md` for PR workflow and commit conventions. The OpenAPI spec (`docs/oas.yml`) is the canonical API contract — propose API changes there first and add contract tests.

If you use an AI assistant to author code or tests, follow `.github/copilot-instructions.md` for repo-specific guidance.

## Logging & observability 🔧

- A lightweight service-level logging decorator is available at `app/utils/logging_decorator.py` as `service_log`.
- Apply `@service_log` to public service methods to automatically log entry, exit and exceptions. Logs are emitted to the `service_logger` logger.
- The decorator preserves function metadata (name, docstring). If you need to redact or truncate large arguments, configure your logging or request an enhancement.

## Tests ✅

- Run the full test suite with coverage:

```bash
PYTHONPATH="$(pwd)" .venv/bin/pytest -q --maxfail=1 --cov=app
```

- Unit tests for the logging decorator are in `tests/unit/test_logging_decorator.py` and assert entry/exit/exception logging behavior.
