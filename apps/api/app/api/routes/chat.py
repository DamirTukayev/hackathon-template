import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.ai.router import stream_chat
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/api", tags=["chat"])


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@router.post("/chat")
async def chat(body: ChatRequest, request: Request) -> StreamingResponse:
    async def gen() -> AsyncIterator[str]:
        async for event in stream_chat(body.messages):
            if await request.is_disconnected():  # пользователь нажал «Стоп»
                return
            yield _sse(event)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
