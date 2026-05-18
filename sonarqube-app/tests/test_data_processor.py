"""Unit tests for data_processor.py — ensures ≥80 % coverage for quality gate."""

import pytest

from src.data_processor import (
    calculate_hash,
    normalize_email,
    normalize_username,
    process_data,
    safe_risky_call,
    get_db_password,
)


# ── process_data ───────────────────────────────────────────────────────────────
class TestProcessData:
    def test_basic_split(self):
        assert process_data("a,b,c") == ["a", "b", "c"]

    def test_strips_whitespace(self):
        assert process_data(" a , b , c ") == ["a", "b", "c"]

    def test_single_value(self):
        assert process_data("only") == ["only"]

    def test_raises_on_none(self):
        with pytest.raises(ValueError, match="None"):
            process_data(None)  # type: ignore[arg-type]

    def test_raises_on_wrong_type(self):
        with pytest.raises(ValueError, match="Expected str"):
            process_data(123)  # type: ignore[arg-type]


# ── calculate_hash ─────────────────────────────────────────────────────────────
class TestCalculateHash:
    def test_known_hash(self):
        digest = calculate_hash("hello")
        assert digest == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    def test_returns_64_chars(self):
        assert len(calculate_hash("test")) == 64

    def test_raises_on_empty(self):
        with pytest.raises(ValueError, match="empty"):
            calculate_hash("")

    def test_different_inputs_differ(self):
        assert calculate_hash("abc") != calculate_hash("xyz")


# ── normalize helpers ──────────────────────────────────────────────────────────
class TestNormalize:
    def test_username_lowercased(self):
        assert normalize_username("  Alice  ") == "alice"

    def test_email_lowercased(self):
        assert normalize_email("  Bob@Example.COM  ") == "bob@example.com"


# ── safe_risky_call ────────────────────────────────────────────────────────────
class TestSafeRiskyCall:
    def test_returns_false_on_failure(self):
        # risky_operation always raises NotImplementedError
        result = safe_risky_call()
        assert result is False


# ── get_db_password ────────────────────────────────────────────────────────────
class TestGetDbPassword:
    def test_returns_env_value(self, monkeypatch):
        monkeypatch.setenv("DB_PASSWORD", "supersecret")
        assert get_db_password() == "supersecret"

    def test_raises_when_missing(self, monkeypatch):
        monkeypatch.delenv("DB_PASSWORD", raising=False)
        with pytest.raises(RuntimeError, match="DB_PASSWORD"):
            get_db_password()
