from sqlalchemy import Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimeMixin, Base



class CartModel(TimeMixin, Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_cookie: Mapped[int | None] = mapped_column(BigInteger, unique=True)

    owner_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["UserModel | None"] = relationship(back_populates="carts", passive_deletes=True)

    cart_items: Mapped[list["CartItemModel"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin",
        passive_deletes=True
    )

class CartItemModel(Base):
    __tablename__ = "cart_items"

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.id"),
        primary_key=True
    )
    product: Mapped["ProductModel"] = relationship()

    cart_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True
    )
    cart: Mapped["CartModel"] = relationship(back_populates="cart_items")

