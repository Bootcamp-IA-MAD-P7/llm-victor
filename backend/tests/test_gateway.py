import pytest

from app.providers.gateway import TextProviderGateway, is_fallback_eligible
from app.providers.groq import ModelUnavailableError


class ProviderError(Exception):
    """Provider error with the status code the classifier inspects."""

    def __init__(self, status_code: int | None) -> None:
        self.status_code = status_code
        super().__init__(f"provider error {status_code}")


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (429, True),
        (500, True),
        (503, True),
        (None, True),
        (400, False),
        (401, False),
        (403, False),
        (404, False),
    ],
)
def test_is_fallback_eligible_by_status(status_code: int | None, expected: bool) -> None:
    assert is_fallback_eligible(ProviderError(status_code)) is expected


def test_model_unavailable_is_not_fallback_eligible() -> None:
    assert is_fallback_eligible(ModelUnavailableError("llama-3.1-8b-instant")) is False


class RecordingProvider:
    """Provider that records calls and can fail with a given error."""

    def __init__(
        self, result: dict[str, str] | None = None, error: Exception | None = None
    ) -> None:
        self.result = result or {"text": "ok", "provider": "fake", "model": "fake"}
        self.error = error
        self.calls: list[tuple[str, str | None]] = []

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        self.calls.append((prompt, model))
        if self.error is not None:
            raise self.error
        return self.result


def test_gateway_returns_primary_result_without_fallback() -> None:
    primary = RecordingProvider(result={"text": "groq", "provider": "groq", "model": "m"})
    fallback = RecordingProvider()

    result = TextProviderGateway(primary, fallback).generate_text("hola", model="m")

    assert result["provider"] == "groq"
    assert fallback.calls == []


def test_gateway_falls_back_on_eligible_failure_without_model() -> None:
    primary = RecordingProvider(error=ProviderError(429))
    fallback = RecordingProvider(
        result={"text": "or", "provider": "openrouter", "model": "or-model"}
    )

    result = TextProviderGateway(primary, fallback).generate_text("hola", model="groq-model")

    assert result == {"text": "or", "provider": "openrouter", "model": "or-model"}
    assert primary.calls == [("hola", "groq-model")]
    assert fallback.calls == [("hola", None)]


def test_gateway_does_not_fall_back_on_validation_error() -> None:
    primary = RecordingProvider(error=ProviderError(400))
    fallback = RecordingProvider()

    with pytest.raises(ProviderError):
        TextProviderGateway(primary, fallback).generate_text("hola", model="m")

    assert fallback.calls == []


def test_gateway_does_not_fall_back_on_model_unavailable() -> None:
    primary = RecordingProvider(error=ModelUnavailableError("m"))
    fallback = RecordingProvider()

    with pytest.raises(ModelUnavailableError):
        TextProviderGateway(primary, fallback).generate_text("hola", model="m")

    assert fallback.calls == []


def test_gateway_propagates_when_both_providers_fail() -> None:
    primary = RecordingProvider(error=ProviderError(500))
    fallback = RecordingProvider(error=ProviderError(503))

    with pytest.raises(ProviderError):
        TextProviderGateway(primary, fallback).generate_text("hola", model="m")

    assert primary.calls == [("hola", "m")]
    assert fallback.calls == [("hola", None)]
