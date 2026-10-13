"""OpenRouter provider client."""

from __future__ import annotations

import os

import httpx

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct"
REQUEST_TIMEOUT_SECONDS = 30.0


class OpenRouterProvider:
    """Minimal OpenRouter provider wrapper.

    OpenRouter exposes an OpenAI-compatible chat completions API. Without an
    API key it returns a deterministic stub for local development and tests; a
    real call failure propagates so the API can report it.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
        self.base_url = (base_url or os.getenv("OPENROUTER_BASE_URL") or DEFAULT_BASE_URL).rstrip(
            "/"
        )

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        """Generate text using OpenRouter API.

        Returns dict with text, provider, model.
        """
        model_name = str(model or self.model)

        if not self.api_key:
            return {
                "text": f"[STUB-OPENROUTER] {prompt}",
                "provider": "openrouter",
                "model": model_name,
            }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"] or ""
        return {"text": text, "provider": "openrouter", "model": model_name}
