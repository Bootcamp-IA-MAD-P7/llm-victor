"""OpenRouter provider client."""

from __future__ import annotations

import os
from collections.abc import Sequence

import httpx

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODELS = (
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "poolside/laguna-s-2.1:free",
)
REQUEST_TIMEOUT_SECONDS = 60.0


class OpenRouterProvider:
    """Minimal OpenRouter provider wrapper.

    OpenRouter exposes an OpenAI-compatible chat completions API. A single
    request sends the models in order and OpenRouter routes to the next one when
    a model fails or is rate-limited; the response reports the model that
    actually answered. Without an API key it returns a deterministic stub for
    local development and tests; a real call failure propagates so the API can
    report it.
    """

    def __init__(
        self,
        api_key: str | None = None,
        models: Sequence[str] | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.models = list(models or DEFAULT_MODELS)
        self.base_url = (base_url or os.getenv("OPENROUTER_BASE_URL") or DEFAULT_BASE_URL).rstrip(
            "/"
        )

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        """Generate text using OpenRouter API.

        An explicit `model` goes first and the configured models follow as its
        fallback; without one, the configured models are tried in order.
        Returns dict with text, provider and effective model.
        """
        models = [model, *(m for m in self.models if m != model)] if model else self.models
        model_name = models[0]

        if not self.api_key:
            return {
                "text": f"[STUB-OPENROUTER] {prompt}",
                "provider": "openrouter",
                "model": model_name,
            }

        payload: dict[str, object] = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        if len(models) > 1:
            payload["models"] = models

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"] or ""
        effective_model = str(data.get("model") or model_name)
        return {"text": text, "provider": "openrouter", "model": effective_model}
