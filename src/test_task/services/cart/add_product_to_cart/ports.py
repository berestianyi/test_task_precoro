from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.cart.entity import CartEntity


class AddProductToCartInput(Input):
    owner_id: int | None
    owner_cookie: int | None
    cart_id: int | None
    product_id: int


class AddProductToCartSuccessfulOutput(SuccessfulOutput):
    cart: CartEntity
