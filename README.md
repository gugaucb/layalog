# ⚡ LayaLog — Intelligent Log Observability & AI Semantic Diagnosis

<p align="center">
  <strong>Transform raw server logs into structured AI diagnoses, actionable root-cause insights, and real-time observability.</strong>
</p>

<p align="center">
  <a href="README.md"><strong>🇺🇸 English</strong></a> •
  <a href="README.pt-BR.md"><strong>🇧🇷 Português</strong></a> •
  <a href="README.zh-CN.md"><strong>🇨🇳 简体中文</strong></a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://hub.docker.com/r/gugaucb/layalog"><img src="https://img.shields.io/docker/v/gugaucb/layalog?label=Docker%20Hub&logo=docker&logoColor=white&color=2496ED" alt="Docker Hub" /></a>
  <a href="https://github.com/typesafe-ai/laya"><img src="https://img.shields.io/badge/Laya%20AI-System%20One-7928CA?logo=openai&logoColor=white" alt="Laya AI" /></a>
  <a href="https://driverjs.com/"><img src="https://img.shields.io/badge/Driver.js-Guided%20Tour-FF5722?logo=javascript&logoColor=white" alt="Driver.js" /></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-E2E%20Tests%20Passing-2EAD33?logo=playwright&logoColor=white" alt="Playwright" /></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Pytest-100%25%20Passing-brightgreen?logo=pytest&logoColor=white" alt="Pytest" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## 📖 Overview

**LayaLog** is a modern log observability platform designed for engineering and SRE teams dealing with massive, high-volume server logs. Instead of exhausting hours in manual `grep` scans across hundred-megabyte text files, LayaLog unites:

1. **Smart Signature Clustering**: Cryptographically groups repeated stack traces, timestamps, UUIDs, and log signatures before model inference, reducing LLM calls by over 98%.
2. **Laya AI (System One Engine)**: Delivers typed semantic judgments (`Choice`, `Score`, `Noul`) to classify root causes, severity ratings (Low, Medium, Critical), and recommend immediate remediation steps.
3. **Quiet UI & Master-Detail Architecture**: Clean, high-density dashboard inspired by modern observability tooling.
4. **Virtualized Stream Explorer (60 FPS)**: Virtual scrolling engine rendering millions of lines with zero browser memory bloat and real-time query highlighting.
5. **Interactive Guided Tour ([Driver.js](https://driverjs.com/))**: Step-by-step product walkthrough integrated natively with full multilingual support.
6. **Full Internationalization (i18n)**: Seamless real-time switching between English (`en`), Brazilian Portuguese (`pt-br`), and Simplified Chinese (`cn`).

---

## 📸 Screenshots

### 1. Gravity Profiles & Calibration Studio
Create, customize, clone, and manage domain-specific semantic calibration profiles (*Web Apps, Keycloak / IAM, Payment Gateways, Databases, Event-Driven Queues*) that tune Laya AI's evaluation criteria.

<p align="center">
  <img src="docs/assets/02-perfis-gravidade.png" alt="Gravity Profiles Modal" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

### 2. High-Performance Virtualized Log Explorer
Virtualized chunked stream viewer with mono-spaced typography (*JetBrains Mono*), direct line jumps, and real-time search match highlighting.

<p align="center">
  <img src="docs/assets/03-explorador-logs.png" alt="Virtualized Log Viewer" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

---

## 🎯 7 Native Laya AI Gravity Profiles

LayaLog includes 7 built-in calibration profiles tailored for standard production architectures:

| Profile | Domain Focus | Critical Severity Trigger (Score 3) |
| :--- | :--- | :--- |
| **Web Application / Monolith** | REST APIs, MVC, HTTP handlers | 5xx cascades, database unreachable, broken checkout flow |
| **Keycloak / IAM / OAuth2** | SSO, Realms, LDAP, JWT tokens | Realm locked, Keycloak DB connection pool failure, token forgery |
| **Payment Gateway** | Financial transactions, PIX, credit cards | Transaction drops, acquirer timeout, idempotency violations |
| **Microservices / Event-Driven** | Kafka, RabbitMQ, gRPC | Dead-letter queue overflow, split-brain, consumer group stall |
| **Async Workers / Queues** | Celery, Redis, background jobs | Pipeline deadlock, worker OOM, billing batch process drop |
| **Databases & Storage** | Postgres, MySQL, Redis, S3 | Connection exhaustion, lock wait timeout, data corruption |
| **Edge / Gateway / Infrastructure** | Nginx, Traefik, Envoy, DNS | All upstreams down, expired TLS certificate, connection saturation |

---

## 🚀 Key Features

- **⚡ NDJSON Progressive Streaming**: Real-time progress updates with user cancellation support via `AbortController`.
- **🎯 Dynamic Gravity Calibration**: Modify criteria on the fly or duplicate existing built-in profiles.
- **🧭 Interactive Product Tour**: Built with [Driver.js](https://driverjs.com/) to guide users through key capabilities.
- **🌐 Triple-Language i18n Engine**: Instant switching across English, Portuguese, and Simplified Chinese without page reloads.
- **📊 Real-time Operational KPIs**: Instant calculation of total lines, classified error events, high-priority criticals, and availability impact rate.
- **📝 Executive Markdown Export**: Generates comprehensive post-mortem Markdown reports ready for Jira, GitHub Issues, or Slack.
- **💾 SQLite Snapshot History**: Lightweight, zero-config local persistence allowing instant historical review and one-click deletion.

---

## 🛠️ Quick Start & Installation

### Prerequisites
- Python 3.9 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 1. Clone & Set Up Environment

```bash
# Clone repository
git clone https://github.com/gugaucb/layalog.git
cd layalog

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or: .venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Launch the Web Server

```bash
python run.py
```

Open your browser and navigate to: **[http://localhost:8100](http://localhost:8100)**

### 🐳 Run with Docker (Docker Hub)

You can pull and run the official pre-built image directly from Docker Hub:

```bash
# Pull the latest image
docker pull gugaucb/layalog:latest

# Run the container (mapping port 8100)
docker run -d -p 8100:8100 --name layalog gugaucb/layalog:latest
```

Access the application at: **[http://localhost:8100](http://localhost:8100)**

---

## 🧪 Automated Testing

LayaLog includes full unit test coverage and automated browser E2E suites powered by **Playwright**:

```bash
# Run backend test suite (unit + integration)
pytest

# Run Playwright automated E2E tests
python scripts/run_e2e_tests.py

# Run with verbose output
pytest -v
```

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/analyze-stream` | NDJSON streaming log upload & real-time classification |
| `POST` | `/api/analyze` | Synchronous consolidated log analysis |
| `GET` | `/api/analyses` | List saved analysis history |
| `GET` | `/api/analyses/{id}` | Retrieve full details of an analysis |
| `GET` | `/api/analyses/{id}/lines` | On-demand chunk pagination for virtual log viewer |
| `GET` | `/api/analyses/{id}/export-md` | Download executive diagnostic report in Markdown format |
| `DELETE`| `/api/analyses/{id}` | Permanently delete analysis record and log file |
| `GET` | `/api/profiles` | List all available gravity calibration profiles |
| `POST` | `/api/profiles` | Create a new custom gravity profile |
| `PUT` | `/api/profiles/{id}` | Update an existing custom profile |
| `DELETE`| `/api/profiles/{id}` | Delete a custom gravity profile |
| `POST` | `/api/profiles/{id}/clone` | Clone a profile creating an editable copy |

---

## 📁 Project Architecture

```
layalog/
├── layalog/
│   ├── app.py              # FastAPI server, REST routes & static SPA mount
│   ├── classifier.py       # Laya AI System One semantic classification engine
│   ├── database.py         # SQLite persistence & audit snapshots
│   ├── exporter.py         # Executive Markdown report generator
│   ├── models.py           # Pydantic data schemas & validation
│   ├── parser.py           # Log parsing & cryptographic signature clustering
│   ├── profiles.py         # 7 Built-in profiles & custom CRUD persistence
│   └── static/             # Single Page Application (SPA)
│       ├── css/v2.css      # Quiet UI design system & Driver.js theme
│       ├── js/i18n.js      # Multilingual translation dictionary (EN, PT-BR, CN)
│       ├── js/tour.js      # Driver.js interactive guided walkthrough
│       ├── js/v2-app.js    # Application controller, state & reactive UI
│       ├── js/v2-log-viewer.js # 60 FPS Virtualized log streaming engine
│       └── index.html      # Responsive HTML5 entry point
├── tests/                  # Pytest unit & integration suite
│   ├── e2e/                # Playwright automated browser tests
├── docs/                   # ADRs and visual documentation assets
├── pyproject.toml          # Python package configuration
├── requirements.txt        # Core dependencies
└── run.py                  # Entrypoint runner (port 8100)
```

---

## 🤝 Contributing

Contributions from the open-source community are very welcome!

1. Fork the Project (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m "feat: add amazing feature"`)
3. Ensure all tests pass (`pytest && python scripts/run_e2e_tests.py`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a descriptive Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
