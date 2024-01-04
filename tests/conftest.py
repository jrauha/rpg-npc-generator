import pytest

from npcgen import create_app
from npcgen.auth.models import User
from npcgen.extensions import db


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        DEBUG=False,
        TESTING=True,
        WTF_CSRF_ENABLED=False,
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


@pytest.fixture
def user_fixture(session):
    from npcgen.auth.daos import UserDao

    test_admin = User(
        username="admin",
        email="admin@example.org",
        password="password1",
        superuser=True,
    )

    user_dao = UserDao(session)
    user = user_dao.create_user(test_admin)

    yield user

    user_dao.delete_user(user.id)
