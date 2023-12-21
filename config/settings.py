from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


def build_database_uri():
    user = environ.get("POSTGRES_USER") or "postgres"
    password = environ.get("POSTGRES_PASSWORD") or "postgres"
    host = environ.get("POSTGRES_HOST") or "localhost"
    port = environ.get("POSTGRES_PORT") or "5432"
    name = environ.get("POSTGRES_DB") or "postgres"
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


# General Config
ENVIRONMENT = environ.get("ENVIRONMENT")
FLASK_APP = environ.get("FLASK_APP")
FLASK_DEBUG = environ.get("FLASK_DEBUG")
SECRET_KEY = environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = build_database_uri()
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
