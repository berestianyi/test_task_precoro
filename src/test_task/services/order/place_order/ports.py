import typing as t
from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.order.dto import OrderDTO


class PlaceOrderInput(Input):
    user_id: int


class PlaceOrderOutput(SuccessfulOutput):
    order: t.List[OrderDTO]
