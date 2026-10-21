import json

import pytest
from fastapi.testclient import TestClient


def _events(raw: str) -> list[dict]:
    return [
        json.loads(line.removeprefix("data: "))
        for line in raw.splitlines()
        if line.startswith("data: ")
    ]


@pytest.fixture(autouse=True)
def fast_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    """Убираем искусственную задержку mock-стрима, чтобы тесты шли за миллисекунды."""
    import asyncio

    real_sleep = asyncio.sleep
    monkeypatch.setattr("app.ai.providers.mock.asyncio.sleep", lambda _d: real_sleep(0))


def test_chat_streams_sse_contract(client: TestClient) -> None:
    r = client.post("/api/chat", json={"messages": [{"role": "user", "content": "Привет"}]})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/event-stream")

    events = _events(r.text)
    types = [e["type"] for e in events]
    assert types[0] == "meta"
    assert events[0]["provider"] == "mock"
    assert types[-1] == "done"
    assert "delta" in types
    assert set(types) <= {"meta", "delta", "done"}

    text = "".join(e["text"] for e in events if e["type"] == "delta")
    assert text.strip()


@pytest.mark.parametrize(
    "payload",
    [
        {"messages": []},
        {"messages": [{"role": "user", "content": ""}]},
        {"messages": [{"role": "system", "content": "hi"}]},
        {},
    ],
)
def test_chat_rejects_invalid_payload(client: TestClient, payload: dict) -> None:
    assert client.post("/api/chat", json=payload).status_code == 422
