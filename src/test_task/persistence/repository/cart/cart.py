import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.test_task.persistence.models.cart import CartModel
from src.test_task.persistence.repository.abc import CartRepositoryABC, SomeModel


class CartRepository(
    CartRepositoryABC[CartModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cart_id: int) -> t.Optional[CartModel]:
        cart = self.db.execute(
            select(CartModel)
            .options(selectinload(CartModel.cart_items))
            .where(CartModel.id == cart_id)
        )
        return cart.scalar_one_or_none()

    def list(self) -> list[CartModel]:
        cart = self.db.execute(select(CartModel))
        return list(cart.scalars().all())

    def save(self, owner_id: int | None, owner_cookie: int | None) -> SomeModel:
        cart = CartModel(
            owner_id=owner_id,
            owner_cookie=owner_cookie,
        )
        self.db.add(cart)
        self.db.flush()
        return cart

    def update(self, cart_id: int, owner_id: int, owner_cookie: int) -> SomeModel:
        cart = self.db.get(CartModel, cart_id)
        if not cart:
            raise ValueError("Cart doesnt exist")

        cart.owner_id = owner_id
        cart.owner_cookie = owner_cookie

        self.db.flush()
        return cart

    def delete(self, index: int) -> bool:
        cart = self.db.get(CartModel, index)
        if not cart:
            raise ValueError("Cart doesnt exist")

        self.db.delete(cart)
        return True

    def get_by_owner_cookie(self, owner_cookie: int) -> t.Optional[CartModel]:
        cart = self.db.execute(
            select(CartModel)
            .options(selectinload(CartModel.cart_items))
            .where(CartModel.owner_cookie == owner_cookie)
        )
        return cart.scalar_one_or_none()

    def get_by_owner_id(self, owner_id: int) -> t.Optional[CartModel]:
        cart = self.db.execute(
            select(CartModel)
            .options(selectinload(CartModel.cart_items))
            .where(CartModel.owner_id == owner_id)
        )
        return cart.scalar_one_or_none()
