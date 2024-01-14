from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = StringField("Old password", validators=[DataRequired()])
    new_password = StringField(
        "New password", validators=[DataRequired(), Length(min=8)]
    )
    new_password_confirm = StringField(
        "Confirm new password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
