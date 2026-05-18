# 🚀 Hướng Dẫn Chạy Project Từ Đầu — SonarQube Assignment

> **Mục tiêu:** Hoàn thành 5 Tasks (100 điểm) + Bonus SonarLint (+10 điểm)  
> **Stack:** Python 3.11 · FastAPI · pytest · SonarQube · GitHub Actions (self-hosted runner)

---

## 📋 Yêu cầu cài đặt trước

| Công cụ | Phiên bản tối thiểu | Kiểm tra |
|---------|-------------------|----------|
| Docker Desktop | 24+ | `docker --version` |
| Python | 3.11+ | `python --version` |
| Git | 2.40+ | `git --version` |
| GitHub account | — | Đã có repo `Nhatto20/Sonarqube-app` |

---

## TASK 1 — Cài SonarQube Server (15 điểm)

### Bước 1.1 — Khởi động SonarQube bằng Docker Compose

File `docker-compose.yml` đã có sẵn ở thư mục gốc (`Sonarqube/`), chạy từ **WSL terminal**:

```bash
# Từ thư mục gốc Sonarqube/
docker compose up -d sonarqube-db sonarqube
```

> ⏳ Chờ **1–2 phút** để SonarQube khởi động xong.

Kiểm tra logs:

```bash
docker logs -f sonarqube
# Chờ đến khi thấy: "SonarQube is operational"
```

> ⚠️ **Lưu ý WSL:** Tất cả lệnh `docker` phải chạy trong **WSL Debian terminal**, không phải PowerShell.

### Bước 1.2 — Đổi mật khẩu admin

1. Mở browser → `http://localhost:9000`
2. Đăng nhập: **admin / admin**
3. Hệ thống bắt buộc đổi mật khẩu → nhập mật khẩu mới (ghi lại)

### Bước 1.3 — Tạo project mới

1. **Projects → Create Project → Manually**
2. Điền:
   - **Project key:** `sonarqube-app`
   - **Display name:** `SonarQube Demo App`
3. Click **Set Up** → **Locally**
4. **Generate a token:**
   - Token name: `sonarqube-app-token`
   - Click **Generate** → **Copy token** (dạng `sqp_xxxx...`)
   - ⚠️ Token chỉ hiện **một lần** — lưu ngay vào nơi an toàn

### Bước 1.4 — Thêm secrets vào GitHub repo

Vào `https://github.com/Nhatto20/Sonarqube-app` → **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Giá trị |
|-------------|---------|
| `SONAR_TOKEN` | Token vừa copy (`sqp_xxxx...`) |
| `SONAR_HOST_URL` | `http://host.docker.internal:9000` |

> **⚠️ Tại sao phải dùng `host.docker.internal`?**
>
> Kiến trúc thực tế trên máy:
> ```
> WSL2 / Docker Host
> ├── [Container] github-runner   ← chạy CI job
> ├── [Container] sq_server       ← SonarQube :9000
> └── [Container] sq_db           ← PostgreSQL
> ```
>
> | Ngữ cảnh | `localhost` trỏ vào | Cần dùng |
> |----------|--------------------|---------|
> | WSL terminal / browser | Docker host ✅ | `localhost:9000` |
> | **Bên trong runner container** | Loopback của container ❌ | **`host.docker.internal:9000`** |
>
> Runner container đã khai báo `extra_hosts: host.docker.internal:host-gateway` → có thể resolve đúng.

📸 **Screenshot 1:** SonarQube dashboard sau khi tạo project (tab Projects).

---

## TASK 2 — Cấu hình Project Analysis (20 điểm)

### Bước 2.1 — Clone repo về máy (nếu chưa có)

```bash
git clone git@github.com:Nhatto20/Sonarqube-app.git
cd Sonarqube-app/sonarqube-app
```

### Bước 2.2 — Tạo môi trường Python & cài dependencies

> ⚠️ **Phải `cd` vào thư mục `sonarqube-app/` trước** — `pyproject.toml` nằm ở đây, không phải thư mục gốc.

```bash
# WSL terminal
cd /mnt/c/Users/japan/Workspaces/FPT-fsa/Docker/Sonarqube/sonarqube-app

# Tạo virtual environment
python3 -m venv .venv

# Kích hoạt (WSL/Linux)
source .venv/bin/activate

# Cài dependencies (bao gồm dev tools: pytest, ruff, black)
cd sonarqube-app
pip install -e ".[dev]"
```

> **Windows PowerShell** (nếu không dùng WSL):
> ```powershell
> cd sonarqube-app
> python -m venv .venv
> .\.venv\Scripts\Activate.ps1
> pip install -e ".[dev]"
> ```

### Bước 2.3 — Chạy tests và tạo coverage report

```bash
pytest \
  --cov=src \
  --cov-report=xml:coverage.xml \
  --cov-report=term-missing
```

Kết quả mong đợi:
```
PASSED tests/test_app.py
PASSED tests/test_data_processor.py
Coverage: >= 80%
```

### Bước 2.4 — Kiểm tra `sonar-project.properties`

File này đã có sẵn trong `sonarqube-app/`:

```properties
sonar.projectKey=sonarqube-app
sonar.projectName=SonarQube Demo App
sonar.sources=src
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
sonar.exclusions=**/__pycache__/**,**/.pytest_cache/**,**/migrations/**
sonar.qualitygate.wait=true
```

### Bước 2.5 — Chạy SonarQube scan local (manual)

Chạy từ **WSL terminal**, trong thư mục `sonarqube-app/`:

```bash
# SonarQube chạy qua docker compose → dùng tên service làm host
docker run --rm \
  --network sonarqube_default \
  -e SONAR_HOST_URL="http://sonarqube:9000" \
  -e SONAR_TOKEN="<token-của-bạn>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

> **Nếu không dùng network compose** (chạy SonarQube riêng lẻ):
> ```bash
> docker run --rm \
>   -e SONAR_HOST_URL="http://172.17.0.1:9000" \
>   -e SONAR_TOKEN="<token-của-bạn>" \
>   -v "$(pwd):/usr/src" \
>   sonarsource/sonar-scanner-cli
> ```

📸 **Screenshot 2:** SonarQube dashboard → tab **Overview** của project `sonarqube-app` sau khi scan xong.

---

## TASK 3 — Tích hợp GitHub Actions (25 điểm)

### Bước 3.1 — Kiểm tra self-hosted runner đang chạy

Workflow `sonarqube.yml` dùng `runs-on: self-hosted` cho job SonarQube.  
Runner phải **online** trên GitHub: **Settings → Actions → Runners**

Nếu runner chưa có, xem thư mục `runner/` trong repo để thiết lập.

### Bước 3.2 — Xác nhận secrets đã có

**Settings → Secrets and variables → Actions**

| Secret | Trạng thái |
|--------|-----------|
| `SONAR_TOKEN` | ✅ Đã cấu hình (Task 1.4) |
| `SONAR_HOST_URL` | ✅ Đã cấu hình (Task 1.4) |

### Bước 3.3 — Push code để trigger pipeline

```bash
# Từ thư mục gốc Sonarqube/
git add sonarqube-app/ .github/workflows/sonarqube.yml
git commit -m "feat: add sonarqube-app with CI/CD pipeline"
git push origin main
```

### Bước 3.4 — Theo dõi pipeline

GitHub → **Actions → SonarQube Analysis** → chọn run mới nhất

Pipeline chạy theo thứ tự:
```
[lint]  Ruff + Black check
  └─ [test]  pytest + coverage (chạy sau lint pass)
       └─ [sonarqube]  scan + quality gate (chạy sau test pass)
```

📸 **Screenshot 3:** GitHub Actions → tất cả 3 jobs màu xanh ✅.

---

## TASK 4 — Phân tích & Fix Code Issues (25 điểm)

### Danh sách 7 issues đã được fix trong `src/data_processor.py`

| # | Loại | Vấn đề gốc | Fix đã áp dụng | Mức độ |
|---|------|-----------|----------------|--------|
| 1 | 🐛 Bug | `data.split(",")` khi `data=None` → crash | Thêm guard: `if data is None: raise ValueError` | 🔴 Critical |
| 2 | 🔒 Vulnerability | `password = "admin123"` hardcoded | Đọc từ `os.environ.get("DB_PASSWORD")` | 🔴 Critical |
| 3 | 🌀 Code Smell | `except: pass` (bare except) | Thay bằng `except Exception as exc: logger.warning(...)` | 🟡 Major |
| 4 | 🐛 Bug | `calculate_hash` đôi khi trả `None` | Luôn trả `str`, raise `ValueError` nếu input rỗng | 🔴 Major |
| 5 | 🌀 Code Smell | Logic normalize bị copy-paste 2 lần | Trích ra hàm `_normalize()` dùng chung | 🟡 Minor |
| 6 | 🌀 Code Smell | Thiếu type annotations | Thêm đầy đủ `-> str`, `-> list[str]`, v.v. | 🟡 Minor |
| 7 | 🌀 Code Smell | Thiếu docstrings | Thêm docstring cho tất cả functions | 🟡 Info |

> Chi tiết before/after xem tại [`FIXES.md`](./FIXES.md)

### Bước 4.1 — Verify trên SonarQube

Sau khi scan (Task 2.5 hoặc pipeline Task 3):

- SonarQube → **Issues** → filter **Type = Bug** → 0 bugs
- SonarQube → **Issues** → filter **Type = Vulnerability** → 0 vulnerabilities
- SonarQube → **Security Hotspots** → Reviewed

📸 **Screenshot 4:** Tab Issues hiển thị 0 Bugs, 0 Vulnerabilities.

---

## TASK 5 — Cấu hình Custom Quality Gate (15 điểm)

### Bước 5.1 — Tạo custom quality gate

1. SonarQube → **Quality Gates** (menu trên cùng) → **Create**
2. Tên: `FPT Custom Gate` → **Save**
3. Click **Add Condition** và thêm lần lượt:

| Metric | Operator | Giá trị |
|--------|----------|---------|
| New Bugs | is greater than | **0** |
| New Vulnerabilities | is greater than | **0** |
| Coverage on New Code | is less than | **80** |
| Duplicated Lines on New Code (%) | is greater than | **3** |

4. Click **Save** sau mỗi condition

### Bước 5.2 — Gán Quality Gate cho project

1. **Projects → sonarqube-app → Project Settings → Quality Gate**
2. Chọn **FPT Custom Gate** → **Save**

### Bước 5.3 — Test Quality Gate PASS ✅

Push code hiện tại (code đã clean) → pipeline chạy → quality gate xanh.

```bash
git commit --allow-empty -m "test: trigger quality gate pass"
git push origin main
```

📸 **Screenshot 5:** SonarQube Quality Gate → **PASSED** (màu xanh).

### Bước 5.4 — Test Quality Gate FAIL ❌ (cố tình)

Thêm đoạn code lỗi vào cuối `src/data_processor.py`:

```python
# INTENTIONAL BUG — test quality gate fail (XÓA SAU KHI CHỤP ẢNH)
def bad_function(x):
    password = "admin123"   # hardcoded credential → Vulnerability
    return x.upper()        # crash nếu x là None → Bug
```

```bash
git add sonarqube-app/src/data_processor.py
git commit -m "test: intentional bug to trigger quality gate fail"
git push origin main
```

Pipeline sẽ fail tại bước **SonarQube Quality Gate Check**.

📸 **Screenshot 6:** SonarQube Quality Gate → **FAILED** (màu đỏ).  
📸 **Screenshot 7:** GitHub Actions → job `sonarqube` bị ❌.

### Bước 5.5 — Revert lại code sạch

```bash
git revert HEAD --no-edit
git push origin main
```

---

## 🎁 Bonus — SonarLint IDE Integration (+10 điểm)

### VSCode

1. Extension Marketplace → tìm **SonarLint** → Install
2. `Ctrl+Shift+P` → **SonarLint: Connect to SonarQube**
3. Điền:
   - Server URL: `http://localhost:9000`
   - Token: `<SONAR_TOKEN>`
4. Chọn project: `sonarqube-app`
5. SonarLint sẽ highlight lỗi **ngay trong editor** khi code

📸 **Screenshot 8 (Bonus):** VSCode hiển thị SonarLint warnings trong file.

---

## ✅ Checklist nộp bài

| # | Hạng mục | File/Location | Trạng thái |
|---|----------|---------------|-----------|
| 1 | Source code + `sonar-project.properties` | `sonarqube-app/` | ✅ Đã có |
| 2 | GitHub Actions workflow | `.github/workflows/sonarqube.yml` | ✅ Đã có |
| 3 | Documentation fixes (before/after) | `FIXES.md` | ✅ Đã có |
| 4 | README hướng dẫn setup | `README.md` | ✅ Đã có |
| 5 | Screenshot SonarQube dashboard (Task 1) | _(tự chụp)_ | 📸 |
| 6 | Screenshot analysis results (Task 2) | _(tự chụp)_ | 📸 |
| 7 | Screenshot GitHub Actions 3 jobs xanh (Task 3) | _(tự chụp)_ | 📸 |
| 8 | Screenshot 0 Issues (Task 4) | _(tự chụp)_ | 📸 |
| 9 | Screenshot Quality Gate PASSED (Task 5) | _(tự chụp)_ | 📸 |
| 10 | Screenshot Quality Gate FAILED (Task 5) | _(tự chụp)_ | 📸 |
| 11 | Screenshot SonarLint VSCode (Bonus) | _(tự chụp)_ | 📸 |

---

## 🏆 Điểm tổng kết

| Tiêu chí | Điểm |
|---------|------|
| Task 1 — SonarQube server setup | 15 |
| Task 2 — Project configuration | 20 |
| Task 3 — CI/CD integration | 25 |
| Task 4 — Code issue analysis & fixes | 25 |
| Task 5 — Quality gate configuration | 15 |
| **Tổng** | **100** |
| Bonus — SonarLint IDE integration | +10 |

---

## 🔧 Troubleshooting

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| `docker` not found trong PowerShell | Docker cài trong WSL, không phải Windows | Chạy tất cả lệnh docker trong **WSL terminal** |
| SonarQube chưa khởi động | Container còn đang start | Chờ thêm, check `docker logs sonarqube` |
| Image `2026.1-community` not found | Tag không tồn tại trên Docker Hub | Dùng `sonarqube:community` (trong docker-compose.yml) |
| Runner offline | Service chưa chạy | Trong WSL: `cd runner && docker compose up -d` |
| Quality gate timeout | `sonar.qualitygate.wait=true` chờ lâu | Tăng `timeout-minutes: 5` trong workflow |
| Coverage < 80% | Tests chưa đủ | Thêm test cases hoặc kiểm tra `pytest --cov` |
| Scanner không kết nối SonarQube | Network mismatch | Dùng `--network sonarqube_default` khi scan local |
| PostgreSQL không healthy | Volume cũ bị corrupt | `docker compose down -v` rồi `up` lại |
