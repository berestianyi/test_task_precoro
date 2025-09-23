import typing as t

from src.test_task.persistence.uow.product import ProductUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.product.dto import ProductDTO
from src.test_task.services.product.list.ports import ProductListOutput, ProductListInput


class ProductListService(ServiceABC[ProductListInput, ProductListOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], ProductUoW],
    ):
        self._uow_factory = uow_factory

    def execute(self, product_list_input: ProductListInput) -> ProductListOutput:
        with self._uow_factory() as uow:
            products = uow.product_repo.list()
            products_entity_list = [ProductDTO(
                id=product.id,
                name=product.name,
                price=product.price,
                quantity=product.quantity
            ) for product in products]
            return ProductListOutput(product_list=products_entity_list)
