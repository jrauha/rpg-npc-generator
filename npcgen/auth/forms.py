from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Length(min=6, max=50), Email()]
    )
    password = StringField(
        "Password", validators=[DataRequired(), Length(min=8, max=100)]
    )
    password_confirm = StringField(
        "Confirm password",
        validators=[
            DataRequired(),
            Length(min=8, max=100),
            EqualTo("password", message="Passwords must match"),
        ],
    )
