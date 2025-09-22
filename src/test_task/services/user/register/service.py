import typing as t

from flask_login import login_user

from src.test_task.persistence.uow.user import UserUoW
from src.test_task.services.abc import ServiceABC
from src.test_task.services.user.hash import PasswordHasher
from src.test_task.services.user.register.ports import RegisterInput, RegisterSuccessfulOutput
from src.test_task.services.user.uuid import IdGenerator


class RegisterService(ServiceABC[RegisterInput, RegisterSuccessfulOutput]):

    def __init__(
            self,
            uow_factory: t.Callable[[], UserUoW],
            hasher: PasswordHasher,
            uuid_generator: IdGenerator
    ):
        self._uow_factory = uow_factory
        self._hasher = hasher
        self._uuid_generator = uuid_generator

    def execute(self, register_input: RegisterInput) -> RegisterSuccessfulOutput:
        with self._uow_factory() as uow:
            is_user_exist = uow.user_repo.get_by_email(register_input.email)
            if is_user_exist:
                raise ValueError("User already exist")

            user_id = None
            if register_input.owner_cookie:
                user_id = register_input.owner_cookie

            user = uow.user_repo.save(
                user_id=user_id,
                email=register_input.email,
                hashed_password=self._hasher.hash(password=register_input.password)
            )

            login_user(user, remember=True)

            return RegisterSuccessfulOutput(user=user)
