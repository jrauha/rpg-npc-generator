import json
import os

from flask import Blueprint, redirect, render_template, url_for

from ..auth.decorators import login_required
from ..extensions import db
from .daos import CharacterDao, ItemDao, SkillDao
from .forms import CharacterForm
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
    return redirect(url_for("characters.generate"))


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
    form = CharacterForm()

    races = character_dao.get_character_race_options()
    form.race_id.choices = _get_field_choices(races)

    classes = character_dao.get_character_class_options()
    form.class_id.choices = _get_field_choices(classes)

    alignments = character_dao.get_character_alignment_options()
    form.alignment_id.choices = _get_field_choices(alignments)

    templates = character_dao.get_character_template_options()
    form.template_id.choices = _get_field_choices(templates)

    if form.validate_on_submit():
        # TODO: Generate character
        print(form.data)

        return redirect(
            url_for("characters.character_details", character_id=1)
        )
    else:
        return render_template("characters/generate.html", form=form)


def _get_field_choices(options):
    choices = [(opt.id, opt.name) for opt in options]
    choices.insert(0, ("", "Random"))

    return choices


# CLI Commands


@bp.cli.command("init-templates")
def init_templates():
    file_path = os.path.join("data", "character_templates.json")

    with open(file_path, "r") as file:
        characters_data = json.load(file)

        for character_data in characters_data:
            character_template_service.create_template(character_data)
