def test_register_and_login(client):
    \
    r = client.post("/api/auth/register", json={"username":"tester","password":"pass123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["is_admin"] is True
    \
\
    r2 = client.post("/api/auth/login", data={"username":"tester","password":"pass123"})
    assert r2.status_code == 200
    token_data = r2.json()
    assert "access_token" in token_data
    assert token_data["is_admin"] is True
