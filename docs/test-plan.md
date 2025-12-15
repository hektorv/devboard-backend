# Test Plan — DevBoard Backend

Purpose

This document describes the testing strategy for the DevBoard backend. It defines test types, scope, acceptance criteria, local commands, CI steps, DB strategy, and how to add new tests.

Goals

- Ensure business rules (services) are well covered by unit tests.
- Validate API behavior and contract adherence via integration and contract tests.
- Run tests deterministically and fast in CI and locally.
- Maintain coverage targets: **>= 95% for services**, overall coverage goal **>= 90%** for the backend.

Test types and responsibilities

- Unit tests (fast, isolated):
  - Focus: `app/services/*` and pure functions.
  - Tools: `pytest`.
  - No DB or network calls (use `sqlite` in-memory or mocking for dependencies).

- Integration tests (database + HTTP):
  - Focus: routers, request/response behavior, service + repository integration, DB constraints.
  - Tools: FastAPI `TestClient` or `httpx.AsyncClient`, `pytest`.
  - DB: use local sqlite for fast dev; CI uses MySQL via `docker/docker-compose.test.yml` or the service in GitHub Actions.

- Contract tests (OpenAPI parity):
  - Focus: validate `app` generated OpenAPI (`/openapi.json`) matches `docs/oas.yml` and that responses conform to schemas.
  - Tools: `schemathesis`, `openapi-core` or custom pytest assertions.

- End-to-end tests (future):
  - Focus: full system tests across services and UI (outside current MVP). Setup via separate job or environment.

Test data and DB strategy

- Local dev: prefer SQLite for quick unit/integration tests and iterate fast. Tests that require MySQL should be tagged and run by developers on demand.
- CI: use MySQL service in the workflow (`.github/workflows/ci.yml` or `docker/docker-compose.test.yml`) to validate actual DB behavior.
- Isolation: prefer transactional tests (rollback) or deterministic truncation/fixture teardown between tests.

CI workflow (recommended)

1. Checkout repo.
2. Set up Python and install dependencies (`pip install -r requirements.txt`).
3. Start MySQL service (GitHub Actions service or docker compose) and wait for healthcheck.
4. Run unit tests: `pytest tests/unit`.
5. Run integration tests: `pytest tests/integration` (against MySQL in CI).
6. Run contract test: compare `/openapi.json` produced by the app with `docs/oas.yml` (fail job if mismatched).
7. Run coverage reporting and fail the job if coverage thresholds are not met.

Commands

- Run all tests locally (with project root on PYTHONPATH):

```bash
export PYTHONPATH=$(pwd)
.venv/bin/pytest -q --maxfail=1 --cov=app
```

- Run only unit tests:

```bash
.venv/bin/pytest tests/unit -q
```

- Run only integration tests (fast feedback with sqlite):

```bash
PYTHONPATH=. .venv/bin/pytest tests/integration -q
```

Test organization & naming

- Place unit tests in `tests/unit/` and integration tests in `tests/integration/`.
- Use `test_<module>_<behavior>.py` naming for readability (e.g. `test_project_service_delete_conflict.py`).
- Keep tests hermetic: avoid relying on external services (unless explicitly testing integration with those services).

Adding tests

1. Add unit tests when you implement/modify business logic in a service. Mock external dependencies where appropriate.
2. Add integration tests when you modify routers, DB schema, or add behavioral contracts.
3. When you change the API contract (`docs/oas.yml`), add/adjust a contract test to verify the generated `/openapi.json` matches the spec.

Flaky tests

- Mark flaky tests with `@pytest.mark.flaky` (or a custom marker) and open an issue to fix them ASAP. CI should fail on flaky behavior; temporary skips may be allowed with an embargoed PR documenting the plan to fix.

Coverage and thresholds

- Minimums:
  - Services: 95%
  - Overall repo: 90%
- Use `pytest-cov` to measure and report coverage. Enforce thresholds in CI job as part of the test stage.

Traceability and acceptance criteria

- Each public requirement (docs/project-spec.md RF-*) should have at least one integration test that validates the requirement end-to-end.
- Bugs and regressions must include tests demonstrating the failure before fixing (TDD-friendly workflow).

Maintenance

- Keep tests fast (<5s per unit test, <200ms typical) to encourage frequent runs locally.
- Review and prune outdated tests when behavior changes are intentional.

Appendix — Example mapping (feature -> tests)

| Feature | Unit tests | Integration tests | Contract test |
|---|---:|---:|---:|
| Create Project | ProjectService.create | POST /api/projects returns 201 + correct schema | OpenAPI schema defines ProjectCreate/ProjectOut |
| Delete Project with Tasks | ProjectService.delete raises ConflictError | DELETE /api/projects/{id} returns 409 | n/a |
