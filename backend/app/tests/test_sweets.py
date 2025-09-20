def register_and_login_admin(client):
    \
    client.post("/api/auth/register", json={"username": "admin", "password": "pass123"})
    r = client.post("/api/auth/login", data={"username": "admin", "password": "pass123"})
    assert r.status_code == 200
    return r.json()["access_token"]
def test_sweet_crud_and_purchase(client):
    admin_token = register_and_login_admin(client)
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    \
\
    s = {"name":"Test Sweet","category":"Traditional","price":20.5,"quantity":10}
    r = client.post("/api/sweets", json=s, headers=admin_headers)
    assert r.status_code == 200
    sweet = r.json()
    sweet_id = sweet["id"]
    \
\
    r2 = client.post(f"/api/sweets/{sweet_id}/purchase?qty=2", headers=admin_headers)
    assert r2.status_code == 200
    assert r2.json()["quantity"] == 8
    \
\
    r3 = client.get("/api/sweets/search?query=Test")
    assert r3.status_code == 200
    assert any(item["id"] == sweet_id for item in r3.json())
