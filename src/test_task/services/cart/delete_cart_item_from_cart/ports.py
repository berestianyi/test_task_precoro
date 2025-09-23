from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.cart.dto import CartDTO


class DeleteProductFromCartInput(Input):
    owner_id: int | None
    owner_cookie: int | None
    cart_id: int
    product_id: int


class DeleteProductFromCartOutput(SuccessfulOutput):
    cart: CartDTO | None
