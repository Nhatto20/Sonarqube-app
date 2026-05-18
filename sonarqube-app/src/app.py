"""FastAPI application entry-point for the SonarQube demo project."""

from fastapi import FastAPI

from .data_processor import (
    calculate_hash,
    normalize_email,
    normalize_username,
    process_data,
    safe_risky_call,
)

app = FastAPI(title="SonarQube Demo App:", version="1.0.0")


@app.get("/health")
def health() -> dict:
    """Liveness probe endpoint."""
    return {"status": "healthy"}


@app.get("/api/ping")
def ping() -> dict:
    """Simple connectivity check."""
    return {"message": "pong"}


@app.get("/api/version")
def version() -> dict:
    """Return application metadata."""
    return {"name": "sonarqube-app", "version": "1.0.0"}


@app.get("/api/process")
def api_process(data: str = "a,b,c") -> dict:
    """Split a CSV string and return the tokens."""
    return {"tokens": process_data(data)}


@app.get("/api/hash")
def api_hash(value: str) -> dict:
    """Return SHA-256 hash of a string."""
    return {"hash": calculate_hash(value)}


@app.get("/api/normalize")
def api_normalize(username: str, email: str) -> dict:
    """Normalize username and email."""
    return {
        "username": normalize_username(username),
        "email": normalize_email(email),
    }


@app.get("/api/risky")
def api_risky() -> dict:
    """Demonstrate safe error handling."""
    success = safe_risky_call()
    return {"success": success}
