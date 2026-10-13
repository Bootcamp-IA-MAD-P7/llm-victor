from fastapi.testclient import TestClient

from app.catalog import parse_catalog
from app.config import Settings
from app.main import create_app


def make_client(text_models: str | None = None) -> TestClient:
    settings = Settings(cors_origins="http://localhost:5173")
    if text_models is not None:
        settings = Settings(cors_origins="http://localhost:5173", text_models=text_models)
    return TestClient(create_app(settings))


def test_parse_catalog_reads_id_and_label() -> None:
    models = parse_catalog("llama-3.1-8b-instant|Llama 3.1 8B Instant, llama-3.3-70b|Llama 3.3 70B")

    assert [(model.id, model.label) for model in models] == [
        ("llama-3.1-8b-instant", "Llama 3.1 8B Instant"),
        ("llama-3.3-70b", "Llama 3.3 70B"),
    ]


def test_parse_catalog_falls_back_to_id_without_label() -> None:
    models = parse_catalog("llama-3.1-8b-instant")

    assert len(models) == 1
    assert models[0].id == "llama-3.1-8b-instant"
    assert models[0].label == "llama-3.1-8b-instant"


def test_parse_catalog_ignores_blank_entries() -> None:
    assert parse_catalog("  ,  , ") == []


def test_models_returns_configured_catalog() -> None:
    response = make_client("llama-3.1-8b-instant|Llama 3.1 8B Instant,only-id").get("/models")

    assert response.status_code == 200
    assert response.json() == {
        "models": [
            {"id": "llama-3.1-8b-instant", "label": "Llama 3.1 8B Instant"},
            {"id": "only-id", "label": "only-id"},
        ]
    }


def test_models_exposes_no_secrets() -> None:
    response = make_client("llama-3.1-8b-instant|Llama 3.1 8B Instant").get("/models")

    assert response.status_code == 200
    for model in response.json()["models"]:
        assert set(model) == {"id", "label"}
    assert "key" not in response.text.lower()


def test_models_returns_default_catalog() -> None:
    response = make_client().get("/models")

    assert response.status_code == 200
    assert response.json()["models"][0]["id"] == "llama-3.1-8b-instant"
