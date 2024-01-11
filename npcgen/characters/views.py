from flask import Blueprint

from ..auth.decorators import login_required

bp = Blueprint("characters", __name__)


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
    # TODO
    pass
