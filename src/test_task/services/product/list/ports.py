import typing as t
from src.test_task.persistence.models.product import ProductModel
from src.test_task.services.abc import Input, SuccessfulOutput


class ProductListInput(Input):
    pass


class ProductListSuccessfulOutput(SuccessfulOutput):
    product_list: t.List[ProductModel]