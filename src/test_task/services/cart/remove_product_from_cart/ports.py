from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.cart.dto import CartDTO


class RemoveProductFromCartInput(Input):
    owner_id: int | None
    owner_cookie: int | None
    cart_id: int
    product_id: int


class RemoveProductFromCartOutput(SuccessfulOutput):
    cart: CartDTO | None
