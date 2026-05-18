# Code Issue Fixes — Task 4 Documentation

Tài liệu này ghi lại **7 issues** được SonarQube phát hiện và cách sửa từng issue (before → after).

---

## Issue 1 — Bug: Possible `NoneType` error

| | Code |
|---|---|
| **Before** | `result = data.split(",")` — không kiểm tra `data is None` |
| **After** | Guard clause: `if data is None: raise ValueError(...)` |
| **Severity** | 🔴 Bug |
| **Rule** | `python:S2259` — Null dereference |

```python
# BEFORE
def process_data(data):
    result = data.split(",")   # crash if data is None
    return result

# AFTER
def process_data(data: str) -> list[str]:
    if data is None:
        raise ValueError("data must not be None")
    if not isinstance(data, str):
        raise ValueError(f"Expected str, got {type(data).__name__}")
    return [token.strip() for token in data.split(",")]
```

---

## Issue 2 — Vulnerability: Hardcoded password

| | Code |
|---|---|
| **Before** | `password = "admin123"` — hardcoded credential trong source code |
| **After** | Đọc từ environment variable `DB_PASSWORD` |
| **Severity** | 🔴 Vulnerability |
| **Rule** | `python:S2068` — Credentials should not be hard-coded |

```python
# BEFORE
password = "admin123"

# AFTER
def get_db_password() -> str:
    password = os.environ.get("DB_PASSWORD")
    if not password:
        raise RuntimeError("DB_PASSWORD environment variable is not set")
    return password
```

---

## Issue 3 — Code Smell: Bare `except` clause

| | Code |
|---|---|
| **Before** | `except: pass` — bắt mọi exception kể cả `SystemExit` |
| **After** | `except Exception as exc:` với logging |
| **Severity** | 🟡 Code Smell |
| **Rule** | `python:S5754` — Bare except |

```python
# BEFORE
try:
    risky_operation()
except:
    pass

# AFTER
try:
    risky_operation()
    return True
except Exception as exc:
    logger.warning("risky_operation failed: %s", exc)
    return False
```

---

## Issue 4 — Bug: Inconsistent return type (implicit `None`)

| | Code |
|---|---|
| **Before** | `calculate_hash` không raise khi `value` rỗng → trả về empty digest |
| **After** | Raise `ValueError` rõ ràng khi input rỗng |
| **Severity** | 🔴 Bug |
| **Rule** | `python:S1168` — Return empty collection instead of null |

```python
# BEFORE
def calculate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()  # empty string → weak

# AFTER
def calculate_hash(value: str) -> str:
    if not value:
        raise ValueError("value must not be empty")
    return hashlib.sha256(value.encode()).hexdigest()
```

---

## Issue 5 — Code Smell: Duplicated logic

| | Code |
|---|---|
| **Before** | `normalize_username` và `normalize_email` đều lặp lại `.strip().lower()` |
| **After** | Refactor thành hàm helper `_normalize()` dùng chung |
| **Severity** | 🟡 Code Smell |
| **Rule** | `python:S4144` — Methods should not have identical implementations |

```python
# BEFORE
def normalize_username(username):
    return username.strip().lower()

def normalize_email(email):
    return email.strip().lower()

# AFTER
def _normalize(text: str) -> str:
    return text.strip().lower()

def normalize_username(username: str) -> str:
    return _normalize(username)

def normalize_email(email: str) -> str:
    return _normalize(email)
```

---

## Issue 6 — Code Smell: Missing type annotations

| | Code |
|---|---|
| **Before** | Không có type hints trên bất kỳ hàm nào |
| **After** | Đầy đủ type hints trên tất cả functions (`str`, `list[str]`, `bool`, etc.) |
| **Severity** | 🟡 Code Smell |
| **Rule** | `python:S5886` — Type annotations improve readability |

---

## Issue 7 — Code Smell: Missing docstrings

| | Code |
|---|---|
| **Before** | Không có docstring cho module hay functions |
| **After** | Docstring đầy đủ (Args, Returns, Raises) theo Google style |
| **Severity** | 🟡 Code Smell |
| **Rule** | `python:S1602` — Missing docstrings |

---

## Tổng kết

| # | Loại | Rule | Severity | Trạng thái |
|---|------|------|----------|------------|
| 1 | Bug | `S2259` NullType dereference | 🔴 Critical | ✅ Fixed |
| 2 | Vulnerability | `S2068` Hardcoded credentials | 🔴 Critical | ✅ Fixed |
| 3 | Code Smell | `S5754` Bare except | 🟡 Major | ✅ Fixed |
| 4 | Bug | `S1168` Implicit None return | 🔴 Major | ✅ Fixed |
| 5 | Code Smell | `S4144` Duplicated logic | 🟡 Minor | ✅ Fixed |
| 6 | Code Smell | `S5886` Missing type hints | 🟡 Minor | ✅ Fixed |
| 7 | Code Smell | `S1602` Missing docstrings | 🟡 Info | ✅ Fixed |
