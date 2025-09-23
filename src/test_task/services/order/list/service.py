import typing as t

from src.test_task.persistence.uow.order import OrderUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.order.dto import OrderDTO, OrderItemDTO
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

            order_dto = [OrderDTO(
                id=order.id,
                user_id=order.user_id,
                total_price=order.total_price,
                order_items=[OrderItemDTO(
                    product_id=item.product_id,
                    order_id=item.order_id,
                    quantity=item.quantity,
                    purchase_price=item.purchase_price,
                    total_price=item.total_price
                ) for item in order.order_items]
            ) for order in orders]

            return OrderListOutput(order=order_dto)
