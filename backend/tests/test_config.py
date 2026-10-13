import pytest

from app.config import Settings


@pytest.fixture(autouse=True)
def _isolate_model_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("OPENROUTER_MODEL", "QDRANT_URL", "QDRANT_API_KEY"):
        monkeypatch.delenv(name, raising=False)


def test_settings_use_default_openrouter_model() -> None:
    assert Settings().openrouter_model == "meta-llama/llama-3.1-8b-instruct"


def test_settings_read_openrouter_model_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_MODEL", "custom/model")

    assert Settings().openrouter_model == "custom/model"


def test_settings_use_local_qdrant_without_key_by_default() -> None:
    settings = Settings()

    assert settings.qdrant_url == "http://localhost:6333"
    assert settings.qdrant_api_key == ""


def test_settings_read_qdrant_connection_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("QDRANT_URL", "https://qdrant.example.com:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "secret")

    settings = Settings()

    assert settings.qdrant_url == "https://qdrant.example.com:6333"
    assert settings.qdrant_api_key == "secret"
