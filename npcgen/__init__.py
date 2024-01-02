from flask import Flask

from npcgen import routes
from npcgen.extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")

    db.init_app(app)

    app.register_blueprint(routes.bp)

    return app
