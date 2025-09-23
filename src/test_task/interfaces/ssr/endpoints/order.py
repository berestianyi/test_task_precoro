from dependency_injector.wiring import Provide, inject
from flask import render_template, Blueprint, redirect, url_for, current_app, abort
from flask_login import login_required, current_user

from src.test_task.application import ServiceContainer
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR
from src.test_task.services.order.list.ports import OrderListInput
from src.test_task.services.order.list.service import OrderListService
from src.test_task.services.order.place_order.ports import PlaceOrderInput
from src.test_task.services.order.place_order.service import PlaceOrderService

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
    try:
        user_id = current_user.id
        orders = order_list_service.execute(OrderListInput(user_id=user_id))
        return render_template("orders.html", orders=orders.order)
    except Exception as e:
        current_app.logger.error(f"Invalid form input: {e}")
        abort(400)

@order_bp.route("/place", methods=["POST"])
@inject
def place_order(
        place_order_service: PlaceOrderService = Provide[ServiceContainer.place_order_service],

):
        try:
            if current_user.is_authenticated:
                user_id = current_user.id
                orders = place_order_service.execute(PlaceOrderInput(user_id=user_id))
                return render_template("orders.html", orders=orders.order)

            return redirect(url_for("get.cart"))
        except Exception as e:
            current_app.logger.error(f"Invalid form input: {e}")
            abort(400)