from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.api import generate as generate_module
from app.config import Settings
from app.main import create_app
from app.providers.groq import GroqProvider, ModelUnavailableError, _is_model_unavailable
from app.workflows.generate_direct import (
    Audience,
    Language,
    Tone,
    generate_direct,
)

VALID_CONFIG: dict[str, str] = {
    "audience": "tech-professionals",
    "tone": "professional",
    "language": "es",
    "model": "llama-3.1-8b-instant",
}


def make_client() -> TestClient:
    return TestClient(create_app(Settings(cors_origins="http://localhost:5173")))


@pytest.mark.parametrize("brief", ["", "   "])
def test_generate_rejects_missing_or_blank_brief(brief: str) -> None:
    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": brief})

    assert response.status_code == 422


def test_generate_rejects_absent_brief() -> None:
    response = make_client().post("/generate", json=VALID_CONFIG)

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

    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "   "})

    assert response.status_code == 422
    assert called is False


@pytest.mark.parametrize(
    "config",
    [
        {**VALID_CONFIG, "audience": "unknown"},
        {**VALID_CONFIG, "tone": "unknown"},
        {**VALID_CONFIG, "language": "unknown"},
    ],
    ids=["audience", "tone", "language"],
)
def test_generate_rejects_invalid_audience_tone_or_language(config: dict[str, str]) -> None:
    response = make_client().post("/generate", json={**config, "brief": "hola"})

    assert response.status_code == 422


def test_generate_does_not_run_workflow_for_invalid_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        nonlocal called
        called = True
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "audience": "unknown"},
    )

    assert response.status_code == 422
    assert called is False


def test_generate_does_not_run_workflow_for_invalid_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        nonlocal called
        called = True
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "language": "unknown"},
    )

    assert response.status_code == 422
    assert called is False


@pytest.mark.parametrize("audience", [audience.value for audience in Audience])
@pytest.mark.parametrize("tone", [tone.value for tone in Tone])
def test_generate_accepts_allowed_options(audience: str, tone: str) -> None:
    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "audience": audience, "tone": tone},
    )

    assert response.status_code == 200


@pytest.mark.parametrize("language", [language.value for language in Language])
def test_generate_accepts_all_allowed_languages(language: str) -> None:
    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "language": language},
    )

    assert response.status_code == 200


def test_generate_trims_brief_before_generating(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(*, brief: str, **kwargs: Any) -> dict[str, str]:
        captured["brief"] = brief
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "  hola  "})

    assert response.status_code == 200
    assert captured["brief"] == "hola"


def test_generate_passes_audience_tone_and_language_to_workflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(
        *,
        brief: str,
        audience: Audience,
        tone: Tone,
        language: Language,
        **kwargs: Any,
    ) -> dict[str, str]:
        captured.update(
            brief=brief,
            audience=audience,
            tone=tone,
            language=language,
        )
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "hola"})

    assert response.status_code == 200
    assert captured["audience"] == Audience.TECH_PROFESSIONALS
    assert captured["tone"] == Tone.PROFESSIONAL
    assert captured["language"] == Language.SPANISH


def test_generate_reports_provider_failure_without_leaking_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        raise RuntimeError("groq rejected the secret api key")

    monkeypatch.setattr(generate_module, "generate_direct", failing_generate_direct)

    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "hola"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Generation failed"}
    assert "secret" not in response.text


def test_generate_rejects_absent_model() -> None:
    payload = {key: value for key, value in VALID_CONFIG.items() if key != "model"}

    response = make_client().post("/generate", json={**payload, "brief": "hola"})

    assert response.status_code == 422


def test_generate_rejects_model_not_in_catalog() -> None:
    response = make_client().post(
        "/generate", json={**VALID_CONFIG, "brief": "hola", "model": "not-in-catalog"}
    )

    assert response.status_code == 422


def test_generate_validates_against_configured_catalog() -> None:
    client = TestClient(
        create_app(
            Settings(
                cors_origins="http://localhost:5173",
                text_models="only-model|Only Model",
            )
        )
    )

    accepted = client.post(
        "/generate", json={**VALID_CONFIG, "brief": "hola", "model": "only-model"}
    )
    rejected = client.post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "model": "llama-3.1-8b-instant"},
    )

    assert accepted.status_code == 200
    assert rejected.status_code == 422


def test_generate_does_not_run_workflow_for_unknown_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        nonlocal called
        called = True
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post(
        "/generate", json={**VALID_CONFIG, "brief": "hola", "model": "not-in-catalog"}
    )

    assert response.status_code == 422
    assert called is False


def test_generate_passes_model_to_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(*, model: str, **kwargs: Any) -> dict[str, str]:
        captured["model"] = model
        return {"text": "ok", "provider": "groq", "model": model}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "model": "llama-3.1-8b-instant"},
    )

    assert response.status_code == 200
    assert captured["model"] == "llama-3.1-8b-instant"
    assert response.json()["model"] == "llama-3.1-8b-instant"


def test_generate_reports_model_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def unavailable_generate_direct(*args: Any, **kwargs: Any) -> dict[str, str]:
        raise ModelUnavailableError("llama-3.1-8b-instant")

    monkeypatch.setattr(generate_module, "generate_direct", unavailable_generate_direct)

    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "hola"})

    assert response.status_code == 409
    assert response.json() == {"detail": "Selected model is not available"}
    assert "secret" not in response.text


class FakeProviderError(Exception):
    """Provider error with the attributes the classifier inspects."""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(body)


@pytest.mark.parametrize(
    ("status_code", "body"),
    [
        (400, "model_not_found"),
        (404, "the requested model does not exist"),
        (400, "model_decommissioned"),
    ],
)
def test_is_model_unavailable_when_provider_reports_it(status_code: int, body: str) -> None:
    assert _is_model_unavailable(FakeProviderError(status_code, body)) is True


@pytest.mark.parametrize(
    ("status_code", "body"),
    [
        (400, "invalid api key"),
        (429, "rate limit exceeded"),
        (500, "the model server exploded"),
    ],
)
def test_is_model_unavailable_false_for_other_errors(status_code: int, body: str) -> None:
    assert _is_model_unavailable(FakeProviderError(status_code, body)) is False


class CapturingProvider(GroqProvider):
    """Provider that records the prompt and model it receives."""

    def __init__(self) -> None:
        super().__init__(api_key="test")
        self.prompts: list[str] = []
        self.models: list[str | None] = []

    def generate_text(self, prompt: str, model: str | None = None) -> dict[str, str]:
        self.prompts.append(prompt)
        self.models.append(model)
        return {"text": "ok", "provider": "groq", "model": str(model or "test")}


def test_generate_direct_builds_prompt_with_audience_and_tone() -> None:
    provider = CapturingProvider()

    generate_direct(
        brief="Sobre IA",
        audience=Audience.AI_SPECIALISTS,
        tone=Tone.INSPIRING,
        language=Language.SPANISH,
        provider=provider,
    )

    assert len(provider.prompts) == 1
    prompt = provider.prompts[0]
    assert "especialistas en IA" in prompt
    assert "inspirador" in prompt
    assert "Sobre IA" in prompt


def test_generate_direct_uses_selected_model() -> None:
    provider = CapturingProvider()

    result = generate_direct(
        brief="Sobre IA",
        audience=Audience.AI_SPECIALISTS,
        tone=Tone.INSPIRING,
        language=Language.SPANISH,
        model="llama-3.3-70b",
        provider=provider,
    )

    assert provider.models == ["llama-3.3-70b"]
    assert result["model"] == "llama-3.3-70b"


@pytest.mark.parametrize(
    ("language", "label"),
    [
        (Language.SPANISH, "español"),
        (Language.ENGLISH, "inglés"),
        (Language.FRENCH, "francés"),
        (Language.ITALIAN, "italiano"),
    ],
)
def test_generate_direct_builds_prompt_with_language_label(language: Language, label: str) -> None:
    provider = CapturingProvider()

    generate_direct(
        brief="Sobre IA",
        audience=Audience.AI_SPECIALISTS,
        tone=Tone.INSPIRING,
        language=language,
        provider=provider,
    )

    prompt = provider.prompts[0]
    assert f"Idioma de salida: {label}" in prompt
    assert prompt.index("Idioma de salida") < prompt.index("Briefing:")


def test_generate_accepts_request_without_context() -> None:
    response = make_client().post("/generate", json={**VALID_CONFIG, "brief": "hola"})

    assert response.status_code == 200


def test_generate_accepts_request_with_context() -> None:
    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "context": "dirigido a startups"},
    )

    assert response.status_code == 200


@pytest.mark.parametrize("context", [None, "", "   "])
def test_generate_normalizes_absent_context_to_none(
    context: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(*, context: str | None = None, **kwargs: Any) -> dict[str, str]:
        captured["context"] = context
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    payload: dict[str, str] = {**VALID_CONFIG, "brief": "hola"}
    if context is not None:
        payload["context"] = context

    response = make_client().post("/generate", json=payload)

    assert response.status_code == 200
    assert captured["context"] is None


def test_generate_passes_context_to_workflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_generate_direct(*, context: str | None = None, **kwargs: Any) -> dict[str, str]:
        captured["context"] = context
        return {"text": "ok", "provider": "groq", "model": "test"}

    monkeypatch.setattr(generate_module, "generate_direct", fake_generate_direct)

    response = make_client().post(
        "/generate",
        json={**VALID_CONFIG, "brief": "hola", "context": "  dirigido a startups  "},
    )

    assert response.status_code == 200
    assert captured["context"] == "dirigido a startups"


def test_generate_direct_builds_prompt_with_labelled_context() -> None:
    provider = CapturingProvider()

    generate_direct(
        brief="Sobre IA",
        audience=Audience.AI_SPECIALISTS,
        tone=Tone.INSPIRING,
        language=Language.SPANISH,
        context="Dirigido a startups",
        provider=provider,
    )

    prompt = provider.prompts[0]
    assert "Dirigido a startups" in prompt
    assert "Contexto adicional" in prompt
    assert prompt.index("Briefing:") < prompt.index("Contexto adicional")


def test_generate_direct_omits_context_block_without_context() -> None:
    provider = CapturingProvider()

    generate_direct(
        brief="Sobre IA",
        audience=Audience.AI_SPECIALISTS,
        tone=Tone.INSPIRING,
        language=Language.SPANISH,
        provider=provider,
    )

    assert "Contexto adicional" not in provider.prompts[0]
