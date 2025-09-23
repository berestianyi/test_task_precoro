from src.test_task.persistence.models import UserModel
from src.test_task.services.abc import Input, SuccessfulOutput


class RegisterInput(Input):
    email: str
    password: str
    owner_cookie: int | None = None


class RegisterOutput(SuccessfulOutput):
    user: UserModel
