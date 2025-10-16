import os
os.environ["INTELLIDOC_FAST_INIT"] = "1"
os.environ["PYTHONHASHSEED"] = "0"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session


def setup_module(module):
    # Fresh DB for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_auth_register_login_and_me():
    # register
    r = client.post("/api/auth/register", json={"email": "test@example.com", "password": "pw123456"})
    assert r.status_code == 200
    user = r.json()
    assert user["email"] == "test@example.com"

    # login
    r = client.post("/api/auth/login", data={"username": "test@example.com", "password": "pw123456"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # me
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == "test@example.com"


def test_documents_crud_flow():
    # login
    r = client.post("/api/auth/login", data={"username": "test@example.com", "password": "pw123456"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # upload a small text file
    files = {"file": ("hello.txt", b"Hello world. This is a test document.", "text/plain")}
    data = {"category": "technical"}
    r = client.post("/api/documents/upload", headers=headers, files=files, data=data)
    assert r.status_code == 200
    doc = r.json()
    doc_id = doc["id"]

    # list
    r = client.get("/api/documents/", headers=headers)
    assert r.status_code == 200
    docs = r.json()
    assert any(d["id"] == doc_id for d in docs)

    # get
    r = client.get(f"/api/documents/{doc_id}", headers=headers)
    assert r.status_code == 200

    # query
    r = client.post(f"/api/documents/{doc_id}/query", headers=headers, json={"query": "What is this?"})
    assert r.status_code == 200
    assert "answer" in r.json()

    # search
    r = client.post("/api/documents/search", headers=headers, json={"query": "Hello", "limit": 5})
    assert r.status_code == 200

    # delete
    r = client.delete(f"/api/documents/{doc_id}", headers=headers)
    assert r.status_code == 200


