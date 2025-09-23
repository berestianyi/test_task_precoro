from dependency_injector.wiring import Provide, inject
from flask import render_template, Blueprint, request
from flask_login import current_user

from src.test_task.application import ServiceContainer
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR, get_owner_cookie
from src.test_task.services.cart.add_product_to_cart.ports import AddProductToCartInput
from src.test_task.services.cart.add_product_to_cart.service import AddProductToCartService
from src.test_task.services.cart.delete_cart_item_from_cart.ports import DeleteProductFromCartInput
from src.test_task.services.cart.delete_cart_item_from_cart.service import DeleteProductFromCartService
from src.test_task.services.cart.remove_product_from_cart.ports import RemoveProductFromCartInput
from src.test_task.services.cart.remove_product_from_cart.service import RemoveProductFromCartService

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart",
    template_folder=str(TEMPLATES_DIR),
)


@cart_bp.route("/list", methods=["POST"])
@inject
def add_product_to_cart(
        add_product_to_cart_service: AddProductToCartService = Provide[
            ServiceContainer.add_product_to_cart_service],
):
    owner_id = current_user.id if current_user.is_authenticated else None
    owner_cookie = get_owner_cookie()
    output = add_product_to_cart_service.execute(AddProductToCartInput(
        owner_id=owner_id,
        owner_cookie=owner_cookie,
        cart_id=int(request.form["cart_id"]),
        product_id=int(request.form["product_id"])
    ))
    return render_template("cart.html", cart=output)


@cart_bp.route("/list", methods=["POST"])
@inject
def remove_product_from_cart(
        remove_product_to_cart_service: RemoveProductFromCartService = Provide[
            ServiceContainer.remove_product_from_cart_service],
):
    owner_id = current_user.id if current_user.is_authenticated else None
    owner_cookie = get_owner_cookie()

    output = remove_product_to_cart_service.execute(RemoveProductFromCartInput(
        owner_id=owner_id,
        owner_cookie=owner_cookie,
        cart_id=int(request.form["cart_id"]),
        product_id=int(request.form["product_id"])
    ))
    return render_template("cart.html", cart=output)


@cart_bp.route("/list", methods=["POST"])
@inject
def delete_product_from_cart(
        delete_product_from_cart_service: DeleteProductFromCartService = Provide[
            ServiceContainer.delete_product_from_cart_service],
):
    owner_id = current_user.id if current_user.is_authenticated else None
    owner_cookie = get_owner_cookie()

    output = delete_product_from_cart_service.execute(DeleteProductFromCartInput(
        owner_id=owner_id,
        owner_cookie=owner_cookie,
        cart_id=int(request.form["cart_id"]),
        product_id=int(request.form["product_id"])
    ))
    return render_template("cart.html", cart=output)
