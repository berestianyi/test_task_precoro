from contextlib import AbstractContextManager

from sqlalchemy.orm import Session

from src.test_task.persistence.repository.abc import CartRepositoryABC, CartItemRepositoryABC, ProductRepositoryABC


class CartUoW(AbstractContextManager):
    def __init__(self, session_factory, cart_repo, cart_item_repo, product_repo):
        self._session_factory = session_factory

        self._cart_repo = cart_repo
        self._cart_item_repo = cart_item_repo
        self._product_repo = product_repo

        self.db: Session | None = None

        self.cart_repo: CartRepositoryABC | None = None
        self.cart_item_repo: CartItemRepositoryABC | None = None
        self.product_repo:  ProductRepositoryABC | None = None



    def __enter__(self):
        self.db = self._session_factory()
        self.cart_repo = self._cart_repo(self.db)
        self.cart_item_repo = self._cart_item_repo(self.db)
        self.product_repo = self._product_repo(self.db)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.db.commit()
            else:
                self.db.rollback()
        finally:
            self.db.close()
