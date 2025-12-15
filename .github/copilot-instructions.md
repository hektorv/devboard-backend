# Copilot / AI agent instructions for `devboard-backend`

Short, actionable guidance for AI coding assistants working on this repository.

Core purpose

- Backend API (**FastAPI/Python**) for managing Projects and Tasks. OpenAPI is the single source of truth (`docs/oas.yml`).

High-level architecture (what matters)

- Layers: routers (FastAPI `APIRouter`), services (business rules), repositories (DB/ORM), models (SQLAlchemy), schemas (Pydantic DTOs). Follow separation strictly: do not put business logic in routers or decorators.
- Data model: Projects -> Tasks (1:N), Users exist for assignment only (no auth in MVP).
- Persist to MySQL. Tests should run against MySQL in Docker.

Conventions and expectations

- Language: code, docstrings and comments in **English**.
- Tests: TDD mindset. Use `pytest`; unit tests for services; integration tests for API (use FastAPI `TestClient` or `httpx` for async endpoints). Aim for high coverage (95%+ for service layer).
- Error responses must follow the shape: `{ error_code, message, details?, trace_id? }` and use canonical codes (e.g., `VALIDATION_ERROR`, `NOT_FOUND`, `CONFLICT_PROJECT_HAS_TASKS`). Map domain exceptions to this shape using FastAPI exception handlers.
- State machine defaults:
  - TaskStatus: BACKLOG -> IN_PROGRESS -> DONE (revert DONE -> IN_PROGRESS allowed by default)
  - ProjectStatus: ACTIVE <-> ON_HOLD -> ARCHIVED (ARCHIVED is terminal/read-only)
- Deletion policy: default to **soft delete** (add `deleted_at`), and `DELETE` should return 409 when deleting a project that still has tasks unless a special hard-delete is requested and approved.

FastAPI-specific notes

- Use **Pydantic** models for request and response validation. Keep Pydantic schemas (DTOs) separate from SQLAlchemy models.
- Use `APIRouter` and dependency injection (`Depends`) to inject service instances and DB sessions into route handlers.
- FastAPI automatically generates OpenAPI at `/openapi.json` and interactive docs at `/docs` (Swagger) and `/redoc` (ReDoc). Keep `docs/oas.yml` as the canonical spec and add CI checks to validate generated spec against it.
- For errors, raise `HTTPException` or define custom exception handlers to return the standardized error payload.

Developer workflow (for AI to follow when editing code)

1. If API changes are required, update `docs/oas.yml` first (contract-first policy), add/modify contract tests, and include the `docs/oas.yml` changes in the PR. Use FastAPI's generated `/openapi.json` to validate parity in CI.
2. Implement changes in services/repositories/models; keep routers thin. Use Pydantic for payloads and response models; avoid returning ORM objects directly from route handlers.
3. Add/modify unit and integration tests to cover behavior and edge cases. For API tests use FastAPI `TestClient` or `httpx.AsyncClient` for async routes.
4. Update `docs/backend-architecture-spec.md` or `docs/project-spec.md` if altering business rules.
5. Run tests locally using `docker/docker-compose.test.yml` for MySQL and `pytest`.

Helpful file references

- Architecture: `docs/backend-architecture-spec.md`
- Product requirements: `docs/project-spec.md`
- Developer quickstart: `docs/developer-setup.md`
- OpenAPI: `docs/oas.yml`

If you are uncertain about a business rule or a choice (e.g., revert transitions, hard-delete semantics), prefer documenting the assumption in code + tests and open a short issue asking for confirmation.
