from decimal import Decimal
from typing import List

from pydantic import BaseModel


class OrderItemDTO(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    purchase_price: Decimal
    total_price: Decimal



class OrderDTO(BaseModel):
    id: int
    user_id: int | None
    order_items: List[OrderItemDTO]
    total_price: Decimal
