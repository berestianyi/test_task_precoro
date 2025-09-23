
from decimal import Decimal

from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: int
    name: str
    price: Decimal
    quantity: int
