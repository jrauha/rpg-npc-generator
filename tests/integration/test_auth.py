from flask import session


def test_login_success(client, user_fixture):
    assert client.get("/login").status_code == 200

    with client:
        client.post(
            "/login", data={"username": "admin", "password": "password1"}
        )
        assert isinstance(session["user_id"], int)


def test_login_invalid_credentials(client, user_fixture):
    assert client.get("/login").status_code == 200

    with client:
        client.post("/login", data={"username": "admin", "password": "wrong"})
        assert "user_id" not in session


def test_logout(client, user_fixture):
    with client:
        client.get("/logout")
        assert "user_id" not in session
