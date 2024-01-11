from unittest.mock import MagicMock

import pytest

from npcgen.characters.services import CharacterTemplateService
from npcgen.core.expections import ValidationError


@pytest.fixture
def character_dao():
    return MagicMock()


@pytest.fixture
def item_dao():
    return MagicMock()


@pytest.fixture
def skill_dao():
    return MagicMock()


@pytest.fixture
def character_template_service(character_dao, item_dao, skill_dao):
    return CharacterTemplateService(character_dao, item_dao, skill_dao)


@pytest.fixture
def character_data():
    return {
        "name": "Template1",
        "race_id": 1,
        "alignment_id": 1,
        "level": 1,
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "charisma": 10,
        "constitution": 10,
        "wisdom": 10,
        "armor_class": 10,
        "hit_points": 10,
        "speed": 10,
        "fortitude_save": 10,
        "reflex_save": 10,
        "will_save": 10,
        "perception": 10,
        "items": [
            {
                "name": "Sword",
                "damage": 5,
                "damage_type": "S",
                "item_type": "Melee weapon",
                "traits": ["sharp"],
                "proficiency": 10,
            }
        ],
        "skills": [
            {
                "name": "Acrobatics",
                "proficiency": 10,
            }
        ],
    }


def test_create_template_success(
    character_template_service,
    character_dao,
    character_data,
):
    character_dao.character_with_name_exists.return_value = False

    character_template_service.create_template(character_data)

    character_dao.character_with_name_exists.assert_called_once_with(
        "Template1"
    )
    character_dao.create_character.assert_called_once()


def test_create_template_existing_name(
    character_template_service, character_dao, character_data
):
    character_dao.character_with_name_exists.return_value = True

    with pytest.raises(ValidationError):
        character_template_service.create_template(character_data)

    character_dao.character_with_name_exists.assert_called_once_with(
        "Template1"
    )
    character_dao.create_character.assert_not_called()
