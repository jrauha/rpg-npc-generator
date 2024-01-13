def test_character_details(client, character_fixture):
    character_id = character_fixture.id
    response = client.get(f"/character/{character_id}")

    assert response.status_code == 200
    assert character_fixture.name.encode() in response.data


def test_character_details_not_found(client):
    character_id = 999
    response = client.get(f"/character/{character_id}")

    assert response.status_code == 404
    assert b"Character not found" in response.data


def test_characters(client, character_fixture, login_user):
    with client:
        response = client.get("/characters")

        assert response.status_code == 200
