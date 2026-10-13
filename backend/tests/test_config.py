import pytest

from app.config import Settings


@pytest.fixture(autouse=True)
def _isolate_model_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("TEXT_MODELS", "OPENROUTER_MODELS", "QDRANT_URL", "QDRANT_API_KEY"):
        monkeypatch.delenv(name, raising=False)


def test_settings_default_openrouter_models_are_free() -> None:
    models = [entry.split("|")[0] for entry in Settings().openrouter_models.split(",")]

    assert models
    assert all(model.endswith(":free") for model in models)


def test_settings_read_openrouter_models_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_MODELS", "custom/model:free|Custom")

    assert Settings().openrouter_models == "custom/model:free|Custom"


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
