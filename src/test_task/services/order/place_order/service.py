import typing as t

from src.test_task.persistence.uow.order import OrderUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.cart.entity import CartEntity, CartItemEntity
from src.test_task.services.order.place_order.ports import PlaceOrderOutput, PlaceOrderInput


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

            cart_entity = CartEntity(
                cart=cart,
                cart_items=[
                    CartItemEntity(cart_item=item) for item in cart.cart_items
                ]
            )

            order = uow.order_repo.save(user_id=service_input.user_id, total_price=cart_entity.total_price)
            for cart_item_entity in cart_entity.cart_items:
                uow.order_item_repo.save(
                    order_id=order.id,
                    product_id=cart_item_entity.cart_item.product.id,
                    quantity=cart_item_entity.cart_item.quantity,
                    purchase_price=cart_item_entity.cart_item.product.price,
                    total_price=cart_item_entity.total_price
                )

                product = uow.product_repo.get_by_id(cart_item_entity.cart_item.product.id)
                uow.product_repo.update(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=product.quantity - cart_item_entity.cart_item.quantity
                )

            uow.cart_repo.delete(cart.id)
            orders = uow.order_repo.get_by_user_id(user_id=service_input.user_id)
            return PlaceOrderOutput(order=orders)
