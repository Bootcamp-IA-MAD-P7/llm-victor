"""Endpoint del catálogo de modelos."""

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Request
from pydantic import BaseModel

from ..catalog import Model, parse_catalog
from ..config import Settings

router = APIRouter()


class ModelsResponse(BaseModel):
    models: list[Model]


@router.get("/models", response_model=ModelsResponse)
def list_models(request: Request) -> ModelsResponse:
    settings = cast(Settings, request.app.state.settings)
    return ModelsResponse(models=parse_catalog(settings.text_models))
