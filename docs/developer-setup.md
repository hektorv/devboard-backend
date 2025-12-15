# Developer setup & quickstart

This document describes the minimal steps to get a local development environment running so you can start implementing features and running tests.

Prerequisites

- Linux / macOS / Windows Subsystem for Linux
- Docker & Docker Compose (for running a local MySQL instance for tests)
- Python 3.11+ (or the project's target Python version)

1) Clone the repo

```bash
git clone git@github.com:hektorv/devboard-backend.git
cd devboard-backend
```

2) Create and activate virtualenv

```bash
python -m venv .venv
source .venv/bin/activate
```

3) Install dependencies (temporary instructions until `requirements.txt` exists)

When dependencies are added to `requirements.txt` you can use:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present yet, install minimally required tools for development:

```bash
pip install fastapi uvicorn[standard] SQLAlchemy PyMySQL pytest pytest-cov alembic
```

4) Environment variables

Copy `.env.example` to `.env` and edit values as needed (DB host/port, credentials).

5) Start a local MySQL for tests (recommended)

```bash
docker compose -f docker/docker-compose.test.yml up -d
```

6) Run tests

```bash
# run all tests
pytest -q --maxfail=1 --cov=app

# run a single test file
pytest tests/unit/test_project_service.py -q
```

7) Run the app locally (development)

With FastAPI you can run the app using Uvicorn:

```bash
# assuming your app entrypoint is `app.main:app`
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI will expose interactive docs at `http://127.0.0.1:8000/docs` (Swagger) and `http://127.0.0.1:8000/redoc` (ReDoc).

8) Helpful tips

- Keep the OpenAPI spec `docs/oas.yml` as the single source of truth for endpoints; when using FastAPI, validate generated OpenAPI (`/openapi.json`) against `docs/oas.yml` in CI.
- Use `pytest -k <pattern>` to run focused tests while developing.
- Use the Test DB docker compose file above to run an isolated MySQL instance per CI job or locally.

If anything is missing from this guide or you want a `Makefile`/helper scripts added, open an issue and I'll add it.
