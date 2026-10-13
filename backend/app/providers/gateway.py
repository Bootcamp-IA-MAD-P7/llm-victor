"""Gateway that falls back to a secondary text provider on eligible failures."""

from __future__ import annotations

from typing import Protocol

from .groq import ModelUnavailableError

FALLBACK_ELIGIBLE_STATUS_CODES = {429}


class TextProvider(Protocol):
    """A text provider that can generate content from a prompt."""

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]: ...


def _status_code(exc: Exception) -> int | None:
    """HTTP status of a provider error, if it has one."""
    status = getattr(exc, "status_code", None)
    if status is None:
        response = getattr(exc, "response", None)
        status = getattr(response, "status_code", None)
    return status if isinstance(status, int) else None


def is_fallback_eligible(exc: Exception) -> bool:
    """Whether a primary-provider failure should trigger the fallback.

    Eligible: the provider is unreachable (no HTTP status), rate-limits the
    request (429) or fails on its side (5xx). Not eligible: request validation
    or authentication errors (other 4xx) and a model the provider no longer
    offers, which keeps its own response.
    """
    if isinstance(exc, ModelUnavailableError):
        return False
    status = _status_code(exc)
    if status is None:
        return True
    return status in FALLBACK_ELIGIBLE_STATUS_CODES or status >= 500


class TextProviderGateway:
    """Tries the primary provider and, on eligible failures, the fallback once."""

    def __init__(self, primary: TextProvider, fallback: TextProvider) -> None:
        self.primary = primary
        self.fallback = fallback

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        try:
            return self.primary.generate_text(prompt, model=model)
        except Exception as exc:
            if not is_fallback_eligible(exc):
                raise
            return self.fallback.generate_text(prompt)
