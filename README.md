<p align="center">
  <img src="assets/racerapi-logo.png" alt="RacerAPI Logo"/>
</p>


<p align="center">
  Production-grade modular monolith architecture built on FastAPI
</p>

---

## 🚀 Overview

RacerAPI is a **minimal, structured backend foundation** for building scalable applications using FastAPI.

It combines:

* ⚡ FastAPI performance
* 🧩 Modular architecture (inspired by NestJS)
* 🧱 Clean layering and separation of concerns

---

## 🏗️ Architecture

RacerAPI follows a **modular monolith design**:

```text
API (controller) → Service → Repository → Database
```

### Key Principles

* No framework wrapping (pure FastAPI)
* Feature-based modules (`modules/`)
* Clear separation of concerns
* No cross-module imports
* Dependency injection via FastAPI `Depends`

---

## 📂 Project Structure

```text
racerapi/
├── main.py
├── core/
├── modules/
│   └── <feature>/
│       ├── controller.py
│       ├── service.py
│       ├── repository.py   # optional
│       ├── module.py
│       └── tests
├── shared/
├── utils/
└── tests/
```

---

## ⚡ Quick Start

### 1. Setup environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

---

### 2. Run the application

```bash
python -m racerapi.main
```

---

### 3. Health check

```bash
curl http://127.0.0.1:8000/health
```

---

## 🧪 Development & Validation

Run tests:

```bash
python -m pytest -q
```

Lint code:

```bash
python -m ruff check src tests
```

Architecture validation:

```bash
python scripts/check_architecture.py
```

---

## ⚙️ Environment Configuration

Copy:

```bash
.env.example → .env
```

### Key variables:

```env
RACERAPI_ENV=dev|test|prod
RACERAPI_DATABASE_URL=your_database_url
RACERAPI_LOG_LEVEL=INFO
RACERAPI_DEBUG=false
```

---

## 🎯 Design Goals

* Minimal but scalable
* Clear architecture without over-engineering
* Easy onboarding for developers
* Production-ready foundation

---

## 🔌 Extensibility (Plugins)

RacerAPI is designed to support optional plugins:

* Database integrations (SQL, Mongo)
* Authentication (JWT, OAuth)
* Logging and monitoring
* Caching and background jobs

Plugins extend the system **without coupling to core**.

---

## 📌 Philosophy

> Keep the core simple. Add complexity only when needed.

---

## 🛣️ Roadmap

* Plugin system (DB, Auth, Logger)
* Dependency Injection container
* CLI generators (modules, resources)
* Production tooling improvements

---

## 📄 License

MIT License
