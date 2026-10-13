import pytest

from app.config import Settings


@pytest.fixture(autouse=True)
def _isolate_model_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)


def test_settings_use_default_openrouter_model() -> None:
    assert Settings().openrouter_model == "meta-llama/llama-3.1-8b-instruct"


def test_settings_read_openrouter_model_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_MODEL", "custom/model")

    assert Settings().openrouter_model == "custom/model"
