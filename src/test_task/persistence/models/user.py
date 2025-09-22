from typing import List

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import TimeMixin, Base


class UserModel(TimeMixin, Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[List["OrderModel"]] = relationship(
        back_populates="user",
    )

    carts: Mapped[List["CartModel"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )