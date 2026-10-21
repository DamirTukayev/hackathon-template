"""Минимальный retrieval без внешних зависимостей (поиск по пересечению слов).

Достаточно, чтобы показать RAG на демо за 5 минут. Когда будет время — замените
`retrieve` на эмбеддинги + векторную БД (Chroma / pgvector / Qdrant), интерфейс
останется тем же: query -> список текстовых фрагментов.
"""

import re
from functools import lru_cache
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parents[1] / "data" / "knowledge"


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"\w+", text.lower()) if len(w) > 2}


@lru_cache
def _chunks() -> list[tuple[str, set[str]]]:
    chunks: list[tuple[str, set[str]]] = []
    for path in KNOWLEDGE_DIR.glob("*.md"):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            block = block.strip()
            if block and not block.startswith("#"):
                chunks.append((block, _tokens(block)))
    return chunks


def retrieve(query: str, k: int = 3) -> list[str]:
    q = _tokens(query)
    scored = [(len(q & toks), text) for text, toks in _chunks()]
    return [text for score, text in sorted(scored, reverse=True)[:k] if score > 0]
