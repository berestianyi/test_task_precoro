import typing as t

from src.test_task.persistence.models.cart import CartModel
from src.test_task.persistence.uow.cart import CartUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.cart.delete_cart_item_from_cart.ports import DeleteProductFromCartInput, \
    DeleteProductFromCartSuccessfulOutput
from src.test_task.services.cart.entity import CartEntity, CartItemEntity

from src.test_task.services.user.uuid import IdGenerator


class DeleteProductFromCartService(ServiceABC[DeleteProductFromCartInput, DeleteProductFromCartSuccessfulOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], CartUoW],
            uuid_generator: IdGenerator

    ):
        self._uow_factory = uow_factory
        self._uuid_generator = uuid_generator

    @staticmethod
    def _get_cart(uow, owner_id: int | None, owner_cookie: str | None) -> CartModel:
        if owner_id is not None:
            cart = uow.cart_repo.get_by_owner_id(owner_id)
            if cart:
                return cart
        elif owner_cookie is not None:
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

    def execute(self, service_input: DeleteProductFromCartInput) -> DeleteProductFromCartSuccessfulOutput:
        with self._uow_factory() as uow:
            cart = self._get_cart(uow, service_input.owner_id, service_input.owner_cookie)
            self._delete_cart_item(uow, cart.id, service_input.product_id)

            cart = uow.cart_repo.get_by_id(cart.id)

            if cart.cart_items:
                return DeleteProductFromCartSuccessfulOutput(cart=CartEntity(
                    cart=cart,
                    cart_items=[
                        CartItemEntity(cart_item=item) for item in cart.cart_items
                    ]
                ))

            return DeleteProductFromCartSuccessfulOutput(cart=None)
