import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Клиент в офлайн-режиме: только mock-провайдер, без сети и ключей."""
    monkeypatch.setenv("DEMO_MODE", "true")

    from app.ai import router as ai_router
    from app.core.config import get_settings

    get_settings.cache_clear()
    ai_router._REGISTRY.clear()

    from app.main import app

    with TestClient(app) as c:
        yield c

    get_settings.cache_clear()
    ai_router._REGISTRY.clear()
