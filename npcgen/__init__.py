from flask import Flask
from . import routes


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object("config.Config")
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(routes.bp)

    return app
