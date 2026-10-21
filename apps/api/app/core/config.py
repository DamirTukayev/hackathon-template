from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    # Порядок фолбэка: если первый провайдер упал/завис — идём к следующему.
    # "mock" в конце гарантирует, что демо никогда не покажет ошибку.
    ai_providers: str = "anthropic,openai,mock"
    # DEMO_MODE=true -> только mock, без сети (страховка на сцене).
    demo_mode: bool = False
    # Сколько ждём ПЕРВЫЙ токен, прежде чем переключиться на следующий провайдер.
    first_token_timeout: float = 8.0

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5-5"

    # Любой OpenAI-совместимый эндпоинт: OpenAI, Ollama, vLLM, OpenRouter...
    openai_api_key: str = ""
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    max_tokens: int = 1024
    cors_origins: str = "http://localhost:5173"

    @property
    def provider_order(self) -> list[str]:
        if self.demo_mode:
            return ["mock"]
        return [p.strip() for p in self.ai_providers.split(",") if p.strip()]

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
