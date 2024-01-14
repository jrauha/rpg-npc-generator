def test_character_details(client, character_fixture, login_user):
    character_id = character_fixture.id
    response = client.get(f"/character/{character_id}")

    assert response.status_code == 200
    assert character_fixture.name.encode() in response.data


def test_character_details_not_found(client, login_user):
    character_id = 999
    response = client.get(f"/character/{character_id}")

    assert response.status_code == 404
    assert b"Character not found" in response.data


def test_characters(client, character_fixture, login_user):
    with client:
        response = client.get("/characters")

        assert response.status_code == 200


def test_unauthorized_access(client):
    response = client.get("/characters")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_generate(client, login_user):
    with client:
        response = client.get("/generate")

        assert response.status_code == 200
        assert b"Generate an NPC" in response.data


def test_delete_character(client, character_fixture, login_user):
    character_id = character_fixture.id
    response = client.post(f"/character/delete/{character_id}")

    assert response.status_code == 302
    assert "/characters" in response.headers["Location"]

    # Assert deletion
    response = client.get(f"/character/{character_id}")
    assert response.status_code == 404


def test_delete_character_not_found(client, login_user):
    character_id = 999
    response = client.post(f"/character/delete/{character_id}")

    assert response.status_code == 404
    assert b"Character not found" in response.data


def test_delete_character_unauthorized(client, character_fixture):
    character_id = character_fixture.id
    response = client.post(f"/character/delete/{character_id}")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_delete_character_template(
    client, character_template_fixture, login_user
):
    character_id = character_template_fixture.id
    response = client.post(f"/character/delete/{character_id}")

    assert response.status_code == 400
    assert b"Bad request" in response.data
