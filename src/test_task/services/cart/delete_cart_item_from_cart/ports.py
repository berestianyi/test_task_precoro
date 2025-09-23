from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.cart.entity import CartEntity


class DeleteProductFromCartInput(Input):
    owner_id: int | None
    owner_cookie: int | None
    cart_id: int
    product_id: int


class DeleteProductFromCartSuccessfulOutput(SuccessfulOutput):
    cart: CartEntity | None
