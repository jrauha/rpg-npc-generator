import json
import os

from celery import shared_task
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ..auth.decorators import login_required
from ..extensions import db
from .daos import CharacterDao, ItemDao, SkillDao
from .forms import CharacterForm
from .services import CharacterGeneratorService, CharacterTemplateService

bp = Blueprint("characters", __name__)

character_dao = CharacterDao(db.session)
item_dao = ItemDao(db.session)
skill_dao = SkillDao(db.session)

character_generator_service = CharacterGeneratorService(character_dao)
character_template_service = CharacterTemplateService(
    character_dao, item_dao, skill_dao
)


@bp.app_template_filter()
def delta(num):
    return f"+{num}" if not num or num > 0 else num


@bp.app_template_filter()
def character_description(character):
    class_name = character.class_name if character.class_name != "None" else ""
    return (
        f"Level {character.level} {character.race_name} {class_name}".strip()
        + ", "
        f"{character.alignment_name} alignment"
    )


@bp.route("/")
def index():
    return redirect(url_for("characters.generate"))


@bp.route("/characters")
@login_required
def characters():
    user_id = session["user_id"]
    page = int(request.args.get("page") or 1)
    tab = request.args.get("tab") or None
    search = request.args.get("search")
    sort = request.args.get("sort") or "date_desc"

    res = character_dao.get_characters_by_user(
        user_id,
        _resolve_template_filter(tab),
        page,
        search=search,
        sort_field="name" if sort.startswith("name") else "created_at",
        sort_desc=sort.endswith("desc"),
    )

    return render_template(
        "characters/index.html",
        tab=tab,
        sort=sort,
        search=search,
        data=res.data,
        pagination=res.pagination,
    )


def _resolve_template_filter(tab):
    if tab == "templates":
        return True
    elif tab == "my_characters":
        return False
    else:
        return None


@bp.route("/character/<int:character_id>")
@login_required
def character_details(character_id):
    character = character_dao.get_character(
        character_id, populate_items=True, populate_skills=True
    )

    if character is None:
        return "Character not found", 404

    if not character.is_template and character.user_id != session["user_id"]:
        return "Unauthorized", 401

    return render_template(
        "characters/details.html",
        character=character,
    )


@bp.route("/character/delete/<int:character_id>", methods=["POST"])
@login_required
def delete_character(character_id):
    character = character_dao.get_character(character_id)

    if character is None:
        return "Character not found", 404

    if character.is_template:
        return "Bad request", 400

    if character.user_id != session["user_id"]:
        return "Unauthorized", 401

    character_dao.soft_delete_character(character.id)
    flash(f"Character {character.name} deleted", "success")
    return redirect(url_for("characters.characters", _anchor="character"))


@bp.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    form = _init_character_form()
    user_id = session["user_id"]

    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") != "XMLHttpRequest"
    ):
        flash("Please enable javascript to generate a character", "danger")
        return redirect(url_for("characters.generate"))

    if form.validate_on_submit():
        task = generate_character.delay(
            {
                "template_id": form.get_choice_or_random(form.template_id),
                "alignment_id": form.get_choice_or_random(form.alignment_id),
                "class_id": form.get_choice_or_random(form.class_id),
                "race_id": form.get_choice_or_random(form.race_id),
                "hints": form.hints.data,
                "user_id": user_id,
            }
        )

        return {"task_id": task.id}

    character_id = request.args.get("character_id")

    if character_id:
        if not character_id.isdigit():
            return "Bad request", 400

        character = character_dao.get_character(
            character_id, populate_items=True, populate_skills=True
        )
        if character is None:
            return "Character not found", 404

        if character.user_id != user_id:
            return "Unauthorized", 401

        return render_template(
            "characters/generate.html", form=form, character=character
        )

    return render_template("characters/generate.html", form=form)


@bp.route("/generate/<task_id>")
@login_required
def generate_status(task_id):
    task = generate_character.AsyncResult(task_id)
    return {
        "ready": task.ready(),
        "successful": task.successful(),
        "value": task.result if task.ready() else None,
    }


def _get_field_choices(options):
    choices = [(opt.id, opt.name) for opt in options]
    choices.insert(0, ("", "Random"))

    return choices


def _init_character_form():
    form = CharacterForm()

    races = character_dao.get_character_race_options()
    form.race_id.choices = _get_field_choices(races)

    classes = character_dao.get_character_class_options()
    form.class_id.choices = _get_field_choices(classes)

    alignments = character_dao.get_character_alignment_options()
    form.alignment_id.choices = _get_field_choices(alignments)

    templates = character_dao.get_character_template_options()
    form.template_id.choices = _get_field_choices(templates)

    return form


# CLI Commands


@bp.cli.command("init-templates")
def init_templates():
    file_path = os.path.join("data", "character_templates.json")

    with open(file_path, "r") as file:
        characters_data = json.load(file)

        for character_data in characters_data:
            character_template_service.create_template(character_data)


# Celery Tasks


@shared_task
def generate_character(options):
    character_id = character_generator_service.generate_character(**options)
    return character_id
