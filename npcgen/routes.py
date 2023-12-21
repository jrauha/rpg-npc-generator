from flask import Blueprint
from sqlalchemy import text

from npcgen.extensions import db

bp = Blueprint("routes", __name__)


@bp.route("/")
def hello():
    now = db.session.execute(text("SELECT now();"))
    return "Hello, World! Time: " + now.fetchone()[0].isoformat()
