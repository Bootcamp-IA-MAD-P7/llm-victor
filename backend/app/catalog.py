"""Catálogo de modelos de texto que la API publica."""

from __future__ import annotations

from pydantic import BaseModel


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
