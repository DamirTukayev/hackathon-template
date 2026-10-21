"""Оркестратор: пробует провайдеров по цепочке и стримит события наружу.

События (dict -> SSE):
  {"type": "meta", "provider": "anthropic"}
  {"type": "fallback", "from": "anthropic", "reason": "timeout"}
  {"type": "delta", "text": "..."}
  {"type": "done"}
  {"type": "error", "message": "..."}
"""

import asyncio
import logging
from collections.abc import AsyncIterator

from app.ai.base import Provider
from app.ai.prompts import build_system
from app.ai.providers.anthropic_ import AnthropicProvider
from app.ai.providers.mock import MockProvider
from app.ai.providers.openai_ import OpenAIProvider
from app.ai.rag import retrieve
from app.core.config import get_settings
from app.schemas.chat import Message

log = logging.getLogger("ai")

_REGISTRY: dict[str, Provider] = {}


def get_providers() -> dict[str, Provider]:
    if not _REGISTRY:
        for p in (AnthropicProvider(), OpenAIProvider(), MockProvider()):
            _REGISTRY[p.name] = p
    return _REGISTRY


async def _first_then_rest(gen: AsyncIterator[str], timeout: float) -> AsyncIterator[str]:
    """Ждём первый токен не дольше `timeout`, дальше отдаём поток как есть."""
    it = gen.__aiter__()
    first = await asyncio.wait_for(it.__anext__(), timeout)
    yield first
    async for chunk in it:
        yield chunk


async def stream_chat(messages: list[Message]) -> AsyncIterator[dict]:
    s = get_settings()
    providers = get_providers()
    last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
    system = build_system(retrieve(last_user))

    chain = [providers[n] for n in s.provider_order if n in providers and providers[n].available]
    for i, provider in enumerate(chain):
        started = False
        try:
            gen = _first_then_rest(provider.stream(messages, system), s.first_token_timeout)
            async for text in gen:
                if not started:
                    started = True
                    yield {"type": "meta", "provider": provider.name}
                yield {"type": "delta", "text": text}
            yield {"type": "done"}
            return
        except Exception as e:  # на хакатоне любая ошибка = переходим к следующему
            reason = "timeout" if isinstance(e, TimeoutError) else type(e).__name__
            log.warning("provider %s failed (%s): %s", provider.name, reason, e)
            if started:
                # Уже что-то показали пользователю — не мешаем ответы, сообщаем об обрыве.
                yield {"type": "error", "message": f"{provider.name}: stream interrupted"}
                return
            if i + 1 < len(chain):
                yield {"type": "fallback", "from": provider.name, "reason": reason}

    yield {"type": "error", "message": "No AI provider available"}
