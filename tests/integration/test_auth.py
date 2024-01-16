from flask import session


def test_login_success(client, user_fixture):
    assert client.get("/login").status_code == 200

    with client:
        client.post(
            "/login",
            data={"username": user_fixture.username, "password": "password1"},
        )
        assert "user_id" in session
        assert isinstance(session["user_id"], int)


def test_login_invalid_credentials(client, user_fixture):
    assert client.get("/login").status_code == 200

    with client:
        client.post(
            "/login",
            data={"username": user_fixture.username, "password": "wrong"},
        )
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


def test_registration_success(client):
    assert client.get("/register").status_code == 200

    with client:
        response = client.post(
            "/register",
            data={
                "username": "new_user",
                "email": "new_user@aol.com",
                "password": "password1",
                "password_confirm": "password1",
            },
        )
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


def test_registration_invalid_credentials(client):
    assert client.get("/register").status_code == 200

    with client:
        response = client.post(
            "/register",
            data={
                "username": "new_user",
                "email": "new_user@example.com",
                "password": "password1",
                "password_confirm": "wrong",
            },
        )
        assert response.status_code == 200
        assert b"Passwords must match" in response.data


def test_registration_existing_username(client, user_fixture):
    assert client.get("/register").status_code == 200

    with client:
        response = client.post(
            "/register",
            data={
                "username": user_fixture.username,
                "email": "new_user@example.com",
                "password": "password1",
                "password_confirm": "password1",
            },
        )
        assert response.status_code == 200
        assert b"Username already exists" in response.data


def test_registration_existing_email(client, user_fixture):
    assert client.get("/register").status_code == 200

    with client:
        response = client.post(
            "/register",
            data={
                "username": "new_user",
                "email": user_fixture.email,
                "password": "password1",
                "password_confirm": "password1",
            },
        )
        assert response.status_code == 200
        assert b"Email already exists" in response.data


def test_disable_registration(app, client):
    app.config["DISABLE_REGISTRATION"] = True

    response = client.get("/register")
    assert response.status_code == 200
    assert b"Registration is currently disabled" in response.data
