from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "API is running"


def test_process_invalid_file():
    response = client.post(
        "/api/process",
        data={"claim_id": "test123"},
        files={"file": ("test.txt", b"invalid content")}
    )
    assert response.status_code in [400, 422]