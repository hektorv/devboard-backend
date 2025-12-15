from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi import Response
from app.schemas.project_schemas import (
    ProjectCreate,
    ProjectOut,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.errors import NotFoundError, ConflictError

router = APIRouter()


def _handle_domain_errors(exc: Exception):
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error_code": "NOT_FOUND", "message": str(exc)})
    if isinstance(exc, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error_code": "CONFLICT_PROJECT_HAS_TASKS", "message": str(exc)})
    raise exc


@router.post("/api/projects", response_model=ProjectResponse, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    svc = ProjectService(db)
    project = svc.create(name=payload.name, description=payload.description, status=payload.status)
    return {"data": project}


@router.get("/api/projects", response_model=ProjectListResponse)
def list_projects(page: int = 1, per_page: int = 20, db: Session = Depends(get_db)):
    svc = ProjectService(db)
    result = svc.list_paginated(page=page, per_page=per_page)
    items = result["items"]
    page = result["page"]
    per_page = result["per_page"]
    total = result["total"]
    offset = (page - 1) * per_page
    return {"data": items, "paging": {"limit": per_page, "offset": offset, "total": total}}


@router.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    svc = ProjectService(db)
    try:
        return {"data": svc.get(project_id)}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.put("/api/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    svc = ProjectService(db)
    try:
        return {"data": svc.update(project_id, **payload.dict())}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.patch("/api/projects/{project_id}/status", response_model=ProjectResponse)
def patch_project_status(project_id: int, payload: dict, db: Session = Depends(get_db)):
    # payload expected: {"status": "ARCHIVED"}
    svc = ProjectService(db)
    try:
        status = payload.get("status")
        return {"data": svc.update(project_id, status=status)}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    svc = ProjectService(db)
    try:
        svc.delete(project_id)
        return Response(status_code=204)
    except Exception as exc:
        _handle_domain_errors(exc)
