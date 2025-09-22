from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, DECIMAL, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimeMixin



class OrderModel(TimeMixin,Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    total_price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    user: Mapped["UserModel"] = relationship(back_populates="orders")

    order_items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
        passive_deletes=True,
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    purchase_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.id"),
        primary_key=True
    )
    product: Mapped["ProductModel"] = relationship()

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True,
    )
    order: Mapped["OrderModel"] = relationship(back_populates="order_items")