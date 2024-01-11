from flask import Flask

from .auth import views as auth_views
from .characters import views as character_views
from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")

    db.init_app(app)

    app.register_blueprint(auth_views.bp, name="auth")
    app.register_blueprint(character_views.bp, name="characters")

    return app
