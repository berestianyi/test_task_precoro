import typing as t
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.test_task.persistence.models.product import ProductModel
from src.test_task.persistence.repository.abc import ProductRepositoryABC


class ProductRepository(
    ProductRepositoryABC[ProductModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int) -> t.Optional[ProductModel]:
        product = self.db.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        return product.scalar_one_or_none()

    def list(self) -> list[ProductModel]:
        products = self.db.execute(select(ProductModel))
        return list(products.scalars().all())

    def save(self, name: str, price: Decimal, quantity: int) -> ProductModel:
        product = ProductModel(
            name=name,
            price=price,
            quantity=quantity,
        )
        self.db.add(product)
        self.db.flush()
        return product

    def update(self, product_id: int, name: str, price: Decimal, quantity: int) -> ProductModel:
        product = self.db.get(ProductModel, product_id)
        if not product:
            raise ValueError("Product doesn't exist")

        product.name = name
        product.price = price
        product.quantity = quantity

        self.db.flush()
        return product

    def delete(self, index: int) -> bool:
        product = self.db.get(ProductModel, index)
        if not product:
            raise ValueError("Product doesn't exist")

        self.db.delete(product)
        return True