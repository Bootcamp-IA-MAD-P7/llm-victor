import logging
from collections.abc import Awaitable, Callable
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient

from ..config import Settings

router = APIRouter()
logger = logging.getLogger(__name__)

QDRANT_TIMEOUT_SECONDS = 3

QdrantCheck = Callable[[Settings], Awaitable[bool]]


class HealthResponse(BaseModel):
    status: Literal["ok"]


async def check_qdrant(settings: Settings) -> bool:
    """Return whether Qdrant answers with the configured URL and key."""
    try:
        client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key or None,
            timeout=QDRANT_TIMEOUT_SECONDS,
        )
    except Exception as exc:
        logger.warning("Invalid Qdrant configuration: %s: %s", type(exc).__name__, exc)
        return False
    try:
        await client.get_collections()
    except Exception as exc:
        logger.warning("Qdrant is not available: %s: %s", type(exc).__name__, exc)
        return False
    finally:
        await client.close()
    return True


def get_qdrant_check() -> QdrantCheck:
    return check_qdrant


@router.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/health/qdrant")
async def health_qdrant(
    request: Request, check: Annotated[QdrantCheck, Depends(get_qdrant_check)]
) -> HealthResponse:
    settings = cast(Settings, request.app.state.settings)
    if not await check(settings):
        raise HTTPException(status_code=503, detail="Qdrant is not available")
    return HealthResponse(status="ok")
