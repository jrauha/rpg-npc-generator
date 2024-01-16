import openai
from celery import Celery, Task
from flask import Flask

from .auth import views as auth_views
from .characters import views as character_views
from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")
    openai.api_key = app.config.get("OPENAI_API_KEY")

    db.init_app(app)

    app.register_blueprint(auth_views.bp, name="auth")
    app.register_blueprint(character_views.bp, name="characters")

    return app


def create_celery_app(app=None):
    app = app or create_app()

    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    celery.set_default()
    app.extensions["celery"] = celery

    return celery


celery_app = create_celery_app()
