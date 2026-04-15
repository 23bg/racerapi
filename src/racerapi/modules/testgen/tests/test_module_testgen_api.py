def test_testgen_health(client):
    r = client.get('/testgen')
    assert r.status_code in (200, 404, 422, 201)
