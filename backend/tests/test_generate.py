from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.api import generate as generate_module
from app.config import Settings
from app.main import create_app


def make_client() -> TestClient:
    return TestClient(create_app(Settings(cors_origins="http://localhost:5173")))


@pytest.mark.parametrize("payload", [{"brief": ""}, {"brief": "   "}, {}])
def test_generate_rejects_missing_or_blank_brief(payload: dict[str, Any]) -> None:
    response = make_client().post("/generate", json=payload)

    assert response.status_code == 422


def test_generate_does_not_run_workflow_for_blank_brief(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        nonlocal called
        called = True
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post("/generate", json={"brief": "   "})

    assert response.status_code == 422
    assert called is False


def test_generate_trims_brief_before_generating(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(*, brief: str, **kwargs: Any) -> dict[str, str]:
        captured["brief"] = brief
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post("/generate", json={"brief": "  hola  "})

    assert response.status_code == 200
    assert captured["brief"] == "hola"


def test_generate_reports_provider_failure_without_leaking_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        raise RuntimeError("groq rejected the secret api key")

    monkeypatch.setattr(generate_module, "generate_direct", failing_generate_direct)

    response = make_client().post("/generate", json={"brief": "hola"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Generation failed"}
    assert "secret" not in response.text
