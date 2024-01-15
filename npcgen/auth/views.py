import click
from flask import Blueprint, flash, redirect, render_template, session, url_for

from ..core.expections import ValidationError
from ..extensions import db
from .daos import UserDao
from .decorators import login_required
from .forms import ChangePasswordForm, LoginForm, RegistrationForm
from .models import User
from .services import AuthService

bp = Blueprint("auth", __name__)

user_dao = UserDao(db.session)
auth_service = AuthService(user_dao)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = auth_service.authenticate(username, password)
        if not user:
            return render_template(
                "auth/login.html",
                form=form,
                error="Invalid username or password",
            )
        session["user_id"] = user.id
        return redirect(url_for("auth.account"))

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User(username=username, email=email, password=password)
            auth_service.register_user(user)
            flash("Account created successfully.", "success")
            return redirect(url_for("auth.login"))
        except ValidationError as e:
            form_error = getattr(form, e.attribute)
            form_error.errors.append(e.reason)
            return render_template("auth/register.html", form=form)

    return render_template("auth/register.html", form=form)


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user_id = session.get("user_id")
        user = user_dao.get_user_by_id(user_id)
        old_password = form.old_password.data
        new_password = form.new_password.data
        if auth_service.authenticate(user.username, old_password):
            user_dao.update_password(user.id, new_password)
            return redirect(url_for("auth.account"))

        return render_template(
            "auth/change_password.html",
            form=form,
            error="Invalid old password",
        )

    return render_template("auth/change_password.html", form=form)


@bp.route("/account")
@login_required
def account():
    user_id = session.get("user_id")
    user = user_dao.get_user_by_id(user_id)
    return render_template("auth/account.html", user=user)


@bp.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))


# CLI Commands


@bp.cli.command("create-user")
@click.option("--username", prompt="Username")
@click.option("--email", prompt="Email")
@click.option("--password", prompt="Password")
@click.option("--superuser/--user", default=False)
def create(username, email, password, superuser):
    user = User(
        username=username, email=email, password=password, superuser=superuser
    )
    auth_service.register_user(user)


@bp.cli.command("delete-user")
@click.option("--username", prompt="Username")
def remove(username):
    user = user_dao.get_user_by_username(username)
    if not user:
        raise click.BadParameter(f"User {username} does not exist")
    if click.confirm(f"Are you sure you want to delete {username}?"):
        user_dao.soft_delete_user(user.id)
