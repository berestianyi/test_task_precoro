from dependency_injector.wiring import Provide, inject
from flask import render_template, Blueprint, request
from flask_login import login_required, current_user, login_user

from src.test_task.application import ServiceContainer, InterfacesContainer
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR, get_owner_cookie
from src.test_task.interfaces.ssr.forms.auth import RegisterForm
from src.test_task.services.order.list.ports import OrderListInput
from src.test_task.services.order.list.service import OrderListService
from src.test_task.services.order.place_order.ports import PlaceOrderInput
from src.test_task.services.order.place_order.service import PlaceOrderService
from src.test_task.services.user.register.ports import RegisterInput
from src.test_task.services.user.register.service import RegisterService

order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/order",
    template_folder=str(TEMPLATES_DIR),
)


@order_bp.route("/list", methods=["GET"])
@login_required
@inject
def order_list(
        order_list_service: OrderListService = Provide[ServiceContainer.order_list_service],
):
    user_id = current_user.id
    orders = order_list_service.execute(OrderListInput(user_id=user_id))
    return render_template("orders.html", orders=orders)


@order_bp.route("/place", methods=["POST", "GET"])
@inject
def place_order(
        place_order_service: PlaceOrderService = Provide[ServiceContainer.place_order_service],
        register_service: RegisterService = Provide[ServiceContainer.register_service],
        register_form: RegisterForm = Provide[InterfacesContainer.register_form]
):

    if request.method == "POST":
        if current_user.is_authenticated:
            user_id = current_user.id
            orders = place_order_service.execute(PlaceOrderInput(user_id=user_id))
            return render_template("orders.html", orders=orders)

        if register_form.validate_on_submit():
            email = request.form["email"]
            password = request.form["password"]

            out = register_service.execute(RegisterInput(
                email=email,
                password=password,
                owner_cookie=get_owner_cookie()
            ))

            login_user(out.user)

            orders = place_order_service.execute(PlaceOrderInput(user_id=out.user.id))
            return render_template("orders.html", orders=orders)

        return render_template("cart.html", form=register_form)

    if current_user.is_authenticated:
        return render_template("cart.html")

    return render_template("cart.html", form=register_form)
