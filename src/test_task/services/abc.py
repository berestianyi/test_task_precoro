import typing as t
from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict


class Input(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class SuccessfulOutput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


SomeInput = t.TypeVar("SomeInput", bound=Input)
SomeOutput = t.TypeVar(
    "SomeOutput",
    bound=SuccessfulOutput,
)


class ServiceABC(ABC, t.Generic[SomeInput, SomeOutput]):
    @abstractmethod
    async def execute(self, some_input: SomeInput) -> SomeOutput:
        raise NotImplementedError("Usecase.execute() must be implemented")
