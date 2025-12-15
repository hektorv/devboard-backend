from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.task import Task, TaskStatus
from app.errors import NotFoundError
from app.utils.logging_decorator import service_log


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    @service_log
    def create(self, project_id: int, title: str, description: str = None, status: TaskStatus = TaskStatus.BACKLOG, priority=None, assignee_user_id: int = None):
        # ensure project exists
        project = self.project_repo.get(project_id)
        if not project:
            raise NotFoundError("Project not found")
        task = Task(project_id=project_id, title=title, description=description, status=status, priority=priority, assignee_user_id=assignee_user_id)
        return self.repo.create(task)

    @service_log
    def get(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not task:
            raise NotFoundError("Task not found")
        return task

    @service_log
    def list_by_project(self, project_id: int):
        return self.repo.by_project(project_id)

    @service_log
    def update(self, task_id: int, **patch):
        task = self.get(task_id)
        status = patch.get("status")
        # Normalize status string to enum if needed
        if status is not None and isinstance(status, str):
            try:
                status = TaskStatus(status)
            except Exception:
                # invalid status value; let DB/validation handle it downstream
                pass

        if status is not None and status == TaskStatus.DONE:
            from datetime import datetime, timezone
            task.finished_at = datetime.now(timezone.utc)

        for k, v in patch.items():
            if v is not None and k != "status":
                setattr(task, k, v)
        if status is not None:
            task.status = status
        self.db.commit()
        self.db.refresh(task)
        return task

    @service_log
    def delete(self, task_id: int):
        task = self.get(task_id)
        from datetime import datetime, timezone
        task.deleted_at = datetime.now(timezone.utc)
        self.db.commit()