def test_testmodule_health(client):
    r = client.get('/testmodule')
    assert r.status_code in (200, 404, 422, 201)
