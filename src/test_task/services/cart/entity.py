from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.test_task.persistence.models.cart import CartModel, CartItemModel


@dataclass
class CartItemEntity:
    cart_item: CartItemModel

    @property
    def total_price(self) -> Decimal:
        return self.cart_item.product.price * self.cart_item.quantity


@dataclass
class CartEntity:
    cart: CartModel
    cart_items: List[CartItemEntity]

    @property
    def total_price(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.cart_items:
            total += item.total_price
        return total
