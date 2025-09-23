from decimal import Decimal
from typing import List

from pydantic import BaseModel

from src.test_task.services.product.dto import ProductDTO


class CartItemDTO(BaseModel):
    product_id: int
    cart_id: int
    quantity: int
    available_quantity: int
    product: ProductDTO

    @property
    def total_price(self) -> Decimal:
        return self.product.price * self.quantity


class CartDTO(BaseModel):
    id: int
    owner_cookie: int | None
    owner_id: int | None
    cart_items: list[CartItemDTO]

    @property
    def total_price(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.cart_items:
            total += item.total_price
        return total