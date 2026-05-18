"""
data_processor.py
-----------------
This module demonstrates various code quality issues that SonarQube would flag.
Task 4: Code issues BEFORE fixes (preserved in git history via separate commit).
"""

import hashlib
import logging
import os

logger = logging.getLogger(__name__)


# ── FIXED version of process_data ─────────────────────────────────────────────
# Issue 1 (Bug): NoneType error when data is None → add guard clause
# Issue 2 (Security): hardcoded password removed → use env var
# Issue 3 (Code Smell): bare except replaced with specific Exception


def process_data(data: str) -> list[str]:
    """Split a CSV string into a list of trimmed values.

    Args:
        data: Comma-separated string. Must not be None.

    Returns:
        List of stripped string tokens.

    Raises:
        ValueError: If *data* is None or not a string.
    """
    if data is None:
        raise ValueError("data must not be None")
    if not isinstance(data, str):
        raise ValueError(f"Expected str, got {type(data).__name__}")

    return [token.strip() for token in data.split(",")]


# ── FIXED: credentials from environment, never hardcoded ──────────────────────
# Issue 4 (Vulnerability): hardcoded credentials
def get_db_password() -> str:
    """Retrieve the database password from the environment.

    Raises:
        RuntimeError: If DB_PASSWORD is not set.
    """
    password = os.environ.get("DB_PASSWORD")
    if not password:
        raise RuntimeError("DB_PASSWORD environment variable is not set")
    return password


# ── FIXED: specific exception catch ───────────────────────────────────────────
# Issue 5 (Code Smell): bare except clause
def risky_operation() -> None:
    """Simulate an operation that might fail."""
    raise NotImplementedError("Implement the actual risky logic here")


def safe_risky_call() -> bool:
    """Call risky_operation and handle failures gracefully.

    Returns:
        True if successful, False otherwise.
    """
    try:
        risky_operation()
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("risky_operation failed: %s", exc)
        return False


# ── FIXED: consistent return types ────────────────────────────────────────────
# Issue 6 (Bug): function sometimes returned None implicitly
def calculate_hash(value: str) -> str:
    """Return the SHA-256 hex digest of *value*.

    Args:
        value: Input string to hash.

    Returns:
        Lowercase hex digest string.

    Raises:
        ValueError: If *value* is empty.
    """
    if not value:
        raise ValueError("value must not be empty")
    return hashlib.sha256(value.encode()).hexdigest()


# ── FIXED: removed dead / duplicated code ─────────────────────────────────────
# Issue 7 (Code Smell): duplicate logic consolidated into one helper
def _normalize(text: str) -> str:
    return text.strip().lower()


def normalize_username(username: str) -> str:
    """Return a normalised username."""
    return _normalize(username)


def normalize_email(email: str) -> str:
    """Return a normalised e-mail address."""
    return _normalize(email)

print('ff')