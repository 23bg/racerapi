def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_users_crud_flow(client):
    create = client.post(
        "/users", json={"email": "api@example.com", "full_name": "Api User"}
    )
    assert create.status_code == 201
    user_id = create.json()["id"]

    get_one = client.get(f"/users/{user_id}")
    assert get_one.status_code == 200
    assert get_one.json()["email"] == "api@example.com"

    patch = client.patch(f"/users/{user_id}", json={"full_name": "API User Updated"})
    assert patch.status_code == 200
    assert patch.json()["full_name"] == "API User Updated"

    listed = client.get("/users?page=1&page_size=10")
    assert listed.status_code == 200
    assert listed.json()["total"] >= 1


def test_users_duplicate_email_returns_conflict_error_payload(client):
    first = client.post(
        "/users", json={"email": "dup@example.com", "full_name": "First"}
    )
    assert first.status_code == 201

    second = client.post(
        "/users", json={"email": "dup@example.com", "full_name": "Second"}
    )
    assert second.status_code == 409

    body = second.json()
    assert body["error"]["code"] == "conflict"
    assert body["error"]["request_id"] is not None


def test_not_found_error_returns_safe_payload_and_request_id_header(client):
    response = client.get("/users/999999", headers={"x-request-id": "req-123"})

    assert response.status_code == 404
    assert response.headers["x-request-id"] == "req-123"
    payload = response.json()
    assert payload["error"]["code"] == "not_found"
    assert payload["error"]["request_id"] == "req-123"
