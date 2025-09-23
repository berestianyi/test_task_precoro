from src.test_task.persistence.models import UserModel
from src.test_task.services.abc import Input, SuccessfulOutput


class LoginInput(Input):
    owner_cookie: int
    email: str
    password: str


class LoginOutput(SuccessfulOutput):
    user: UserModel