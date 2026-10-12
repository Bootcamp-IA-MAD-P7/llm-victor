"""Groq provider client."""

from __future__ import annotations

import os


class GroqProvider:
    """Minimal Groq provider wrapper."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        """Generate text using Groq API.

        Returns dict with text, provider, model.
        Falls back to simple stub if API key not configured (for dev/test).
        """
        model_name = model or os.getenv("DEFAULT_MODEL_GROQ", "llama-3.1-8b-instant")

        if not self.api_key:
            # Fallback stub for local development without key
            return {
                "text": f"[STUB-GROQ] {prompt}",
                "provider": "groq",
                "model": str(model_name),
            }

        try:
            from groq import Groq  # type: ignore[import-not-found]

            client = Groq(api_key=self.api_key)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            text = completion.choices[0].message.content or ""
            return {"text": text, "provider": "groq", "model": str(model_name)}
        except Exception:
            # If groq package not installed or call fails, return stub
            return {
                "text": f"[FALLBACK-STUB] {prompt}",
                "provider": "groq",
                "model": str(model_name),
            }
