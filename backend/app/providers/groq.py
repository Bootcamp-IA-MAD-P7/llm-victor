"""Groq provider client."""

from __future__ import annotations

import os

MODEL_UNAVAILABLE_STATUS_CODES = {400, 404}

MODEL_UNAVAILABLE_MARKERS = (
    "model_not_found",
    "model_decommissioned",
    "decommission",
    "not found",
    "does not exist",
    "no longer",
)


class ModelUnavailableError(Exception):
    """The provider no longer offers the requested model."""

    def __init__(self, model: str) -> None:
        self.model = model
        super().__init__(f"model {model} is not available")


def _is_model_unavailable(exc: Exception) -> bool:
    """Whether a provider error means the requested model is gone."""
    status = getattr(exc, "status_code", None)
    if status is None:
        status = getattr(getattr(exc, "response", None), "status_code", None)
    if status not in MODEL_UNAVAILABLE_STATUS_CODES:
        return False
    text = f"{exc} {getattr(exc, 'body', '')}".lower()
    return any(marker in text for marker in MODEL_UNAVAILABLE_MARKERS)


class GroqProvider:
    """Minimal Groq provider wrapper."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        """Generate text using Groq API.

        Returns dict with text, provider, model. Without an API key it returns a
        deterministic stub for local development and tests; a real call failure
        propagates so the API can report it.
        """
        model_name = str(model or os.getenv("DEFAULT_MODEL_GROQ", "openai/gpt-oss-120b"))

        if not self.api_key:
            return {
                "text": f"[STUB-GROQ] {prompt}",
                "provider": "groq",
                "model": str(model_name),
            }

        from groq import Groq

        client = Groq(api_key=self.api_key)
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
        except Exception as exc:
            if _is_model_unavailable(exc):
                raise ModelUnavailableError(model_name) from exc
            raise
        text = completion.choices[0].message.content or ""
        return {"text": text, "provider": "groq", "model": str(model_name)}
