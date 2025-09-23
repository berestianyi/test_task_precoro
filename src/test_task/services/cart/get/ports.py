from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.cart.dto import CartDTO


class GetCartInput(Input):
    owner_id: int | None
    owner_cookie: int | None


class GetCartOutput(SuccessfulOutput):
    cart: CartDTO | None
