from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

ALLOWED_ORIGIN = "http://localhost:5173"


def make_client() -> TestClient:
    return TestClient(create_app(Settings(cors_origins=ALLOWED_ORIGIN)))


def test_health_reports_ok() -> None:
    response = make_client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_configured_origin() -> None:
    response = make_client().get("/health", headers={"Origin": ALLOWED_ORIGIN})

    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_cors_rejects_unknown_origin() -> None:
    response = make_client().get("/health", headers={"Origin": "http://evil.example"})

    assert "access-control-allow-origin" not in response.headers


def test_settings_split_comma_separated_origins() -> None:
    settings = Settings(cors_origins="http://a.test, http://b.test,")

    assert settings.cors_origin_list == ["http://a.test", "http://b.test"]
