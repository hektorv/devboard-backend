from app.services.task_service import TaskService
from app.db.session import SessionLocal
from app.services.project_service import ProjectService
from app.db.session import Base, engine


def test_task_lifecycle():
    # ensure tables exist for this test run
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    ps = ProjectService(db)
    project = ps.create(name="tst_project")
    ts = TaskService(db)
    task = ts.create(project_id=project.id, title="task1")
    assert task.id is not None

    # get
    t2 = ts.get(task.id)
    assert t2.title == "task1"

    # update status to DONE sets finished_at
    ts.update(task.id, status="DONE")
    t3 = ts.get(task.id)
    assert t3.status == "DONE"
    assert t3.finished_at is not None

    # delete (soft)
    ts.delete(task.id)
    try:
        ts.get(task.id)
        assert False, "Expected NotFoundError"
    except Exception:
        pass
