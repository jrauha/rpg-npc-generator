def test_hello(client):
    response = client.get("/")
    assert b"Hello, World!" in response.data
