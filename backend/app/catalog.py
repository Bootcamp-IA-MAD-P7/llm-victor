"""Catálogo de modelos de texto que la API publica."""

from __future__ import annotations

from typing import Literal, NamedTuple

from pydantic import BaseModel

Provider = Literal["groq", "openrouter"]


class Model(BaseModel):
    """Un modelo de texto disponible, sin detalles internos del proveedor."""

    id: str
    label: str


def parse_catalog(raw: str) -> list[Model]:
    """Convierte `id|label,id|label` en la lista del catálogo.

    Las entradas sin etiqueta usan el identificador como etiqueta y las
    entradas vacías se ignoran.
    """
    models: list[Model] = []
    for entry in raw.split(","):
        model_id, _, label = entry.strip().partition("|")
        model_id = model_id.strip()
        if not model_id:
            continue
        models.append(Model(id=model_id, label=label.strip() or model_id))
    return models


class CatalogEntry(NamedTuple):
    """Un modelo del catálogo y el proveedor que lo sirve."""

    model: Model
    provider: Provider


def build_catalog(groq_models: str, openrouter_models: str) -> list[CatalogEntry]:
    """Une los catálogos de Groq y OpenRouter, en ese orden.

    Si un identificador aparece en ambos, se queda el de Groq.
    """
    entries = [CatalogEntry(model, "groq") for model in parse_catalog(groq_models)]
    seen = {entry.model.id for entry in entries}
    entries += [
        CatalogEntry(model, "openrouter")
        for model in parse_catalog(openrouter_models)
        if model.id not in seen
    ]
    return entries
