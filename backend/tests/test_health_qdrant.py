from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.api import health as health_module
from app.api.health import check_qdrant, get_qdrant_check
from app.config import Settings
from app.main import create_app

SECRET = "super-secret-key"


def make_client(available: bool) -> TestClient:
    app = create_app(Settings(qdrant_url="https://qdrant.example.com", qdrant_api_key=SECRET))

    async def fake_check(settings: Settings) -> bool:
        return available

    app.dependency_overrides[get_qdrant_check] = lambda: fake_check
    return TestClient(app)


def test_reports_qdrant_available() -> None:
    response = make_client(available=True).get("/health/qdrant")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reports_qdrant_unavailable_without_leaking_details() -> None:
    response = make_client(available=False).get("/health/qdrant")

    assert response.status_code == 503
    assert response.json() == {"detail": "Qdrant is not available"}
    assert SECRET not in response.text
    assert "qdrant.example.com" not in response.text


def test_general_health_does_not_depend_on_qdrant() -> None:
    response = make_client(available=False).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class FakeClient:
    instances: list["FakeClient"] = []

    def __init__(self, *, fail: bool, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.fail = fail
        self.closed = False
        FakeClient.instances.append(self)

    async def get_collections(self) -> object:
        if self.fail:
            raise ConnectionError(f"cannot reach {self.kwargs['url']}")
        return object()

    async def close(self) -> None:
        self.closed = True


@pytest.fixture
def fake_client() -> type[FakeClient]:
    FakeClient.instances = []
    return FakeClient


async def run_check(
    monkeypatch: pytest.MonkeyPatch, fake_client: type[FakeClient], *, fail: bool, key: str
) -> bool:
    monkeypatch.setattr(
        health_module, "AsyncQdrantClient", lambda **kwargs: fake_client(fail=fail, **kwargs)
    )
    return await check_qdrant(Settings(qdrant_url="http://qdrant.test:6333", qdrant_api_key=key))


@pytest.mark.anyio
async def test_check_uses_configured_connection(
    monkeypatch: pytest.MonkeyPatch, fake_client: type[FakeClient]
) -> None:
    assert await run_check(monkeypatch, fake_client, fail=False, key=SECRET)

    [client] = fake_client.instances
    assert client.kwargs["url"] == "http://qdrant.test:6333"
    assert client.kwargs["api_key"] == SECRET
    assert client.closed


@pytest.mark.anyio
async def test_check_without_key_sends_none(
    monkeypatch: pytest.MonkeyPatch, fake_client: type[FakeClient]
) -> None:
    assert await run_check(monkeypatch, fake_client, fail=False, key="")

    assert fake_client.instances[0].kwargs["api_key"] is None


@pytest.mark.anyio
async def test_check_reports_unavailable_when_client_fails(
    monkeypatch: pytest.MonkeyPatch, fake_client: type[FakeClient]
) -> None:
    assert not await run_check(monkeypatch, fake_client, fail=True, key=SECRET)

    assert fake_client.instances[0].closed


@pytest.mark.anyio
async def test_check_reports_unavailable_for_invalid_url(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(**kwargs: Any) -> None:
        raise ValueError("bad url")

    monkeypatch.setattr(health_module, "AsyncQdrantClient", broken)

    assert not await check_qdrant(Settings(qdrant_url="not a url"))
