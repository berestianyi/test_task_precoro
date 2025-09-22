import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.test_task.persistence.models.cart import CartItemModel
from src.test_task.persistence.repository.abc import CartItemRepositoryABC, SomeModel


class CartItemRepository(
    CartItemRepositoryABC[CartItemModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_cart_id(self, cart_id: int) -> t.List[CartItemModel]:
        carts = self.db.execute(
            select(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        return list(carts.scalars().all())

    def save(self, cart_id: int, product_id: int, quantity: int) -> SomeModel:
        cart = CartItemModel(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.db.add(cart)
        self.db.flush()
        return cart

    def update(self, cart_id: int, product_id: int, quantity: int) -> SomeModel:
        cart = self.db.get(
            CartItemModel, {"cart_id": cart_id, "product_id": product_id}
        )
        if not cart:
            raise ValueError("CartItem doesnt exist")

        cart.quantity = quantity
        self.db.flush()
        return cart


    def delete(self, cart_id: int, product_id: int) -> bool:
        cart = self.db.get(
            CartItemModel, {"cart_id": cart_id, "product_id": product_id}
        )
        if not cart:
            raise ValueError("CartItem doesnt exist")

        self.db.delete(cart)
        return True