from decimal import Decimal

from sqlalchemy import Integer, String, DECIMAL, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, TimeMixin


class ProductModel(TimeMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    cart_items: Mapped[list["CartItemModel"]] = relationship(
        back_populates="product"
    )