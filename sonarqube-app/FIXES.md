# Code Issue Fixes — Task 4 Documentation

Tài liệu này ghi lại **7 issues** (Bugs, Vulnerabilities, Code Smells) được cố tình đưa vào source code để SonarQube phân tích, và cách fix chúng để vượt qua Quality Gate.

Tất cả thay đổi đều nằm trong file `src/data_processor.py`.

---

## 1. Issue 1 — Bug: `NoneType` dereference (Crash)

Khi `data` truyền vào là `None`, lệnh `data.split(",")` sẽ gây crash ứng dụng (`AttributeError: 'NoneType' object has no attribute 'split'`).

| Item | Details |
|------|---------|
| **Severity** | 🔴 Critical / Bug |
| **Before** | Không kiểm tra `data` trước khi xử lý |
| **After** | Thêm "Guard clause" kiểm tra kiểu dữ liệu và raise exception rõ ràng |

**Before:**
```python
def process_data(data):
    result = data.split(",")
    return result
```

**After:**
```python
def process_data(data: str) -> list[str]:
    if data is None:
        raise ValueError("data must not be None")
    if not isinstance(data, str):
        raise ValueError(f"Expected str, got {type(data).__name__}")
    return [token.strip() for token in data.split(",")]
```

---

## 2. Issue 2 — Vulnerability: Hardcoded Password

Lưu trữ mật khẩu dạng plain text trực tiếp trong source code là lỗ hổng bảo mật nghiêm trọng (Hardcoded credentials).

| Item | Details |
|------|---------|
| **Severity** | 🔴 Critical / Vulnerability |
| **Before** | `password = "admin123"` |
| **After** | Lấy password từ biến môi trường (Environment Variable) |

**Before:**
```python
def get_db_password():
    password = "admin123"
    return password
```

**After:**
```python
def get_db_password() -> str:
    password = os.environ.get("DB_PASSWORD")
    if not password:
        raise RuntimeError("DB_PASSWORD environment variable is not set")
    return password
```

---

## 3. Issue 3 — Code Smell: Bare `except` clause

Bắt lỗi bằng `except:` (không chỉ định loại Exception) sẽ bắt toàn bộ các lỗi kể cả lỗi hệ thống (`SystemExit`, `KeyboardInterrupt`), làm ứng dụng khó debug.

| Item | Details |
|------|---------|
| **Severity** | 🟡 Major / Code Smell |
| **Before** | Dùng `except:` và `pass` |
| **After** | Bắt cụ thể `Exception` và có ghi log |

**Before:**
```python
def safe_risky_call():
    try:
        risky_operation()
        return True
    except:
        pass
```

**After:**
```python
def safe_risky_call() -> bool:
    try:
        risky_operation()
        return True
    except Exception as exc:
        logger.warning("risky_operation failed: %s", exc)
        return False
```

---

## 4. Issue 4 — Bug: Implicit `None` return

Hàm đôi khi không trả về giá trị (implicit return None) dẫn đến caller bị lỗi không lường trước được.

| Item | Details |
|------|---------|
| **Severity** | 🔴 Major / Bug |
| **Before** | Trả về hash nếu input tồn tại, nếu input rỗng thì hàm lẳng lặng trả về None |
| **After** | Bắt buộc input hợp lệ, nếu rỗng thì raise exception |

**Before:**
```python
def calculate_hash(value):
    if value:
        return hashlib.sha256(value.encode()).hexdigest()
    # Implicit return None
```

**After:**
```python
def calculate_hash(value: str) -> str:
    if not value:
        raise ValueError("value must not be empty")
    return hashlib.sha256(value.encode()).hexdigest()
```

---

## 5. Issue 5 — Code Smell: Duplicated Logic

Logic chuẩn hóa (strip whitespace + lower case) bị lặp lại ở nhiều nơi.

| Item | Details |
|------|---------|
| **Severity** | 🟡 Minor / Code Smell |
| **Before** | `normalize_username` và `normalize_email` đều gọi `.strip().lower()` |
| **After** | Trích xuất thành private helper function `_normalize()` |

**Before:**
```python
def normalize_username(username):
    return username.strip().lower()

def normalize_email(email):
    return email.strip().lower()
```

**After:**
```python
def _normalize(text: str) -> str:
    return text.strip().lower()

def normalize_username(username: str) -> str:
    return _normalize(username)

def normalize_email(email: str) -> str:
    return _normalize(email)
```

---

## 6. Issue 6 & 7 — Code Smell: Missing Types & Docstrings

Không có định nghĩa kiểu dữ liệu tĩnh và không có chú thích giải thích cho các function.

| Item | Details |
|------|---------|
| **Severity** | 🟡 Minor - Info / Code Smell |
| **Before** | `def process_data(data):` |
| **After** | Thêm Type Hint `-> list[str]:` và Google-style docstrings |

**After:**
```python
def process_data(data: str) -> list[str]:
    """Split a CSV string into a list of trimmed values.

    Args:
        data: Comma-separated string. Must not be None.

    Returns:
        List of stripped string tokens.

    Raises:
        ValueError: If *data* is None or not a string.
    """
```

---

## Bảng tổng kết Task 4

| Loại Issue | Vấn đề | Đã Fix | Severity |
|---|---|---|---|
| 🐛 Bug | NoneType dereference | Guard clause `if is None` | 🔴 Critical |
| 🔒 Vulnerability | Hardcoded password | Thay bằng `os.environ.get` | 🔴 Critical |
| 🌀 Code Smell | Bare except `except:` | Thay bằng `except Exception` | 🟡 Major |
| 🐛 Bug | Implicit `None` return | Raise `ValueError` nếu input rỗng | 🔴 Major |
| 🌀 Code Smell | Logic bị lặp lại | Gom vào helper `_normalize` | 🟡 Minor |
| 🌀 Code Smell | Thiếu Type Hint | Thêm đầy đủ type annotation | 🟡 Minor |
| 🌀 Code Smell | Thiếu Docstring | Thêm Google-style docstring | 🟡 Info |
