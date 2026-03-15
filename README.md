# Library Management API (Flask)

A production-ready **RESTful API** for a Library Management system built with **Python Flask** and **SQLAlchemy**. It covers core flows like **book inventory**, **lending (loans)**, and **user management**, with a clean, extensible architecture.

> **Highlights**: Flask blueprints, service & repository layers, migrations with Alembic/Flask-Migrate, pagination & filtering, robust validation, and test scaffolding.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Run](#run)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
  - [Books](#books)
  - [Users](#users)
  - [Loans](#loans)
- [Business Rules](#business-rules)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Observability](#observability)
- [Performance Notes](#performance-notes)
- [Docker (optional)](#docker-optional)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## Features
- **Book Inventory**: create, read, update, delete (CRUD); search by title/author/isbn; pagination & sorting.
- **Lending (Loans)**: checkout / return flows; due dates; prevents checkout when no copies are available.
- **User Management**: CRUD for library members; track active and historical loans per user.
- **Validation & Errors**: consistent JSON error envelopes; payload validation.
- **Migrations**: reproducible schema with Alembic / Flask-Migrate.
- **Extensible Auth**: ready-to-plug JWT or session auth (off by default for simplicity).

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: Flask (Blueprints), Flask-RESTful or pure Flask routes
- **ORM**: SQLAlchemy
- **Migrations**: Alembic / Flask-Migrate
- **DB**: PostgreSQL (prod), SQLite (dev/testing)
- **Testing**: pytest, Flask testing client
- **Lint/Format**: flake8, black, isort

## Architecture
```
┌───────────────────────────────────────────────────────┐
│                    Flask Application                  │
│  ┌───────────┐   ┌────────────┐   ┌────────────────┐  │
│  │ Blueprints│→→ │  Services  │ → │ Repositories   │ → │ SQLAlchemy/DB
│  └───────────┘   └────────────┘   └────────────────┘  │
│       ↑  ↓              ↑              ↑               │
│     DTOs/Schema     Business        Persistence         │
│     (validation)      logic          (ORM ops)          │
└───────────────────────────────────────────────────────┘
```
- **Blueprints** expose REST endpoints.
- **Services** encapsulate business rules (e.g., checkout/return flows).
- **Repositories** isolate data access (queries, pagination, transactions).

## Database Schema

```mermaid
erDiagram
    USER ||--o{ LOAN : "borrows"
    BOOK ||--o{ LOAN : "loaned"

    USER {
        int id PK
        string name
        string email UNIQUE
        datetime created_at
        datetime updated_at
    }

    BOOK {
        int id PK
        string title
        string author
        string isbn UNIQUE
        int total_copies
        int available_copies
        datetime created_at
        datetime updated_at
    }

    LOAN {
        int id PK
        int user_id FK
        int book_id FK
        date loan_date
        date due_date
        date return_date NULL
        string status  // ACTIVE | RETURNED | OVERDUE
        datetime created_at
        datetime updated_at
    }
```

---

## Getting Started

### Prerequisites
- Python **3.10+**
- PostgreSQL **13+** (recommended for prod) or SQLite (for local/dev)
- `pip` (or `poetry`, optional)

### Setup
```bash
# 1) Clone
git clone https://github.com/your-org/library-management-api.git
cd library-management-api

# 2) Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Create .env (or export env vars)
cp .env.example .env

# 5) Initialize DB (SQLite or Postgres based on env vars)
flask db upgrade
```

### Run
```bash
# With Flask CLI
env FLASK_APP=app:create_app FLASK_ENV=development flask run
# or
python -m flask --app app:create_app --debug run
```
App runs at: `http://127.0.0.1:5000` (by default)

---

## Environment Variables
Create a `.env` file at the project root:
```dotenv
# Flask
FLASK_ENV=development
SECRET_KEY=replace-with-a-strong-secret

# Database (use one)
DATABASE_URL=sqlite:///./library.db
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/library

# Pagination defaults
PAGE_SIZE=20
MAX_PAGE_SIZE=100

# Auth (optional)
ENABLE_AUTH=false
JWT_SECRET=replace-if-auth-enabled
JWT_EXP_MINUTES=60
```

---

## API Reference
Base URL: `/api/v1`

### Books
**List books**
```http
GET /api/v1/books?query=python&author=Mark&sort=title&order=asc&page=1&page_size=20
```
**Create book**
```http
POST /api/v1/books
Content-Type: application/json
{
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "isbn": "9780134494166",
  "total_copies": 5
}
```
**Get book by id**
```http
GET /api/v1/books/{id}
```
**Update book**
```http
PATCH /api/v1/books/{id}
Content-Type: application/json
{
  "title": "Clean Architecture (2nd Ed.)",
  "total_copies": 6
}
```
**Delete book**
```http
DELETE /api/v1/books/{id}
```

**Response (example)**
```json
{
  "id": 42,
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "isbn": "9780134494166",
  "total_copies": 5,
  "available_copies": 5,
  "created_at": "2026-03-15T06:45:00Z",
  "updated_at": "2026-03-15T06:45:00Z"
}
```

### Users
**List users**
```http
GET /api/v1/users?query=alex&page=1&page_size=20
```
**Create user**
```http
POST /api/v1/users
Content-Type: application/json
{
  "name": "Alex Doe",
  "email": "alex@example.com"
}
```
**Get user by id**
```http
GET /api/v1/users/{id}
```
**Update user**
```http
PATCH /api/v1/users/{id}
Content-Type: application/json
{
  "name": "Alexandra Doe"
}
```
**Delete user**
```http
DELETE /api/v1/users/{id}
```
**List a user's loans**
```http
GET /api/v1/users/{id}/loans?status=ACTIVE
```

### Loans
**Checkout (create loan)**
```http
POST /api/v1/loans
Content-Type: application/json
{
  "user_id": 1,
  "book_id": 42,
  "due_date": "2026-03-29"
}
```
**Return (close loan)**
```http
PATCH /api/v1/loans/{id}
Content-Type: application/json
{
  "action": "return"
}
```
**List loans**
```http
GET /api/v1/loans?status=ACTIVE&user_id=1&book_id=42&page=1&page_size=20
```

**Loan response (example)**
```json
{
  "id": 1001,
  "user_id": 1,
  "book_id": 42,
  "loan_date": "2026-03-15",
  "due_date": "2026-03-29",
  "return_date": null,
  "status": "ACTIVE",
  "created_at": "2026-03-15T06:50:00Z",
  "updated_at": "2026-03-15T06:50:00Z"
}
```

**Error envelope (example)**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field 'isbn' must be unique.",
    "details": {"isbn": ["already exists"]}
  }
}
```

---

## Business Rules
- **Availability**: `available_copies` decreases on checkout and increases on return; cannot checkout when `available_copies == 0`.
- **Due Dates**: default to **14 days** from `loan_date` if not provided; loans past due become **OVERDUE** (background job or at read time).
- **Uniqueness**: `BOOK.isbn` and `USER.email` must be unique.
- **Cascade behavior**: prevent deleting a `USER` or `BOOK` with active loans (enforce at service layer and/or with DB constraints).

---

## Testing
```bash
pytest -q
# with coverage
pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=term-missing
```
- Uses Flask test client and in-memory SQLite for fast tests.
- Example fixtures for sample users/books/loans.

---

## Code Quality
```bash
# Format
black .
# Sort imports
isort .
# Lint
flake8 .
```

---

## Observability
- **Logging**: JSON logs in production, structured with request id and endpoint.
- **Error handling**: global error handlers map exceptions → consistent JSON responses with proper HTTP codes.
- **Health checks**: `/health` endpoint (lightweight DB ping optional).

---

## Performance Notes
- **Indexes**: add B-Tree indexes on `BOOK.isbn`, `BOOK.title`, `USER.email`, and FK columns in `LOAN`.
- **Pagination**: default page size configurable via env vars; enforce max page size.
- **N+1 avoidance**: use `selectinload`/`joinedload` for common joins.

---

## Docker (optional)
A minimal setup if you prefer containers.

**Dockerfile** (example):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5000"]
```

**docker-compose.yml** (example):
```yaml
version: '3.9'
services:
  api:
    build: .
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/library
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: library
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

---

## Project Structure
```
.
├── app/
│   ├── __init__.py           # create_app(), extensions, config
│   ├── models.py             # SQLAlchemy models: User, Book, Loan
│   ├── schemas.py            # Marshmallow/Pydantic-style validation (optional)
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── book_repo.py
│   │   ├── user_repo.py
│   │   └── loan_repo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   ├── user_service.py
│   │   └── loan_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── books.py          # /api/v1/books
│   │   ├── users.py          # /api/v1/users
│   │   └── loans.py          # /api/v1/loans
│   ├── errors.py             # error mappers & handlers
│   └── config.py             # settings & env parsing
├── migrations/               # Alembic/Flask-Migrate
├── tests/                    # pytest suites
├── requirements.txt
├── .env.example
├── Dockerfile                # optional
├── docker-compose.yml        # optional
└── README.md
```

---

## Roadmap
- ✅ Core CRUD for books, users, loans
- ✅ Checkout/return flows with availability checks
- ⬜ Authentication & role-based authorization (admin vs member)
- ⬜ Rate limiting & API keys
- ⬜ OpenAPI/Swagger docs (`/docs`)
- ⬜ Background job for marking overdue loans
- ⬜ CI pipeline (lint, test, build)

---

## License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

> Maintainer: *Your Name*  
> Contact: your.email@example.com

