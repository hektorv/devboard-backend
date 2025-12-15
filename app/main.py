from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.health_router import router as health_router
from app.routers.project_router import router as project_router
from app.routers.user_router import router as user_router
from app.routers.task_router import router as task_router
from app.errors import DomainError
from app.db.session import engine, Base

app = FastAPI(title="DevBoard Backend")


@app.on_event("startup")
def on_startup():
    # Create DB tables (for dev / scaffold). In production, use migrations.
    Base.metadata.create_all(bind=engine)


# Ensure tables exist even if startup events are not triggered by the test runner.
# This makes tests more robust in simple environments. In production, use migrations.
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # If DB isn't available at import time, defer to startup event.
    pass


@app.exception_handler(DomainError)
def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(status_code=400, content={"error_code": "CONFLICT_BUSINESS_RULE", "message": str(exc)})


app.include_router(health_router)
app.include_router(project_router)
app.include_router(user_router)
app.include_router(task_router)
