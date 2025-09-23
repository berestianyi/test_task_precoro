import typing as t

from abc import ABC, abstractmethod
from decimal import Decimal

SomeModel = t.TypeVar(
    "SomeModel",
)


class ReaderABC(t.Generic[SomeModel], ABC):
    @abstractmethod
    def list(self) -> list[SomeModel]:
        pass

    @abstractmethod
    def get_by_id(self, index: int) -> t.Optional[SomeModel]:
        pass


class DeleterABC(ABC):
    @abstractmethod
    def delete(self, index: int) -> bool:
        pass


class UserRepositoryABC(
    ReaderABC[SomeModel],
    DeleterABC,
    ABC
):
    @abstractmethod
    def save(self,  user_id: int, email: str, hashed_password: str) -> SomeModel:
        pass

    @abstractmethod
    def update(self, user_id: int, email: str, hashed_password: str) -> SomeModel:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> t.Optional[SomeModel]:
        pass


class ProductRepositoryABC(
    ReaderABC[SomeModel],
    DeleterABC,
    ABC
):
    @abstractmethod
    def save(self, name: str, price: Decimal, quantity: int) -> SomeModel:
        pass

    @abstractmethod
    def update(self, product_id: int, name: str, price: Decimal, quantity: int) -> SomeModel:
        pass


class OrderRepositoryABC(
    ReaderABC[SomeModel],
    DeleterABC,
    ABC
):

    @abstractmethod
    def save(self, user_id: int, total_price: Decimal) -> SomeModel:
        pass

    @abstractmethod
    def update(self, order_id, user_id: int, total_price: Decimal) -> SomeModel:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> t.List[SomeModel]:
        pass


class CartRepositoryABC(
    ReaderABC[SomeModel],
    DeleterABC,
    ABC
):

    @abstractmethod
    def save(self, owner_id: int | None, owner_cookie: int | None) -> SomeModel:
        pass

    @abstractmethod
    def update(self, cart_id: int, owner_id: int, owner_cookie: int) -> SomeModel:
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: int) -> t.Optional[SomeModel]:
        pass

    @abstractmethod
    def get_by_owner_cookie(self, owner_cookie: int) -> t.Optional[SomeModel]:
        pass


class CartItemRepositoryABC(t.Generic[SomeModel], ABC):

    @abstractmethod
    def save(self, cart_id: int, product_id: int, quantity: int) -> SomeModel:
        pass

    @abstractmethod
    def update(self, cart_id: int, product_id: int, quantity: int) -> SomeModel:
        pass

    @abstractmethod
    def get_by_cart_id(self, cart_id: int) -> t.List[SomeModel]:
        pass

    @abstractmethod
    def delete(self, cart_id: int, product_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_ids(self, cart_id: int, product_id: int) -> SomeModel:
        pass

class OrderItemRepositoryABC(t.Generic[SomeModel], ABC):

    @abstractmethod
    def save(self, order_id: int, product_id: int, quantity: int, purchase_price: Decimal, total_price: Decimal) -> SomeModel:
        pass

    @abstractmethod
    def update(self, order_id: int, product_id: int, quantity: int, purchase_price: Decimal, total_price: Decimal) -> SomeModel:
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: int) -> t.List[SomeModel]:
        pass
