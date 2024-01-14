import click
from flask import Blueprint, redirect, render_template, session, url_for

from ..extensions import db
from .daos import UserDao
from .decorators import login_required
from .forms import ChangePasswordForm, LoginForm
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
