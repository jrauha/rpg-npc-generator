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


def test_account(client, login_user):
    with client:
        response = client.get("/account")

        assert response.status_code == 200
        assert b"Account" in response.data
        assert login_user.username.encode() in response.data
        assert login_user.email.encode() in response.data


def test_account_unauthorized(client):
    response = client.get("/account")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_change_password(client, login_user):
    with client:
        response = client.post(
            "/change-password",
            data={
                "current_password": "password1",
                "new_password": "password2",
                "new_password_confirm": "password2",
            },
        )
        assert response.status_code == 200
        assert b"Account" in response.data
