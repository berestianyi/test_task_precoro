from dependency_injector.wiring import Provide, inject
from flask import render_template, Blueprint

from src.test_task.application import ServiceContainer
from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR
from src.test_task.services.product.list.ports import ProductListInput
from src.test_task.services.product.list.service import ProductListService



product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    template_folder=str(TEMPLATES_DIR),
)


@product_bp.route("/list", methods=["GET"])
@inject
def product_list(
        product_service: ProductListService = Provide[ServiceContainer.product_service],
):
    products = product_service.execute(ProductListInput())
    return render_template("products.html", products=products)
