from fastapi.testclient import TestClient
from racerapi.core.app_factory import create_app


def test_system_health_endpoint():
    """
    Test the /system/health endpoint from SystemRepository controller.
    Ensures routing + controller decorators work correctly.
    """

    app = create_app()               # builds FastAPI app
    client = TestClient(app)         # test client

    response = client.get("/system/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
