import uuid
from abc import ABC, abstractmethod


class IdGenerator(ABC):
    @abstractmethod
    def generate(self) -> int:
        pass


class UuidIntGenerator(IdGenerator):

    def generate(self) -> int:
        return uuid.uuid4().int & ((1 << 63) - 1)
