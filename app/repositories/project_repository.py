from sqlalchemy.orm import Session
from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id, Project.deleted_at.is_(None)).first()

    def list(self):
        return self.db.query(Project).filter(Project.deleted_at.is_(None)).all()

    def list_paginated(self, offset: int, limit: int):
        q = self.db.query(Project).filter(Project.deleted_at.is_(None))
        total = q.count()
        items = q.offset(offset).limit(limit).all()
        return items, total

    def delete(self, project: Project):
        self.db.delete(project)
        self.db.commit()

    def soft_delete(self, project: Project):
        from datetime import datetime, timezone
        project.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
