from fastapi import APIRouter

from app.ai.router import get_providers
from app.core.config import get_settings

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health() -> dict:
    s = get_settings()
    providers = get_providers()
    return {
        "status": "ok",
        "demo_mode": s.demo_mode,
        "providers": [n for n in s.provider_order if n in providers and providers[n].available],
    }
