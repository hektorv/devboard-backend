import pytest
from app.db.session import Base, engine, SessionLocal
from app.services.project_service import ProjectService
from app.models.project import Project
from app.models.task import Task


@pytest.fixture(autouse=True)
def setup_db():
    # create tables and a fresh DB per test (sqlite memory is fine here)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_delete_project_with_tasks_raises_conflict():
    db = SessionLocal()
    svc = ProjectService(db)
    project = svc.create(name="Test project")
    # create a task attached to project
    task = Task(project_id=project.id, title="t1")
    db.add(task)
    db.commit()

    with pytest.raises(Exception) as exc:
        svc.delete(project.id)
    assert "cannot be deleted" in str(exc.value) or "has tasks" in str(exc.value)
