import typing as t
from src.test_task.services.abc import Input, SuccessfulOutput
from src.test_task.services.product.dto import ProductDTO


class ProductListInput(Input):
    pass


class ProductListOutput(SuccessfulOutput):
    product_list: t.List[ProductDTO]