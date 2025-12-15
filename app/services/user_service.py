from app.repositories.user_repository import UserRepository
from app.models.user import User
from sqlalchemy.orm import Session
from app.errors import ConflictError, NotFoundError


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create(self, display_name: str, email: str):
        existing = self.repo.by_email(email)
        if existing:
            raise ConflictError("User with that email already exists")
        user = User(display_name=display_name, email=email)
        return self.repo.create(user)

    def get(self, user_id: int):
        user = self.repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_paginated(self, page: int = 1, per_page: int = 20):
        if page < 1:
            page = 1
        per_page = max(1, min(per_page, 100))
        offset = (page - 1) * per_page
        items, total = self.repo.list_paginated(offset, per_page)
        return {"items": items, "page": page, "per_page": per_page, "total": total}

    def update(self, user_id: int, **patch):
        user = self.get(user_id)
        if "email" in patch and patch["email"] is not None:
            existing = self.repo.by_email(patch["email"])
            if existing and existing.id != user.id:
                raise ConflictError("Email already in use")
        for k, v in patch.items():
            if v is not None:
                setattr(user, k, v)
        return self.repo.update(user)

    def deactivate(self, user_id: int):
        user = self.get(user_id)
        user.is_active = False
        return self.repo.update(user)
