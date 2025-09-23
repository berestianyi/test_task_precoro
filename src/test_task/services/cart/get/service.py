import typing as t

from src.test_task.persistence.models.cart import CartModel
from src.test_task.persistence.uow.cart import CartUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.cart.dto import CartDTO, CartItemDTO
from src.test_task.services.cart.get.ports import GetCartOutput, GetCartInput
from src.test_task.services.product.dto import ProductDTO


class GetCartService(ServiceABC[GetCartInput, GetCartOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], CartUoW],

    ):
        self._uow_factory = uow_factory

    @staticmethod
    def _get_cart(uow, owner_id: int | None, owner_cookie: str | None) -> t.Optional[CartModel]:
        if owner_id is not None:
            cart = uow.cart_repo.get_by_owner_id(owner_id)
            if cart:
                return cart
        elif owner_cookie is not None:
            cart = uow.cart_repo.get_by_owner_cookie(owner_cookie)
            if cart:
                return cart
        return None

    def execute(self, service_input: GetCartInput) -> GetCartOutput:
        with self._uow_factory() as uow:
            cart = self._get_cart(uow, service_input.owner_id, service_input.owner_cookie)

            if cart:
                return GetCartOutput(cart=CartDTO(
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

            return GetCartOutput(cart=None)
