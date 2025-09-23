import typing as t

from src.test_task.persistence.models.cart import CartModel
from src.test_task.persistence.uow.cart import CartUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.cart.delete_cart_item_from_cart.ports import DeleteProductFromCartInput, \
    DeleteProductFromCartOutput
from src.test_task.services.cart.dto import CartDTO, CartItemDTO
from src.test_task.services.product.dto import ProductDTO


class DeleteProductFromCartService(ServiceABC[DeleteProductFromCartInput, DeleteProductFromCartOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], CartUoW],

    ):
        self._uow_factory = uow_factory

    @staticmethod
    def _get_cart(uow, owner_id: int | None, owner_cookie: str | None) -> CartModel:
        if owner_id:
            cart = uow.cart_repo.get_by_owner_id(owner_id)
            if cart:
                return cart
        elif owner_cookie:
            cart = uow.cart_repo.get_by_owner_cookie(owner_cookie)
            if cart:
                return cart
        raise Exception("User or guest does not exist")

    @staticmethod
    def _delete_cart_item(uow, cart_id: int, product_id: int):
        product = uow.product_repo.get_by_id(product_id=product_id)
        if not product:
            raise ValueError("Product not found")

        uow.cart_item_repo.delete(cart_id=cart_id, product_id=product.id)

    def execute(self, service_input: DeleteProductFromCartInput) -> DeleteProductFromCartOutput:
        with self._uow_factory() as uow:
            cart = self._get_cart(uow, service_input.owner_id, service_input.owner_cookie)
            self._delete_cart_item(uow, cart.id, service_input.product_id)

            cart = uow.cart_repo.get_by_id(cart.id)

            if cart.cart_items:
                return DeleteProductFromCartOutput(cart=CartDTO(
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
                ))

            return DeleteProductFromCartOutput(cart=None)
