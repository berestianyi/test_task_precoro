from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.test_task.persistence.repository.cart.cart import CartRepository
from src.test_task.persistence.repository.cart.cart_item import CartItemRepository
from src.test_task.persistence.repository.product import ProductRepository
from src.test_task.persistence.repository.user import UserRepository
from src.test_task.persistence.uow.cart import CartUoW
from src.test_task.persistence.uow.product import ProductUoW
from src.test_task.persistence.uow.user import UserUoW
from src.test_task.services.cart.add_product_to_cart.service import AddProductToCartService
from src.test_task.services.cart.delete_cart_item_from_cart.service import DeleteProductFromCartService
from src.test_task.services.cart.remove_product_from_cart.service import RemoveProductFromCartService
from src.test_task.services.product.list.service import ProductListService
from src.test_task.services.user.hash import BcryptHasher
from src.test_task.services.user.login.service import LoginService
from src.test_task.services.user.register.service import RegisterService
from src.test_task.services.user.uuid import UuidIntGenerator


def create_engine_sync(dsn: str):
    return create_engine(dsn, pool_pre_ping=True, future=True)


def create_sessionmaker_sync(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(create_engine_sync, dsn=config.db.dsn)
    session_factory = providers.Singleton(create_sessionmaker_sync, engine=engine)

    user_uow = providers.Factory(
        UserUoW,
        session_factory=session_factory,
        user_repo=UserRepository,
    )
    product_uow = providers.Factory(
        ProductUoW,
        session_factory=session_factory,
        product_repo=ProductRepository,
    )
    cart_uow = providers.Factory(
        CartUoW,
        session_factory=session_factory,
        cart_repo=CartRepository,
        cart_item_repo=CartItemRepository,
        product_repo=ProductRepository
    )

    user_hasher = providers.Factory(BcryptHasher)
    user_id_generator = providers.Factory(UuidIntGenerator)

    login_service = providers.Factory(
        LoginService,
        uow_factory=user_uow.provider,
        user_hasher=user_hasher,
    )
    register_service = providers.Factory(
        RegisterService,
        uow_factory=user_uow.provider,
        user_hasher=user_hasher,
        user_id_generator=user_id_generator,
    )
    product_service = providers.Factory(
        ProductListService,
        uow_factory=product_uow.provider,
    )
    add_product_to_cart_service = providers.Factory(
        AddProductToCartService,
        uow_factory=cart_uow.provider,
    )

    remove_product_from_cart_service = providers.Factory(
        RemoveProductFromCartService,
        uow_factory=cart_uow.provider,
    )

    delete_product_from_cart_service = providers.Factory(
        DeleteProductFromCartService,
        uow_factory=cart_uow.provider,
    )
