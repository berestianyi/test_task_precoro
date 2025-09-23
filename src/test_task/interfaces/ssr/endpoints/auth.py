
from dependency_injector.wiring import Provide, inject
from flask import render_template, redirect, url_for, Blueprint, request
from flask_login import login_required, logout_user

from src.test_task.application import ServiceContainer, InterfacesContainer
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR
from src.test_task.interfaces.ssr.forms.auth import LoginForm, RegisterForm
from src.test_task.services.user.login.ports import LoginInput
from src.test_task.services.user.login.service import LoginService
from src.test_task.services.user.register.ports import RegisterInput
from src.test_task.services.user.register.service import RegisterService



auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder=str(TEMPLATES_DIR),
)


@auth_bp.route("/login", methods=["GET", "POST"])
@inject
def login(
        login_service: LoginService = Provide[ServiceContainer.login_service],
        login_form: LoginForm = Provide[InterfacesContainer.login_from]
):
    if request.method == "POST":
        if login_form.validate_on_submit():
            email = request.form["email"]
            password = request.form["password"]

            login_service.execute(LoginInput(
                email=email,
                password=password
            ))

            return redirect(url_for("profile"))
        return render_template("login.html", form=login_form)
    return render_template("login.html", form=login_form)


@auth_bp.route("/register", methods=["GET", "POST"])
@inject
def register(
        register_service: RegisterService = Provide[ServiceContainer.register_service],
        register_form: RegisterForm = Provide[InterfacesContainer.register_form]
):
    if request.method == "POST":
        if register_form.validate_on_submit():
            email = request.form["email"]
            password = request.form["password"]

            register_service.execute(RegisterInput(
                email=email,
                password=password,
            ))

            return redirect(url_for("auth.login"))
        return render_template("register.html", form=register_form)
    return render_template("register.html", form=register_form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
