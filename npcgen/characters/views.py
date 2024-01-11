import json
import os

from flask import Blueprint

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


@bp.route("/")
def index():
    return "TODO"


@bp.route("/characters")
def characters():
    return "TODO"


@bp.route("/character/<int:character_id>")
def character_details(character_id):
    return "TODO"


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
