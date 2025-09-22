from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.test_task.persistence.repository.product import ProductRepository
from src.test_task.persistence.repository.user import UserRepository
from src.test_task.persistence.uow.product import ProductUoW
from src.test_task.persistence.uow.user import UserUoW
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
        user_repo_cls=UserRepository,
    )
    product_uow = providers.Factory(
        ProductUoW,
        session_factory=session_factory,
        user_repo_cls=ProductRepository,
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