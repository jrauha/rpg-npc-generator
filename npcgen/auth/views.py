import click
from flask import Blueprint, redirect, render_template, session, url_for

from ..extensions import db
from .daos import UserDao
from .decorators import login_required
from .forms import LoginForm
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
    else:
        return render_template("auth/login.html", form=form)


@login_required
@bp.route("/account")
def account():
    user_id = session.get("user_id")
    user = user_dao.get_user_by_id(user_id)
    return render_template("auth/account.html", user=user)


@login_required
@bp.route("/logout")
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
