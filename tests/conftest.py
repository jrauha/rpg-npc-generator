import pytest

from config import settings
from npcgen import create_app


@pytest.fixture
def app():
    db_uri = settings.SQLALCHEMY_DATABASE_URI

    if "?" in db_uri:
        db_uri = db_uri.replace("?", "_test?")
    else:
        db_uri = f"{db_uri}_test"

    app = create_app(
        {
            "DEBUG": False,
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": db_uri,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
