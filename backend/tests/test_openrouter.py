from typing import Any

import httpx
import pytest

from app.providers.openrouter import OpenRouterProvider


@pytest.fixture(autouse=True)
def _clear_openrouter_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_BASE_URL", raising=False)


def test_openrouter_returns_stub_without_api_key() -> None:
    provider = OpenRouterProvider()

    result = provider.generate_text("hola")

    assert result["provider"] == "openrouter"
    assert result["model"] == "nvidia/nemotron-3-super-120b-a12b:free"
    assert result["text"] == "[STUB-OPENROUTER] hola"


def test_openrouter_honours_explicit_model_override() -> None:
    provider = OpenRouterProvider()

    result = provider.generate_text("hola", model="custom/model")

    assert result["model"] == "custom/model"


def test_openrouter_stub_uses_configured_model() -> None:
    provider = OpenRouterProvider(models=["configured/model"])

    result = provider.generate_text("hola")

    assert result["model"] == "configured/model"


class FakeResponse:
    """Minimal httpx.Response stand-in."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._payload


def test_openrouter_calls_chat_completions_with_configured_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_post(url: str, **kwargs: Any) -> FakeResponse:
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse({"choices": [{"message": {"content": "hola mundo"}}]})

    monkeypatch.setattr(httpx, "post", fake_post)

    provider = OpenRouterProvider(api_key="secret", models=["custom/model"])
    result = provider.generate_text("pregunta")

    assert result == {"text": "hola mundo", "provider": "openrouter", "model": "custom/model"}
    assert captured["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["json"]["model"] == "custom/model"
    assert captured["json"]["messages"] == [{"role": "user", "content": "pregunta"}]
    assert "models" not in captured["json"]


def test_openrouter_sends_models_in_order_and_reports_effective_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_post(url: str, **kwargs: Any) -> FakeResponse:
        captured.update(kwargs)
        return FakeResponse({"model": "c", "choices": [{"message": {"content": "hola"}}]})

    monkeypatch.setattr(httpx, "post", fake_post)

    result = OpenRouterProvider(api_key="secret", models=["a", "b", "c"]).generate_text(
        "pregunta", model="b"
    )

    assert captured["json"]["model"] == "b"
    assert captured["json"]["models"] == ["b", "a", "c"]
    assert result["model"] == "c"
