import asyncio
import json
import re
from collections.abc import AsyncIterator
from pathlib import Path

from app.schemas.chat import Message

CACHE_FILE = Path(__file__).resolve().parents[2] / "data" / "demo_cache.json"


def _load() -> list[dict]:
    return json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else []


class MockProvider:
    """Заготовленные ответы для демо. Выглядит как настоящий стрим, но не зависит от сети.

    Добавляйте свои сценарии демо в data/demo_cache.json:
    {"keywords": ["слово1", "слово2"], "answer": "готовый ответ"}
    """

    name = "mock"
    available = True

    def __init__(self, delay: float = 0.025) -> None:
        self._delay = delay
        self._cache = _load()

    def _pick(self, query: str) -> str:
        words = set(re.findall(r"\w+", query.lower()))
        best, score = None, 0
        for item in self._cache:
            q = query.lower()
            hits = sum(1 for k in item["keywords"] if k.lower() in words or k.lower() in q)
            if hits > score:
                best, score = item, hits
        if best:
            return best["answer"]
        return (
            "Это демо-ответ: внешняя модель сейчас недоступна, поэтому показан заранее "
            "подготовленный результат. Подставьте сюда реальный сценарий вашего продукта."
        )

    async def stream(self, messages: list[Message], system: str) -> AsyncIterator[str]:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        answer = self._pick(last_user)
        for token in re.findall(r"\S+\s*", answer):
            await asyncio.sleep(self._delay)
            yield token
