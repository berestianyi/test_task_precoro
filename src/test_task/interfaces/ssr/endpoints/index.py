from flask import Blueprint, url_for, redirect

from src.test_task.interfaces.ssr.endpoints import TEMPLATES_DIR


bp = Blueprint(
    "index",
    __name__,
    template_folder=str(TEMPLATES_DIR),
)

@bp.route("/")
def index():
    return redirect(url_for("product.product_list"))