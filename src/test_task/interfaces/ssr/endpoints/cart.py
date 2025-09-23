from dependency_injector.wiring import Provide, inject
from flask import render_template, Blueprint, request, current_app, redirect, url_for, abort
from flask_login import current_user

from src.test_task.application import ServiceContainer
from src.test_task.application.middleware import get_owner_cookie
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR
from src.test_task.services.cart.add_product_to_cart.ports import AddProductToCartInput
from src.test_task.services.cart.add_product_to_cart.service import AddProductToCartService
from src.test_task.services.cart.delete_cart_item_from_cart.ports import DeleteProductFromCartInput
from src.test_task.services.cart.delete_cart_item_from_cart.service import DeleteProductFromCartService
from src.test_task.services.cart.get.ports import GetCartInput
from src.test_task.services.cart.get.service import GetCartService
from src.test_task.services.cart.remove_product_from_cart.ports import RemoveProductFromCartInput
from src.test_task.services.cart.remove_product_from_cart.service import RemoveProductFromCartService

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart",
    template_folder=str(TEMPLATES_DIR),
)


@cart_bp.route("/add/product/", methods=["POST"])
@inject
def add_product_to_cart(
        add_product_to_cart_service: AddProductToCartService = Provide[
            ServiceContainer.add_product_to_cart_service],
):
    try:
        cart_id = request.form.get("cart_id", type=int)
        product_id = request.form.get("product_id", type=int)
        owner_id = current_user.id if current_user.is_authenticated else None
        owner_cookie = get_owner_cookie()
        add_product_to_cart_service.execute(AddProductToCartInput(
            owner_id=owner_id,
            owner_cookie=owner_cookie,
            cart_id=cart_id,
            product_id=product_id
        ))
        return redirect(url_for("cart.get_cart"))

    except Exception as e:
        current_app.logger.error(f"Invalid form input: {e}")
        abort(400)


@cart_bp.route("/remove/product/", methods=["POST"])
@inject
def remove_product_from_cart(
        remove_product_to_cart_service: RemoveProductFromCartService = Provide[
            ServiceContainer.remove_product_from_cart_service],
):
    try:
        cart_id = request.form.get("cart_id", type=int)
        product_id = request.form.get("product_id", type=int)
        owner_id = current_user.id if current_user.is_authenticated else None
        owner_cookie = get_owner_cookie()

        remove_product_to_cart_service.execute(RemoveProductFromCartInput(
            owner_id=owner_id,
            owner_cookie=owner_cookie,
            cart_id=cart_id,
            product_id=product_id
        ))
        return redirect(url_for("cart.get_cart"))
    except Exception as e:
        current_app.logger.error(f"Invalid form input: {e}")
        abort(400)



@cart_bp.route("/delete/product/", methods=["POST"])
@inject
def delete_product_from_cart(
        delete_product_from_cart_service: DeleteProductFromCartService = Provide[
            ServiceContainer.delete_product_from_cart_service],
):
    try:
        cart_id = request.form.get("cart_id", type=int)
        product_id = request.form.get("product_id", type=int)
        owner_id = current_user.id if current_user.is_authenticated else None
        owner_cookie = get_owner_cookie()

        delete_product_from_cart_service.execute(DeleteProductFromCartInput(
            owner_id=owner_id,
            owner_cookie=owner_cookie,
            cart_id=cart_id,
            product_id=product_id
        ))
        return redirect(url_for("cart.get_cart"))
    except Exception as e:
        current_app.logger.error(f"Invalid form input: {e}")
        abort(400)



@cart_bp.route("/get/", methods=["GET"])
@inject
def get_cart(
        get_cart_service: GetCartService = Provide[
            ServiceContainer.get_cart_service],
):
    try:
        owner_id = current_user.id if current_user.is_authenticated else None
        owner_cookie = get_owner_cookie()

        output = get_cart_service.execute(GetCartInput(
            owner_id=owner_id,
            owner_cookie=owner_cookie,
        ))
        return render_template("cart.html", cart=output.cart)

    except Exception as e:
        current_app.logger.error(f"Invalid form input: {e}")
        abort(400)
