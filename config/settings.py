from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


def _parse_bool(value, default=False):
    if value is None:
        return default
    return str(value).lower() in ["true", "1"]


def build_database_uri():
    url = environ.get("DATABASE_URL")
    if url:
        return url.replace("postgres://", "postgresql://", 1)

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
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
DISABLE_REGISTRATION = _parse_bool(environ.get("DISABLE_REGISTRATION"), False)

REDIS_URL = environ.get("REDIS_URL", "redis://redis:6379/0")

CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": [],
}
