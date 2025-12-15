from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.task import Task


def test_tasks_api_lifecycle():
    client = TestClient(app)
    # create project
    resp = client.post("/api/projects", json={"name": "proj1"})
    assert resp.status_code == 201
    proj = resp.json()["data"]
    pid = proj["id"]

    # create task
    resp = client.post(f"/api/projects/{pid}/tasks", json={"title": "do it"})
    assert resp.status_code == 201
    task = resp.json()["data"]
    tid = task["id"]

    # list tasks
    resp = client.get(f"/api/projects/{pid}/tasks")
    assert resp.status_code == 200
    body = resp.json()
    assert any(t["id"] == tid for t in body.get("data", []))

    # patch status to DONE
    resp = client.patch(f"/api/tasks/{tid}/status", json={"status": "DONE"})
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body.get("status") == "DONE"
    assert body.get("finished_at") is not None

    # delete
    resp = client.delete(f"/api/tasks/{tid}")
    assert resp.status_code == 204

    # ensure it's gone
    resp = client.get(f"/api/tasks/{tid}")
    assert resp.status_code == 404
