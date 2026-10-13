"""Generate endpoint."""

from typing import cast

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from ..catalog import parse_catalog
from ..config import Settings
from ..providers.gateway import TextProviderGateway
from ..providers.groq import GroqProvider, ModelUnavailableError
from ..providers.openrouter import OpenRouterProvider
from ..workflows.generate_direct import Audience, Language, Tone, generate_direct

router = APIRouter()


class GenerateRequest(BaseModel):
    brief: str = Field(..., min_length=1)
    audience: Audience
    tone: Tone
    language: Language
    model: str = Field(..., min_length=1)
    context: str | None = None

    @field_validator("brief")
    @classmethod
    def reject_blank_brief(cls, value: str) -> str:
        brief = value.strip()
        if not brief:
            raise ValueError("brief must not be blank")
        return brief

    @field_validator("context")
    @classmethod
    def normalize_context(cls, value: str | None) -> str | None:
        if value is None:
            return None
        context = value.strip()
        return context or None


class GenerateResponse(BaseModel):
    text: str
    provider: str
    model: str


@router.post("/generate", response_model=GenerateResponse)
async def generate_post(req: GenerateRequest, request: Request) -> GenerateResponse:
    settings = cast(Settings, request.app.state.settings)
    catalog_ids = {model.id for model in parse_catalog(settings.text_models)}
    if req.model not in catalog_ids:
        raise HTTPException(status_code=422, detail="Unknown model")

    try:
        provider = TextProviderGateway(
            primary=GroqProvider(api_key=settings.groq_api_key or None),
            fallback=OpenRouterProvider(
                api_key=settings.openrouter_api_key or None,
                model=settings.openrouter_model,
            ),
        )
        result = generate_direct(
            brief=req.brief,
            audience=req.audience,
            tone=req.tone,
            language=req.language,
            model=req.model,
            context=req.context,
            provider=provider,
        )
        return GenerateResponse(
            text=result.get("text", ""),
            provider=result.get("provider", "groq"),
            model=result.get("model", "unknown"),
        )
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=409, detail="Selected model is not available") from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Generation failed") from exc
