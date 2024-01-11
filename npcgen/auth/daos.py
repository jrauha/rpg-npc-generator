from werkzeug.security import generate_password_hash

from ..core.db_utils import (
    create_record,
    delete_record,
    read_record_by_attr,
    read_record_by_id,
)
from .models import User


class UserDao:
    USER_TABLE = "app_user"

    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_username(self, username):
        record = read_record_by_attr(
            self.db_session, self.USER_TABLE, "username", username
        )
        return self._map_record_to_user(record) if record else None

    def get_user_by_email(self, email):
        record = read_record_by_attr(
            self.db_session, self.USER_TABLE, "email", email
        )
        return self._map_record_to_user(record) if record else None

    def get_user_by_id(self, user_id):
        record = read_record_by_id(self.db_session, self.USER_TABLE, user_id)
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

    def delete_user(self, user_id):
        delete_record(self.db_session, self.USER_TABLE, user_id)
        self.db_session.commit()

    def _map_record_to_user(self, record):
        return User(
            id=record.id,
            username=record.username,
            email=record.email,
            password=record.password,
            superuser=record.superuser,
        )
