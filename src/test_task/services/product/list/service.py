import typing as t

from src.test_task.persistence.uow.product import ProductUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.product.list.ports import ProductListSuccessfulOutput, ProductListInput


class ProductListService(ServiceABC[ProductListInput, ProductListSuccessfulOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], ProductUoW],
    ):
        self._uow_factory = uow_factory

    def execute(self, product_list_input: ProductListInput) -> ProductListSuccessfulOutput:
        with self._uow_factory() as uow:
            products = uow.product_repo.list()

            return ProductListSuccessfulOutput(product_list=products)
