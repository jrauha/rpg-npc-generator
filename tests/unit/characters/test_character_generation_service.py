from unittest.mock import MagicMock

import pytest

from npcgen.characters.services import CharacterGeneratorService
from npcgen.core.expections import ValidationError


@pytest.fixture
def character_dao():
    return MagicMock()


@pytest.fixture
def character_generator_service(character_dao):
    return CharacterGeneratorService(character_dao)


@pytest.fixture
def options():
    return {
        "template_id": 1,
        "alignment_id": 1,
        "class_id": 1,
        "race_id": 1,
        "hints": "Some hints",
    }


def test_generate_character_success(
    character_generator_service,
    character_dao,
    options,
):
    template_character = MagicMock()
    template_character.id = 1
    template_character.is_template = True
    character_dao.get_character.return_value = template_character
    character_dao.create_character.return_value = 2

    created_id = character_generator_service.generate_character(options)

    assert created_id == 2


def test_generate_character_template_not_found(
    character_generator_service,
    character_dao,
    options,
):
    character_dao.get_character.return_value = None

    with pytest.raises(ValidationError):
        character_generator_service.generate_character(options)

    character_dao.get_character.assert_called_once_with(
        options["template_id"],
        populate_items=True,
        populate_skills=True,
    )
    character_dao.create_character.assert_not_called()
