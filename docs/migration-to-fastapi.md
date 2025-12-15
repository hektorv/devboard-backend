# Migration checklist: Flask -> FastAPI (guide for contributors)

If you are migrating an existing Flask implementation or starting an implementation, follow this checklist to ensure consistency and test coverage.

1. Project layout
   - Create FastAPI app entrypoint (e.g., `app/main.py` with `app = FastAPI()`).
   - Use APIRouter modules under `app/routers/` and include them in `app/main.py`.

2. Schemas and validation
   - Define Pydantic models in `app/schemas/` for request/response payloads.
   - Keep Pydantic DTOs separate from SQLAlchemy models in `app/models/`.

3. Services and repositories
   - Keep business logic in `app/services/` and DB access in `app/repositories/`.
   - Inject services into routers using FastAPI `Depends`.

4. OpenAPI & contract-first
   - Keep `docs/oas.yml` as the contract. If you generate code from the OAS or write code directly, add a CI validation step that compares FastAPI's generated `/openapi.json` with `docs/oas.yml`.

5. Tests
   - Add unit tests for services (pytest).
   - Add integration tests for routers using FastAPI `TestClient` or `httpx.AsyncClient`.
   - Use Docker MySQL in tests (see `docker/docker-compose.test.yml`).

6. Error handling
   - Implement custom exception classes in `app/errors.py` and map them to HTTP responses via FastAPI exception handlers.
   - Ensure error payloads follow the standard shape (`error_code`, `message`, `details?`, `trace_id?`).

7. Running & docs
   - Run locally with Uvicorn: `uvicorn app.main:app --reload`.
   - Verify interactive docs at `/docs` and `/redoc`.

8. CI
   - Ensure CI installs FastAPI and Uvicorn and that contract tests/validation run as part of pipeline.

9. Acceptance
   - Add example curl commands and API payload examples to `docs/backend-architecture-spec.md` or `docs/project-spec.md`.
