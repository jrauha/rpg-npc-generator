import pytest

from npcgen import create_app
from npcgen.extensions import db


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        DEBUG=False,
        TESTING=True,
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
