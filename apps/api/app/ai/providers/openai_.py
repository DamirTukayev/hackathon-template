from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.chat import Message


class OpenAIProvider:
    """Работает с любым OpenAI-совместимым API (OpenAI, Ollama, vLLM, OpenRouter)."""

    name = "openai"

    def __init__(self) -> None:
        s = get_settings()
        self._s = s
        # Для локального Ollama ключ может быть любым непустым — задайте OPENAI_API_KEY=ollama
        self._client = (
            AsyncOpenAI(api_key=s.openai_api_key, base_url=s.openai_base_url)
            if s.openai_api_key
            else None
        )

    @property
    def available(self) -> bool:
        return self._client is not None

    async def stream(self, messages: list[Message], system: str) -> AsyncIterator[str]:
        assert self._client
        stream = await self._client.chat.completions.create(
            model=self._s.openai_model,
            max_tokens=self._s.max_tokens,
            stream=True,
            messages=[{"role": "system", "content": system}, *[m.model_dump() for m in messages]],
        )
        async for chunk in stream:
            if chunk.choices and (text := chunk.choices[0].delta.content):
                yield text
