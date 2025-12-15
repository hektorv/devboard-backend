from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def list_paginated(self, offset: int, limit: int):
        q = self.db.query(User)
        total = q.count()
        items = q.offset(offset).limit(limit).all()
        return items, total

    def update(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user
