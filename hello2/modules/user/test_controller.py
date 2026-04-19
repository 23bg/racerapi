from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_items():
    response = client.get("/users")
    assert response.status_code == 200
