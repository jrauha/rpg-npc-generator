import pytest

from npcgen import create_app
from npcgen.auth.models import User
from npcgen.characters.models import Character, Gender
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


@pytest.fixture
def character_fixture(session, user_fixture):
    from npcgen.characters.daos import CharacterDao

    test_character = Character(
        alignment_id=1,
        class_id=2,
        race_id=3,
        level=5,
        gender=Gender.MALE,
        name="John Doe",
        hints="",
        backstory="",
        plot_hook="",
        strength=10,
        dexterity=12,
        constitution=14,
        intelligence=16,
        wisdom=18,
        charisma=20,
        perception=15,
        armor_class=18,
        hit_points=50,
        speed=30,
        fortitude_save=8,
        reflex_save=6,
        will_save=10,
        id=1,
        alignment_name="Neutral",
        class_name="Fighter",
        template_id=None,
        template_name=None,
        race_name="Human",
        user_id=user_fixture.id,
        is_template=False,
        skills=[],
        items=[],
    )

    character_dao = CharacterDao(session)
    id = character_dao.create_character(test_character)
    test_character.id = id

    yield test_character

    character_dao.delete_character(id)


@pytest.fixture
def login_user(client, user_fixture):
    with client.session_transaction() as sess:
        sess["user_id"] = user_fixture.id
