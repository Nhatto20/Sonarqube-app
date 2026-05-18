"""Tests for the FastAPI application endpoints."""

from fastapi.testclient import TestClient

# pyrefly: ignore [missing-import]
from src.app import app

client = TestClient(app)


# ── /health ────────────────────────────────────────────────────────────────────
def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_body():
    response = client.get("/health")
    assert response.json() == {"status": "healthy"}


# ── /api/ping ──────────────────────────────────────────────────────────────────
def test_ping_returns_pong():
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


# ── /api/version ───────────────────────────────────────────────────────────────
def test_version_returns_metadata():
    response = client.get("/api/version")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "sonarqube-app"
    assert "version" in data


# ── /api/process ───────────────────────────────────────────────────────────────
def test_process_default():
    response = client.get("/api/process")
    assert response.status_code == 200
    assert response.json() == {"tokens": ["a", "b", "c"]}


def test_process_custom_data():
    response = client.get("/api/process?data=x%2Cy%2Cz")
    assert response.status_code == 200
    assert response.json() == {"tokens": ["x", "y", "z"]}


# ── /api/hash ──────────────────────────────────────────────────────────────────
def test_hash_returns_hex_string():
    response = client.get("/api/hash?value=hello")
    assert response.status_code == 200
    h = response.json()["hash"]
    assert len(h) == 64  # SHA-256 hex digest
    assert h == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


# ── /api/normalize ─────────────────────────────────────────────────────────────
def test_normalize():
    response = client.get("/api/normalize?username=Alice&email=Alice%40Example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"


# ── /api/risky ─────────────────────────────────────────────────────────────────
def test_risky_returns_bool():
    response = client.get("/api/risky")
    assert response.status_code == 200
    assert "success" in response.json()
