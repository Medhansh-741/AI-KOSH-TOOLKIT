# AIKosh Dataset Quality Evaluation Toolkit

![AIKosh Logo](https://img.shields.io/badge/AIKosh-Dataset%20Quality-blue?style=for-the-badge)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](#)
[![Python Version](https://img.shields.io/badge/python-3.10-blue?style=flat-square&logo=python)](backend/requirements.txt)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.x-blue?style=flat-square&logo=postgresql)](#)
[![Celery](https://img.shields.io/badge/Celery-5.4.0-green?style=flat-square&logo=celery)](#)
[![Redis](https://img.shields.io/badge/Redis-7.2-red?style=flat-square&logo=redis)](#)
[![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-orange?style=flat-square)](#)

> Automated dataset quality assessment, clinical profiling, and privacy scoring toolkit for the AIKosh platform.

---

### [Quick Start](#8-quick-start) &middot; [API Docs](#12-api-documentation) &middot; [Architecture](#3-system-architecture) &middot; [Cheatsheet](#14-common-commands-cheatsheet) &middot; [Troubleshooting](#15-troubleshooting--faq)

---

## Table of Contents
1. [Overview & Concept](#1-overview--concept)
2. [Key Features](#2-key-features)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack & Decision Notes](#4-tech-stack--decision-notes)
5. [Security & Authentication](#5-security--authentication)
6. [Living Documentation & Reference Disclaimer](#6-living-documentation--reference-disclaimer)
7. [Prerequisites](#7-prerequisites)
8. [Quick Start](#8-quick-start)
9. [Configuration Reference](#9-configuration-reference)
10. [Development Setup (Without Docker)](#10-development-setup-without-docker)
11. [Database Migrations (Alembic)](#11-database-migrations-alembic)
12. [API Documentation](#12-api-documentation)
13. [Testing](#13-testing)
14. [Common Commands Cheatsheet](#14-common-commands-cheatsheet)
15. [Troubleshooting & FAQ](#15-troubleshooting--faq)
16. [Production Deployment (Kubernetes)](#16-production-deployment-kubernetes)

---

## 1. Overview & Concept

The **AIKosh Dataset Quality Evaluation Toolkit** provides a robust, standardized framework to evaluate, profile, and audit datasets intended for artificial intelligence and machine learning applications in clinical and healthcare domains. 

In clinical AI, data quality directly correlates with patient safety, algorithmic bias, and model generalizability. The toolkit acts as a gatekeeper, scoring uploaded datasets across **15 distinct evaluation domains** including clinical representative balance, annotation methodology accuracy, and privacy compliance. It computes a unified Clinical Quality Index (CQI) and Patient Risk Score (PRS), generating downloadable audit reports in HTML, JSON, and PDF formats.

This system is built to scale horizontally using an asynchronous task architecture, supporting massive tabular datasets (e.g., millions of clinical rows) while preserving low API latency.

---

## 2. Key Features

| Feature | Description | Reference Docs |
| :--- | :--- | :--- |
| **CQI Scoring Engine** | Evaluates datasets against 15 clinical and technical domains, calculating a normalized CQI score (0–100) and mapping it to certification bands (Diamond, Platinum, Gold, Silver, Bronze, Remediation). | [TDD §4.1 (CQI Algorithm)](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#41-cqi-scoring-algorithm) |
| **PRS Calculation** | Computes Patient Risk Scores (PRS) based on data sensitivity levels, de-identification methods, and the application of Differential Privacy. | [TDD §4.2 (PRS Algorithm)](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#42-prs-algorithm) |
| **Automated Profiling** | Background workers compute structural and statistical summaries of uploaded datasets using a fast Arrow/Pandas ingestion pipeline. | [dataset_profile.py](./backend/app/models/dataset_profile.py) |
| **Compliance Auditing** | Tracks all evaluation job transitions and model overrides in an append-only, deletion-protected audit log table. | [audit_log.py](backend/app/models/audit_log.py) & [TDD §6.1 (Audit Logs DDL)](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#61-postgresql-schema-ddl) |
| **Multi-Format Reports** | Generates downloadable and shareable evaluation reports in JSON, HTML, and print-ready PDF formats. | [assessment_result.py](backend/app/models/assessment_result.py) & [TDD §7 (Reports Generation)](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#7-reports-generation-service) |
| **Supported File Formats** | Tabular and semi-structured file support (CSV, Excel ingestion). | [PRD §23 (Supported Formats)](docs/PRD_AIKosh_Dataset_Quality_Toolkit.md#23-supported-dataset-formats) |

---

## 3. System Architecture

### Data Flow Overview

```
                      +-------------------+
                      |   React Frontend  | (Port 3000)
                      +---------+---------+
                                |
                                | HTTP REST APIs (with API Key)
                                v
                      +-------------------+
                      |   FastAPI App     | (Port 8000)
                      +----+----+----+----+
                           |    |    |
           +---------------+    |    +---------------+
           | SQL (Async)        |                    | S3 API (Boto3)
           v                    v Redis Broker       v
     +-----------+         +----+------+       +-----------+
     | PostgreSQL|         |   Redis   |       |   MinIO   | (Ports 9000/9001)
     +-----------+         +----+------+       +-----------+
                                |
                                | Queues: "assessment", "webhook"
                                v
                      +---------+---------+
                      |   Celery Workers  | (Asynchronous Pipelines)
                      +---------+---------+
                                |
                                +--> [Ingestion] -> [Profiling] -> [Domain Scoring] -> [Report Generation]
```

### Repository Structure

```
.
├── .agents/                 # Internal development configurations
├── backend/                 # Backend codebase (FastAPI + Celery)
│   ├── alembic/             # Database migrations configuration and versions
│   ├── app/
│   │   ├── api/             # API Router endpoints (assessments, reports, health)
│   │   ├── models/          # SQLAlchemy Database Models (TDD §6 compliant)
│   │   ├── schemas/         # Pydantic Schemas for Request/Response validation
│   │   ├── worker/          # Celery worker definitions and task pipelines
│   │   ├── config.py        # Settings configuration using Pydantic Settings
│   │   ├── database.py      # SQLAlchemy engine and session pool setups
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/               # Backend test suites
│   ├── Dockerfile           # Backend container image build blueprint
│   └── requirements.txt     # Python backend dependencies
├── frontend/                # Frontend codebase (React + Vite)
│   ├── src/                 # React component declarations and state
│   ├── Dockerfile           # Frontend web-server container configuration
│   └── package.json         # Node.js dependencies configuration
├── k8s/                     # Production Kubernetes deployments manifests
│   ├── api-deployment.yaml  # FastAPI web-server pods deployment (3 replicas)
│   ├── ingress.yaml         # Ingress Nginx TLS and routing definitions
│   ├── postgres-statefulset.yaml # StatefulSet definition for Postgres storage
│   ├── redis-deployment.yaml # Key-value store deployment
│   ├── worker-deployment.yaml # Split Celery worker deployments (assessment / webhook)
│   └── worker-hpa.yaml      # Horizontal Pod Autoscaler for assessment workers
└── docker-compose.yml       # Local developer compose setup (8 coordinated services)
```

---

## 4. Tech Stack & Decision Notes

| Technology | Purpose | Decision Note / Rationale |
| :--- | :--- | :--- |
| **FastAPI** | High-performance API Gateway | Chosen for high-speed asynchronous request handling, automated OpenAPI/Swagger generation, and built-in type validation via Pydantic. |
| **React (Vite)** | Responsive frontend client dashboard | Vite provides near-instant reload times during local development compared to CRA. |
| **PostgreSQL 16** | Core transactional database | Offers strict ACID compliance, transactional integrity, relational safety, check constraints, and native enum validation. [TDD §6](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#6-database-design--full-schema) |
| **Celery** | Asynchronous background processing | Offloads long-running CPU-intensive CSV parsing, dataset profiling, and scoring calculations from the FastAPI web thread. [TDD §5](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#5-background-task-processing) |
| **Redis** | Broker & cache | Low-latency, high-throughput in-memory data store ideal for Celery task queuing and temporary result caching. |
| **MinIO** | S3-compatible local object storage | Allows us to write standard cloud-ready S3 code (Boto3) locally without internet dependencies or cloud costs. |
| **Flower** | Celery task monitoring dashboard | Provides real-time visual tracking of worker queues, task states, execution times, and pipeline bottlenecks. |
| **WeasyPrint** | PDF report generator backend | Compiles styled HTML/CSS templates into high-fidelity, print-ready PDF files on the backend. [TDD §7](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#7-reports-generation-service) |
| **Pandas & PyArrow** | Tabular data ingestion & profiling | Enables blazing fast memory-mapped data ingestion and column-level statistical profiling of large tabular CSV files. |
| **Pydantic** | Schema validation & configuration | Standardizes request/response payloads, maps settings from environment variables, and catches runtime type errors. |
| **Alembic** | Relational schema migrations | Ensures repeatable, reversible, and version-controlled database schema updates across all environments. [TDD §6.3](docs/TDD_AIKosh_Dataset_Quality_Toolkit.md#63-migrations-strategy-alembic) |
| **Docker & Compose**| Container orchestration | Standardizes the runtime environment across 8 different microservices, eliminating the "works on my machine" problem. |
| **Kubernetes (K8s)**| Production hosting & auto-scaling | Automates container scaling (via HPA), service routing, high availability, and resource constraints isolation. |

---

## 5. Security & Authentication

The system uses a **Dual-Authentication Model** to support both secure human browser interactions and programmatic machine integrations:
*   **User Session Authentication (Browser UI):** JWT stored in a secure, `HttpOnly`, `Secure`, `SameSite=Lax` cookie named `session_token`.
*   **Developer API Key Authentication (Machine Integrations):** API keys passed as Bearer tokens in the `Authorization` header (`Authorization: Bearer <api_key>`), validated against SHA-256 database hashes.
*   **Role-Based Access Boundaries:** Supports `user` (submitter), `reviewer`, and `admin` roles. Admins manage user accounts but are strictly prohibited from viewing user datasets or reports to maintain a firm privacy boundary.
*   **Tenant Data Isolation:** Users only have access to view and manage their own datasets and assessments.
*   **Manual Deletion:** Dataset files are stored securely in S3/MinIO and only deleted when manually triggered by the user via the UI/API (no automatic purging).

---

## 6. Living Documentation & Reference Disclaimer

> [!IMPORTANT]
> The architectural design patterns, dataset questionnaires, and schemas found inside the **[docs/](docs/)** folder are **living reference guidelines**. They represent target specifications but are subject to modification and refinements as development progresses and integration challenges arise. The active code base remains the source of truth.

---

## 7. Prerequisites

Ensure you have the following system-level software installed before setup:
*   **Docker Engine:** version `20.10.x` or newer (supporting Compose V2)
*   **Python:** version `3.10.x` (for local backend development)
*   **Node.js:** version `18.x` LTS (for local frontend development)
*   **PostgreSQL Client (`psql`):** version `16.x` (optional, for direct SQL debugging)

---

## 8. Quick Start

Deploy the entire stack locally in 3 steps:

```bash
# 1. Clone the repository and set up environment configurations
cp .env.example .env

# 2. Build and start all 8 container services in the background
docker compose up --build -d

# 3. Apply database migrations to PostgreSQL
docker compose exec backend alembic upgrade head
```

The services will be available at:
*   **React Dashboard:** http://localhost:3000
*   **FastAPI OpenAPI Docs:** http://localhost:8000/docs
*   **MinIO Console Panel:** http://localhost:9001 (minioadmin / minioadmin)
*   **Flower Celery Monitoring:** http://localhost:5555

---

## 9. Configuration Reference

<details>
<summary><b>Click to expand Environment Variables Reference Table...</b></summary>

System configurations are loaded from the root `.env` file:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `POSTGRES_USER` | `postgres` | Username for the core database instance. |
| `POSTGRES_PASSWORD` | `postgres` | Password for the database instance. |
| `POSTGRES_DB` | `aikosh_quality` | Database name. |
| `POSTGRES_HOST` | `postgres` | Database container host address. |
| `POSTGRES_PORT` | `5432` | Database container port. |
| `REDIS_URL` | `redis://redis:6379/0` | Connection broker URL for Celery. |
| `S3_ENDPOINT_URL` | `http://minio:9000` | Local endpoint for S3-compatible file storage. |
| `S3_ACCESS_KEY` | `minioadmin` | S3 console access key. |
| `S3_SECRET_KEY` | `minioadmin` | S3 console secret key. |
| `S3_BUCKET_NAME` | `aikosh-datasets` | Bucket name for uploaded datasets and reports. |
| `API_KEY_SECRET` | `tkt_secret_super_secure_key_12345678` | System-wide static API Key. |

</details>

---

## 10. Development Setup (Without Docker)

To run the components locally on your host machine for faster debugging cycles:

### A. Run Backend App
1. Navigate to the backend directory and create a virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies listed in requirements file:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Alembic migrations (*Note: Ensure a PostgreSQL instance is running on `localhost:5432` and the database `aikosh_quality` exists before running this*):
   ```bash
   alembic upgrade head
   ```
4. Start FastAPI server using Uvicorn:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

### B. Run Frontend App
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install packages listed in package.json:
   ```bash
   npm install
   ```
3. Run development web server:
   ```bash
   npm run dev
   ```

---

## 11. Database Migrations (Alembic)

Database schema modifications are managed using Alembic.
*   **Apply all pending migrations:**
    ```bash
    docker compose exec backend alembic upgrade head
    ```
*   **Revert the last applied migration:**
    ```bash
    docker compose exec backend alembic downgrade -1
    ```
*   **Generate a new autodetected migration script:**
    ```bash
    docker compose exec backend alembic revision --autogenerate -m "description_of_change"
    ```

---

## 12. API Documentation

Once the backend service is running, the interactive API documentation is available at:
*   **Swagger UI (Interactive API tester):** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc (Clean reading mode):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 13. Testing

Run the test suites using `pytest` inside the backend container:

```bash
docker compose exec backend pytest
```

Test coverage focuses on scoring formulas, PRS risk calculations, dataset metadata model relationships, and API endpoints validation.

---

## 14. Common Commands Cheatsheet

| Command | Action |
| :--- | :--- |
| `docker compose up -d` | Start all stack services in the background. |
| `docker compose down` | Stop all running containers. |
| `docker compose logs -f backend` | Stream logs for the FastAPI web service. |
| `docker compose exec backend alembic upgrade head` | Run all database migrations. |
| `docker compose exec backend alembic downgrade -1` | Rollback the last database migration. |
| `docker compose exec backend pytest` | Run the backend test suites. |
| `docker compose exec postgres psql -U postgres -d aikosh_quality` | Open an interactive SQL shell inside PostgreSQL. |
| `docker compose restart backend` | Restart the web app container. |

---

## 15. Troubleshooting & FAQ

#### Q1: "port 5432 is already in use" on startup
*   **Reason:** You have a local instance of PostgreSQL running on your host machine.
*   **Fix:** Stop your host PostgreSQL service, or modify the port mapping in your `.env` file (e.g. `POSTGRES_PORT=5433`) and rebuild.

#### Q2: Alembic connection refused or "database does not exist"
*   **Reason:** Postgres container takes a few seconds to spin up and load its database configurations.
*   **Fix:** Wait 5-10 seconds for PostgreSQL to become healthy, then re-run the `alembic upgrade head` migration.

#### Q3: S3/MinIO bucket error "aikosh-datasets does not exist"
*   **Reason:** S3 endpoint URL mismatches or MinIO was started without bucket initialization.
*   **Fix:** Make sure the bucket name is defined as `aikosh-datasets` in your `.env`. Celery workers will automatically attempt to create the bucket if it is missing during the first file upload assessment task.

---

## 16. Production Deployment (Kubernetes)

Production manifests are housed inside the **[k8s/](k8s/)** directory, targeting the namespace `aikosh-quality-toolkit`.

To deploy the cluster services:
```bash
# 1. Apply databases and brokers
kubectl apply -f k8s/postgres-statefulset.yaml
kubectl apply -f k8s/redis-deployment.yaml

# 2. Deploy API servers and Celery workers
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml

# 3. Configure Ingress routes and Autoscalers
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/worker-hpa.yaml
```

The system scales background worker pods dynamically between `3` and `20` replicas via the Horizontal Pod Autoscaler (`k8s/worker-hpa.yaml`) based on Celery queue depth metrics.
