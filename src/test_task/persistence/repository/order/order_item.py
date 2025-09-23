import typing as t
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.test_task.persistence.models.order import OrderItemModel
from src.test_task.persistence.repository.abc import OrderItemRepositoryABC


class OrderItemRepository(
    OrderItemRepositoryABC[OrderItemModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_order_id(self, order_id: int) -> t.List[OrderItemModel]:
        order_items = self.db.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        return list(order_items.scalars().all())

    def save(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            purchase_price: Decimal,
            total_price: Decimal
    ) -> OrderItemModel:

        order_item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            purchase_price=purchase_price,
            total_price=total_price
        )
        self.db.add(order_item)
        self.db.flush()
        return order_item

    def update(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            purchase_price: Decimal,
            total_price: Decimal
    ) -> OrderItemModel:

        order_item = self.db.get(OrderItemModel, {"order_id": order_id, "product_id": product_id})
        if not order_item:
            raise ValueError("OrderItemModel doesnt exist")

        order_item.quantity = quantity
        order_item.purchase_price = purchase_price
        order_item.total_price = total_price

        self.db.flush()
        return order_item
