from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.models.project import Project, ProjectStatus
from sqlalchemy.orm import Session
from app.errors import NotFoundError, ConflictError


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)
        self.task_repo = TaskRepository(db)

    def create(self, name: str, description: str = None, status: ProjectStatus = ProjectStatus.ACTIVE):
        project = Project(name=name, description=description, status=status)
        return self.repo.create(project)

    def get(self, project_id: int):
        project = self.repo.get(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project

    def list(self):
        return self.repo.list()

    def list_paginated(self, page: int = 1, per_page: int = 20):
        if page < 1:
            page = 1
        per_page = max(1, min(per_page, 100))
        offset = (page - 1) * per_page
        items, total = self.repo.list_paginated(offset, per_page)
        return {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
        }

    def delete(self, project_id: int):
        project = self.repo.get(project_id)
        if not project:
            raise NotFoundError("Project not found")
        count = self.task_repo.count_by_project(project_id)
        if count > 0:
            raise ConflictError("Project has tasks and cannot be deleted")
        # Soft delete by default
        self.repo.soft_delete(project)

    def update(self, project_id: int, **patch):
        project = self.get(project_id)
        # Handle status change side-effects
        status = patch.get("status")
        if status is not None and status == ProjectStatus.ARCHIVED:
            from datetime import datetime, timezone
            project.finished_at = datetime.now(timezone.utc)

        for k, v in patch.items():
            if v is not None and k != "status":
                setattr(project, k, v)
        if status is not None:
            project.status = status
        self.db.commit()
        self.db.refresh(project)
        return project
