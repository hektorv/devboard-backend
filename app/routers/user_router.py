from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import (
    UserCreate,
    UserOut,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.errors import NotFoundError, ConflictError

router = APIRouter()


def _handle_domain_errors(exc: Exception):
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error_code": "NOT_FOUND", "message": str(exc)})
    if isinstance(exc, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error_code": "CONFLICT_USER_EMAIL", "message": str(exc)})
    raise exc


@router.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        user = svc.create(display_name=payload.display_name, email=payload.email)
        return {"data": user}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.get("/api/users", response_model=UserListResponse)
def list_users(page: int = 1, per_page: int = 20, db: Session = Depends(get_db)):
    svc = UserService(db)
    result = svc.list_paginated(page=page, per_page=per_page)
    items = result["items"]
    page = result["page"]
    per_page = result["per_page"]
    total = result["total"]
    offset = (page - 1) * per_page
    return {"data": items, "paging": {"limit": per_page, "offset": offset, "total": total}}


@router.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        return {"data": svc.get(user_id)}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        return {"data": svc.update(user_id, **payload.dict())}
    except Exception as exc:
        _handle_domain_errors(exc)


@router.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    svc = UserService(db)
    svc.deactivate(user_id)
    return None
