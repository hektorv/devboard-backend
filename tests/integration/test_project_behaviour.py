from fastapi.testclient import TestClient
from app.main import app


def test_delete_project_without_tasks_returns_204():
    client = TestClient(app)
    # create project
    resp = client.post("/api/projects", json={"name": "p1"})
    assert resp.status_code == 201
    project = resp.json()["data"]
    pid = project["id"]

    # delete
    resp = client.delete(f"/api/projects/{pid}")
    assert resp.status_code == 204

    # now get should return 404
    resp = client.get(f"/api/projects/{pid}")
    assert resp.status_code == 404


def test_delete_project_with_tasks_returns_409():
    client = TestClient(app)
    resp = client.post("/api/projects", json={"name": "p2"})
    assert resp.status_code == 201
    project = resp.json()["data"]
    pid = project["id"]

    # create a task for this project (direct DB insertion via API not implemented yet, so use repo)
    # Use the SDK: POST to tasks endpoint if implemented; since tasks endpoints are not present yet,
    # we use a workaround by directly accessing DB via the client app state — instead, add a task using SQLAlchemy session
    from app.db.session import SessionLocal
    from app.models.task import Task
    db = SessionLocal()
    t = Task(project_id=pid, title="task1")
    db.add(t)
    db.commit()

    # attempt delete
    resp = client.delete(f"/api/projects/{pid}")
    assert resp.status_code == 409


def test_patch_archive_sets_finished_at():
    client = TestClient(app)
    resp = client.post("/api/projects", json={"name": "p3"})
    assert resp.status_code == 201
    project = resp.json()["data"]
    pid = project["id"]

    # archive
    resp = client.patch(f"/api/projects/{pid}/status", json={"status": "ARCHIVED"})
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body.get("status") == "ARCHIVED"
    assert body.get("finished_at") is not None
