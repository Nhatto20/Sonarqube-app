# SonarQube Demo App

FastAPI application minh họa quy trình tích hợp SonarQube vào CI/CD pipeline (GitHub Actions).

---

## 📁 Cấu trúc thư mục

```
sonarqube-app/
├── src/
│   ├── __init__.py
│   ├── app.py               # FastAPI entry-point
│   └── data_processor.py    # Business logic (code-issue demo)
├── tests/
│   ├── __init__.py
│   ├── test_app.py          # Integration tests
│   └── test_data_processor.py  # Unit tests
├── Dockerfile               # Multi-stage build
├── pyproject.toml
├── sonar-project.properties
├── FIXES.md                 # Before/after issue documentation
└── README.md
```

---

## ⚙️ Thiết lập (SonarQube đã chạy sẵn)

> **SonarQube server** và **secrets** (`SONAR_TOKEN`, `SONAR_HOST_URL`) đã được cấu hình sẵn từ project CI/CD chính — **không cần cài lại**.

### Bước duy nhất: Tạo project mới trên SonarQube dashboard

1. Truy cập SonarQube tại URL đã cấu hình
2. **Projects → Create Project → Manually**
3. Điền thông tin:

| Trường | Giá trị |
|--------|---------|
| Project key | `sonarqube-app` |
| Display name | `SonarQube Demo App` |

4. Tạo token mới **hoặc** dùng token hiện có (`SONAR_TOKEN` trong GitHub Secrets)

> ⚠️ Project key phải là **`sonarqube-app`** để khớp với `sonar-project.properties`.

---

## 🔐 GitHub Secrets (dùng chung với ci.yml)

| Secret | Mô tả |
|--------|-------|
| `SONAR_TOKEN` | ✅ Đã cấu hình sẵn |
| `SONAR_HOST_URL` | ✅ Đã cấu hình sẵn |

---

## 🚀 CI/CD Pipeline

Workflow `.github/workflows/sonarqube.yml` trigger khi có push/PR vào `sonarqube-app/**`:

```
push/PR to main
     │
     ▼
 [lint]       ── Ruff + Black (ubuntu-latest)
     │
     ▼
 [test]       ── pytest + coverage.xml (ubuntu-latest)
     │
     ▼
 [sonarqube]  ── SonarQube scan + Quality Gate (self-hosted runner)
```

Pipeline **tự động thất bại** nếu Quality Gate không đạt (`sonar.qualitygate.wait=true`).

---

## 🧪 Chạy tests + coverage local

```bash
cd sonarqube-app
pip install -e ".[dev]"
pytest --cov=src --cov-report=xml:coverage.xml --cov-report=term-missing
```

## 🔍 Chạy SonarQube scan local (tuỳ chọn)

```bash
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<your-token>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

---

## 🏗️ Build & Run Docker

```bash
docker build -t sonarqube-app:latest .
docker run -p 8000:8000 sonarqube-app:latest
```

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/health` | Liveness probe |
| GET | `/api/ping` | Connectivity check |
| GET | `/api/version` | App metadata |
| GET | `/api/process?data=a,b,c` | CSV split |
| GET | `/api/hash?value=hello` | SHA-256 hash |
| GET | `/api/normalize?username=X&email=Y` | Normalize fields |
| GET | `/api/risky` | Safe error handling demo |

---

## 🔒 Custom Quality Gate (Task 5)

Tạo trên SonarQube dashboard → **Quality Gates → Create**:

| Điều kiện | Ngưỡng |
|-----------|--------|
| New Bugs | = 0 |
| New Vulnerabilities | = 0 |
| New Code Coverage | ≥ 80 % |
| New Duplicated Lines | ≤ 3 % |

Sau khi tạo → **Set as Default** hoặc gán trực tiếp cho project `sonarqube-app`.
