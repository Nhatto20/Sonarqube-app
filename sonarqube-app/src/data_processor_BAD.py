# """
# data_processor.py — BEFORE version (intentional issues for Task 4 demo)
# Commit này dùng để SonarQube phát hiện các issues.
# SAU KHI chụp screenshot → revert về commit tiếp theo (fixed version).
# """

# import hashlib


# # ── Issue 1 (Bug): NoneType dereference ───────────────────────────────────────
# # Khi data=None → data.split(",") sẽ crash AttributeError
# def process_data(data):
#     result = data.split(",")
#     return result


# # ── Issue 2 (Vulnerability): Hardcoded credentials ────────────────────────────
# # SonarQube phát hiện hardcoded secret ngay lập tức
# def get_db_password():
#     password = "admin123"
#     return password


# # ── Issue 3 (Code Smell): Bare except clause ──────────────────────────────────
# # Bắt tất cả exception mà không xử lý → che giấu lỗi thật
# def risky_operation():
#     raise NotImplementedError("risky!")


# def safe_risky_call():
#     try:
#         risky_operation()
#         return True
#     except:
#         pass


# # ── Issue 4 (Bug): Implicit None return ───────────────────────────────────────
# # Nếu value rỗng → hàm trả về None thay vì str → caller crash
# def calculate_hash(value):
#     if value:
#         return hashlib.sha256(value.encode()).hexdigest()
#     # Missing return → trả về None ngầm


# # ── Issue 5 (Code Smell): Duplicated logic ────────────────────────────────────
# # Hai hàm làm cùng một việc, không trích ra helper
# def normalize_username(username):
#     return username.strip().lower()


# def normalize_email(email):
#     return email.strip().lower()


# # ── Issue 6 (Code Smell): Missing type annotations ────────────────────────────
# # Tất cả functions thiếu type hints → khó maintain

# # ── Issue 7 (Code Smell): Missing docstrings ──────────────────────────────────
# # Tất cả functions thiếu docstring → khó hiểu mục đích
