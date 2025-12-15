from fastapi.testclient import TestClient
from app.main import app


def test_create_user_and_unique_email():
    client = TestClient(app)
    resp = client.post("/api/users", json={"display_name": "Alice", "email": "alice@example.com"})
    assert resp.status_code == 201
    user = resp.json()["data"]
    assert user["email"] == "alice@example.com"

    # duplicate
    resp = client.post("/api/users", json={"display_name": "Alice2", "email": "alice@example.com"})
    assert resp.status_code == 409


def test_list_users_pagination():
    client = TestClient(app)
    # create 7 users
    for i in range(7):
        client.post("/api/users", json={"display_name": f"U{i}", "email": f"u{i}@example.com"})

    resp = client.get("/api/users?page=2&per_page=5")
    assert resp.status_code == 200
    body = resp.json()
    paging = body.get("paging", {})
    assert paging.get("limit") == 5
    assert paging.get("offset") == 5
    assert paging.get("total") >= 7
    assert any(u["display_name"] == f"U{i}" for u in body.get("data", []))
