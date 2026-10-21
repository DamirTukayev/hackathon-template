from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

from app.core.config import get_settings
from app.schemas.chat import Message


class AnthropicProvider:
    name = "anthropic"

    def __init__(self) -> None:
        s = get_settings()
        self._s = s
        self._client = AsyncAnthropic(api_key=s.anthropic_api_key) if s.anthropic_api_key else None

    @property
    def available(self) -> bool:
        return self._client is not None

    async def stream(self, messages: list[Message], system: str) -> AsyncIterator[str]:
        assert self._client
        async with self._client.messages.stream(
            model=self._s.anthropic_model,
            max_tokens=self._s.max_tokens,
            system=system,
            messages=[m.model_dump() for m in messages],
        ) as stream:
            async for text in stream.text_stream:
                yield text
