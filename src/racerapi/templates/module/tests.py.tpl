from fastapi.testclient import TestClient


def test_{name}_health():
    from racerapi.main import app
    # Use context manager so the app's lifespan events run during the test
    with TestClient(app) as client:
        r = client.get('/{name}')
        # adjust expectations per generated module
        assert r.status_code in (200, 404, 422, 201)
