import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.test_task.persistence.models import UserModel
from src.test_task.persistence.repository.abc import UserRepositoryABC, SomeModel


class UserRepository(
    UserRepositoryABC[UserModel]
):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> t.Optional[UserModel]:
        result = self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()


    def list(self) -> list[UserModel]:
        result = self.db.execute(select(UserModel))
        return list(result.scalars().all())

    def save(self, user_id: int | None, email: str, hashed_password: str) -> UserModel:
        user = UserModel(
            id=user_id,
            email=email,
            hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, user_id: int, email: str, hashed_password: str) -> UserModel:

        user = self.db.get(UserModel,  user_id)

        if not user:
            raise ValueError("User doesnt exist")

        user.email = user.email
        user.hashed_password = user.hashed_password

        self.db.flush()
        return user

    def delete(self, index: int) -> bool:
        user = self.db.get(UserModel, index)
        if not user:
            raise ValueError("User doesn't exist")

        self.db.delete(user)
        return True

    def get_by_email(self, email: str) -> t.Optional[UserModel]:
        result = self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()
