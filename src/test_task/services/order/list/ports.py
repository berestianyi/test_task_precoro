import typing as t
from src.test_task.persistence.models.order import OrderModel
from src.test_task.services.abc import Input, SuccessfulOutput


class OrderListInput(Input):
    user_id: int


class OrderListOutput(SuccessfulOutput):
    order: t.List[OrderModel]
