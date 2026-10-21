from collections.abc import AsyncIterator
from typing import Protocol

from app.schemas.chat import Message


class Provider(Protocol):
    name: str

    @property
    def available(self) -> bool: ...

    def stream(self, messages: list[Message], system: str) -> AsyncIterator[str]:
        """Отдаёт текст кусками по мере генерации."""
        ...
