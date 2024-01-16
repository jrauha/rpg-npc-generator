from werkzeug.security import check_password_hash

from ..core.expections import ValidationError


class AuthService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def authenticate(self, username, password):
        user = self.user_dao.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return user

    def register_user(self, user):
        if self.user_dao.get_user_by_username(user.username):
            raise ValidationError("username", "Username already exists")
        if self.user_dao.get_user_by_email(user.email):
            raise ValidationError("email", "Email already exists")
        if len(user.password) < 8:
            raise ValidationError(
                "password", "Password must be at least 8 characters long"
            )

        user_id = self.user_dao.create_user(user)

        return user_id
