from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi import Response
from app.schemas.task_schemas import (
    TaskCreate,
    TaskOut,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)
from app.schemas.project_schemas import StatusUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.task_service import TaskService
from app.errors import NotFoundError

router = APIRouter()


def _handle_domain_errors(exc: Exception):
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error_code": "NOT_FOUND", "message": str(exc)})
    raise exc


@router.post("/api/projects/{project_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db)):
    svc = TaskService(db)
    task = svc.create(project_id=project_id, title=payload.title, description=payload.description, status=payload.status, priority=payload.priority, assignee_user_id=payload.assignee_user_id)
    return {"data": task}


@router.get("/api/projects/{project_id}/tasks", response_model=TaskListResponse)
def list_tasks(project_id: int, db: Session = Depends(get_db)):
    svc = TaskService(db)
    items = svc.list_by_project(project_id)
    return {"data": items, "paging": {"limit": len(items), "offset": 0, "total": len(items)}}


@router.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    svc = TaskService(db)
    try:
        return {"data": svc.get(task_id)}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    svc = TaskService(db)
    try:
        return {"data": svc.update(task_id, **payload.dict())}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.patch("/api/tasks/{task_id}/status", response_model=TaskResponse)
def patch_task_status(task_id: int, payload: dict, db: Session = Depends(get_db)):
    svc = TaskService(db)
    try:
        status = payload.get("status")
        return {"data": svc.update(task_id, status=status)}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    svc = TaskService(db)
    try:
        svc.delete(task_id)
        return Response(status_code=204)
    except Exception as exc:
        _handle_domain_errors(exc)
