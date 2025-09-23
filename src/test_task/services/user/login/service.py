import typing as t

from flask_login import login_user

from src.test_task.persistence.uow.user import UserUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.user.hash import PasswordHasher
from src.test_task.services.user.login.ports import LoginInput, LoginOutput


class LoginService(ServiceABC[LoginInput, LoginOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], UserUoW],
            user_hasher: PasswordHasher,
    ):
        self._uow_factory = uow_factory
        self._user_hasher = user_hasher

    def execute(self, login_input: LoginInput) -> LoginOutput:
        with self._uow_factory() as uow:
            user = uow.user_repo.get_by_email(email=login_input.email)
            if not user:
                raise ValueError("User not found")
            is_password_correct = self._user_hasher.verify(
                password=login_input.password,
                hashed=user.hashed_password
            )

            if not is_password_correct:
                raise ValueError("Invalid password")

            cart = uow.cart_repo.get_by_owner_cookie(login_input.owner_cookie)
            if cart:
                uow.cart_repo.update(cart.id, owner_id=user.id, owner_cookie=None)

            login_user(user, remember=True)

            return LoginOutput(user=user)
