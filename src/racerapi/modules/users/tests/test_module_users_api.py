def test_users_health(client):
    r = client.get('/users')
    assert r.status_code in (200, 404, 422, 201)
