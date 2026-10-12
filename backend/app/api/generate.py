"""Generate endpoint."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from ..workflows.generate_direct import Audience, Tone, generate_direct

router = APIRouter()


class GenerateRequest(BaseModel):
    brief: str = Field(..., min_length=1)
    audience: Audience
    tone: Tone

    @field_validator("brief")
    @classmethod
    def reject_blank_brief(cls, value: str) -> str:
        brief = value.strip()
        if not brief:
            raise ValueError("brief must not be blank")
        return brief


class GenerateResponse(BaseModel):
    text: str
    provider: str
    model: str


@router.post("/generate", response_model=GenerateResponse)
async def generate_post(req: GenerateRequest) -> GenerateResponse:
    try:
        result = generate_direct(
            brief=req.brief,
            audience=req.audience,
            tone=req.tone,
        )
        return GenerateResponse(
            text=result.get("text", ""),
            provider=result.get("provider", "groq"),
            model=result.get("model", "unknown"),
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Generation failed") from exc
