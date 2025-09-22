from abc import ABC, abstractmethod

import bcrypt


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass
    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        pass


class BcryptHasher(PasswordHasher):
    version = "bcrypt"

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())