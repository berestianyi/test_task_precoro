import typing as t

from flask_login import login_user

from src.test_task.persistence.uow.user import UserUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.user.hash import PasswordHasher
from src.test_task.services.user.login.ports import LoginInput, LoginSuccessfulOutput


class LoginService(ServiceABC[LoginInput, LoginSuccessfulOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], UserUoW],
            hasher: PasswordHasher
    ):
        self._uow_factory = uow_factory
        self._hasher = hasher

    def execute(self, login_input: LoginInput) -> LoginSuccessfulOutput:
        with self._uow_factory() as uow:
            user = uow.user_repo.get_by_email(email=login_input.email)
            if not user:
                raise ValueError("User not found")

            is_password_correct = self._hasher.verify(
                password=login_input.password,
                hashed=user.hashed_password
            )

            if not is_password_correct:
                raise ValueError("Invalid password")

            login_user(user, remember=True)

            return LoginSuccessfulOutput(user=user)
