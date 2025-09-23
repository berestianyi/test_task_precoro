import typing as t

from src.test_task.persistence.uow.order import OrderUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.cart.dto import CartDTO, CartItemDTO
from src.test_task.services.order.dto import OrderDTO, OrderItemDTO
from src.test_task.services.order.place_order.ports import PlaceOrderOutput, PlaceOrderInput
from src.test_task.services.product.dto import ProductDTO


class PlaceOrderService(ServiceABC[PlaceOrderInput, PlaceOrderOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], OrderUoW],
    ):
        self._uow_factory = uow_factory

    def execute(self, service_input: PlaceOrderInput) -> PlaceOrderOutput:
        with self._uow_factory() as uow:
            cart = uow.cart_repo.get_by_owner_id(owner_id=service_input.user_id)
            if not cart:
                raise ValueError("Cart is empty")

            cart_dto = CartDTO(
                id=cart.id,
                owner_cookie=cart.owner_cookie,
                owner_id=cart.owner_id,
                cart_items=[
                    CartItemDTO(
                        product_id=item.product_id,
                        cart_id=item.cart_id,
                        quantity=item.quantity,
                        available_quantity=item.product.quantity,
                        product=ProductDTO(
                            id=item.product.id,
                            name=item.product.name,
                            price=item.product.price,
                            quantity=item.product.quantity
                        )
                    ) for item in cart.cart_items
                ]
            )

            order = uow.order_repo.save(user_id=service_input.user_id, total_price=cart_dto.total_price)
            for cart_item_entity in cart_dto.cart_items:
                uow.order_item_repo.save(
                    order_id=order.id,
                    product_id=cart_item_entity.product_id,
                    quantity=cart_item_entity.quantity,
                    purchase_price=uow.product_repo.get_by_id(cart_item_entity.product_id).price,
                    total_price=cart_item_entity.total_price
                )

                product = uow.product_repo.get_by_id(cart_item_entity.product_id)
                uow.product_repo.update(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=product.quantity - cart_item_entity.quantity
                )

            uow.cart_repo.delete(cart.id)
            orders = uow.order_repo.get_by_user_id(user_id=service_input.user_id)

            order_dto = [
                OrderDTO(
                    id=order.id,
                    user_id=order.user_id,
                    total_price=order.total_price,
                    order_items=[
                        OrderItemDTO(
                            product_id=item.product_id,
                            order_id=item.order_id,
                            quantity=item.quantity,
                            purchase_price=item.purchase_price,
                            total_price=item.total_price
                        ) for item in order.order_items
                    ]
                )
                for order in orders
            ]

            return PlaceOrderOutput(order=order_dto)
