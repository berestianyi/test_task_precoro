import typing as t

from flask_login import login_user

from src.test_task.persistence.uow.user import UserUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.user.hash import PasswordHasher
from src.test_task.services.user.register.ports import RegisterInput, RegisterOutput
from src.test_task.services.user.uuid import UuidIntGenerator


class RegisterService(ServiceABC[RegisterInput, RegisterOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], UserUoW],
            user_hasher: PasswordHasher,
            user_id_generator: UuidIntGenerator,
    ):
        self._uow_factory = uow_factory
        self._user_hasher = user_hasher
        self._id_generator = user_id_generator

    def execute(self, register_input: RegisterInput) -> RegisterOutput:
        with self._uow_factory() as uow:
            is_user_exist = uow.user_repo.get_by_email(register_input.email)
            if is_user_exist:
                raise ValueError("User already exist")

            cart = None
            if register_input.owner_cookie:
                cart = uow.cart_repo.get_by_owner_cookie(register_input.owner_cookie)

            user = uow.user_repo.save(
                user_id=register_input.owner_cookie,
                email=register_input.email,
                hashed_password=self._user_hasher.hash(password=register_input.password)
            )

            if cart:
                uow.cart_repo.update(
                    cart_id=cart.id,
                    owner_id=user.id,
                    owner_cookie=None
                )

            login_user(user, remember=True)

            return RegisterOutput(user=user)
