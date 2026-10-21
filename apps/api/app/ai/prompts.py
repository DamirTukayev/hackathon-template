SYSTEM_PROMPT = """Ты — ИИ-ассистент продукта для бизнес-партнёра хакатона.
Отвечай по-русски, кратко и по делу, используй Markdown (списки, **выделение**).
Если в контексте нет ответа — честно скажи об этом, не выдумывай факты."""


def build_system(context: list[str]) -> str:
    if not context:
        return SYSTEM_PROMPT
    joined = "\n\n".join(f"- {c}" for c in context)
    return f"{SYSTEM_PROMPT}\n\nКонтекст из базы знаний:\n{joined}"
