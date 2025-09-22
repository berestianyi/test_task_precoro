import typing as t
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.test_task.persistence.models.order import OrderModel
from src.test_task.persistence.repository.abc import OrderRepositoryABC


class OrderRepository(
    OrderRepositoryABC[OrderModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: int) -> t.Optional[OrderModel]:
        order = self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.order_items))
            .where(OrderModel.id == order_id)
        )
        return order.scalar_one_or_none()

    def list(self) -> list[OrderModel]:
        orders = self.db.execute(select(OrderModel))
        return list(orders.scalars().all())

    def save(self, user_id: int, total_price: Decimal) -> OrderModel:

        order = OrderModel(
            user_id=user_id,
            total_price=total_price,
        )
        self.db.add(order)
        self.db.flush()
        return order

    def update(self, order_id, user_id: int, total_price: Decimal) -> OrderModel:

        order = self.db.get(OrderModel, order_id)

        if not order:
            raise ValueError("Order doesnt exist")

        order.user_id = user_id
        order.total_price = total_price

        self.db.flush()
        return order

    def delete(self, index: int) -> bool:
        orm = self.db.get(OrderModel, index)
        if not orm:
            raise ValueError("Order doesnt exist")

        self.db.delete(orm)
        return True

    def get_by_user_id(self, user_id: int) -> t.List[OrderModel]:
        orders = self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.order_items))
            .where(OrderModel.user_id == user_id)
        )
        return list(orders.scalars().all())
