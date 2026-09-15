from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


def reset_settings(monkeypatch, **env):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    get_settings.cache_clear()


def test_webhook_rejects_wrong_secret(monkeypatch):
    reset_settings(monkeypatch, TELEGRAM_WEBHOOK_SECRET="secret")
    with TestClient(app) as client:
        response = client.post("/telegram/webhook", json={}, headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"})
    assert response.status_code == 403


def test_webhook_accepts_correct_secret(monkeypatch):
    reset_settings(monkeypatch, TELEGRAM_WEBHOOK_SECRET="secret")
    with TestClient(app) as client:
        response = client.post("/telegram/webhook", json={}, headers={"X-Telegram-Bot-Api-Secret-Token": "secret"})
    assert response.status_code == 200


def test_mutation_route_requires_demo_api_key(monkeypatch):
    reset_settings(monkeypatch, DEMO_API_KEY="secret")
    with TestClient(app) as client:
        response = client.post("/users", json={"display_name": "Alex"})
    assert response.status_code == 403


def test_mutation_route_accepts_demo_api_key(monkeypatch):
    reset_settings(monkeypatch, DEMO_API_KEY="secret")
    with TestClient(app) as client:
        response = client.post("/users", json={"display_name": "Alex"}, headers={"X-API-Key": "secret"})
    assert response.status_code == 200
