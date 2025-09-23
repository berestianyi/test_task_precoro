import typing as t
from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.order.dto import OrderDTO


class OrderListInput(Input):
    user_id: int


class OrderListOutput(SuccessfulOutput):
    order: t.List[OrderDTO]
