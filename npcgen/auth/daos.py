from sqlalchemy import text
from werkzeug.security import generate_password_hash

from ..core.db_utils import create_record, delete_record, update_record
from .models import User


class UserDao:
    USER_TABLE = "app_user"

    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_username(self, username):
        record = self.db_session.execute(
            text(
                f"""
            SELECT
            id,
            username,
            email,
            password,
            superuser
            FROM {self.USER_TABLE}
            WHERE username = :username
            AND deleted = FALSE
            """
            ),
            {"username": username},
        ).fetchone()
        return self._map_record_to_user(record) if record else None

    def get_user_by_email(self, email):
        record = self.db_session.execute(
            text(
                f"""
            SELECT
            id,
            username,
            email,
            password,
            superuser
            FROM {self.USER_TABLE}
            WHERE email = :email
            AND deleted = FALSE
            """
            ),
            {"email": email},
        ).fetchone()
        return self._map_record_to_user(record) if record else None

    def get_user_by_id(self, user_id):
        record = self.db_session.execute(
            text(
                f"""
            SELECT
            id,
            username,
            email,
            password,
            superuser
            FROM {self.USER_TABLE}
            WHERE id = :user_id
            AND deleted = FALSE
            """
            ),
            {"user_id": user_id},
        ).fetchone()
        return self._map_record_to_user(record) if record else None

    def create_user(self, user):
        user = create_record(
            self.db_session,
            self.USER_TABLE,
            returning="*",
            username=user.username,
            email=user.email,
            password=generate_password_hash(user.password),
            superuser=user.superuser,
        )

        self.db_session.commit()
        return self._map_record_to_user(user)

    def update_password(self, user_id, password):
        update_record(
            self.db_session,
            self.USER_TABLE,
            user_id,
            password=generate_password_hash(password),
        )
        self.db_session.commit()

    def delete_user(self, user_id):
        delete_record(self.db_session, self.USER_TABLE, user_id)
        self.db_session.commit()

    def soft_delete_user(self, user_id):
        update_record(self.db_session, self.USER_TABLE, user_id, deleted=True)
        self.db_session.commit()

    def _map_record_to_user(self, record):
        return User(
            id=record.id,
            username=record.username,
            email=record.email,
            password=record.password,
            superuser=record.superuser,
        )
