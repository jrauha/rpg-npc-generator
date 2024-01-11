import json
import os

from flask import Blueprint, render_template

from ..auth.decorators import login_required
from ..extensions import db
from .daos import CharacterDao, ItemDao, SkillDao
from .services import CharacterTemplateService

bp = Blueprint("characters", __name__)

character_dao = CharacterDao(db.session)
item_dao = ItemDao(db.session)
skill_dao = SkillDao(db.session)

character_template_service = CharacterTemplateService(
    character_dao, item_dao, skill_dao
)


@bp.app_template_filter()
def delta(num):
    return f"+{num}" if not num or num > 0 else num


@bp.route("/")
def index():
    return "TODO"


@bp.route("/characters")
def characters():
    return "TODO"


@bp.route("/character/<int:character_id>")
def character_details(character_id):
    character = character_dao.get_character(
        character_id, populate_items=True, populate_skills=True
    )

    if character is None:
        return "Character not found", 404

    return render_template(
        "characters/details.html",
        character=character,
    )


@bp.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    return "TODO"


# CLI Commands


@bp.cli.command("init-templates")
def init_templates():
    file_path = os.path.join("data", "character_templates.json")

    with open(file_path, "r") as file:
        characters_data = json.load(file)

        for character_data in characters_data:
            character_template_service.create_template(character_data)
