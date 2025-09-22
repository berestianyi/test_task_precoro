from src.test_task.persistence.models import UserModel
from src.test_task.services.abc import Input, SuccessfulOutput


class LoginInput(Input):
    email: str
    password: str


class LoginSuccessfulOutput(SuccessfulOutput):
    user: UserModel