import typing as t

from src.test_task.persistence.uow.order import OrderUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.order.list.ports import OrderListInput, OrderListOutput


class OrderListService(ServiceABC[OrderListInput, OrderListOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], OrderUoW],
    ):
        self._uow_factory = uow_factory

    def execute(self, service_input: OrderListInput) -> OrderListOutput:
        with self._uow_factory() as uow:
            orders = uow.order_repo.get_by_user_id(user_id=service_input.user_id)
            return OrderListOutput(order=orders)
