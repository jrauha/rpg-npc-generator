from flask import Flask

from npcgen import routes
from npcgen.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object("config.settings")
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    app.register_blueprint(routes.bp)

    return app
