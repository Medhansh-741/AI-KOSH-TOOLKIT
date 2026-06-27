# AGENTS.md — AIKosh Dataset Quality Evaluation Toolkit

> Read this file **first** before any code changes. It overrides all tool-specific configs (`.clinerules`, `.cursorrules`, `CLAUDE.md`).

---

## 1. Project Identity

A standalone full-stack web application for automated MIDAS 2.0-grade health dataset quality assessment. Dataset custodians upload CSV/XLSX health research data via the browser UI, fill a 48-question metadata form, and receive structured quality scores across 15 MIDAS domains. External platforms (AIKosh) integrate via REST API + webhook.

**NOT** a library, plugin, SDK, or mobile app.

---

## 2. Architecture (Real)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Browser (Next.js 14, App Router)              │
│  /login → /upload → /dashboard/[id] → /admin                        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP + HttpOnly session cookie
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  FastAPI + Uvicorn (port 8000)                       │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │  auth.py   │  │ assess.py│  │ reports.py │  │ admin.py        │  │
│  │  /register │  │ /upload- │  │ /{id}/     │  │ /users          │  │
│  │  /login    │  │ url      │  │ report     │  │ /users/{id}/    │  │
│  │  /logout   │  │ /submit  │  │            │  │ toggle-active   │  │
│  │  /keys     │  │ /{id}    │  │            │  │                 │  │
│  └────────────┘  └────┬─────┘  └────────────┘  └─────────────────┘  │
│                       │                                              │
│  deps.py (dual auth: cookie JWT + Bearer API key)                    │
│  → get_current_user() → get_user_assessment() (BOLA guard)          │
│  → get_current_active_admin() / get_current_active_reviewer()       │
│                       │                                              │
│  SecurityHeadersMiddleware: X-Content-Type-Options, X-Frame-Options, │
│  HSTS (production only)                                              │
└───────────────────────┬──────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────────┐
         │              │                  │
         ▼              ▼                  ▼
┌────────────┐  ┌───────────┐  ┌────────────────────┐
│ PostgreSQL │  │ Redis 7.2 │  │ MinIO / S3          │
│ (port 5432)│  │ (broker)  │  │ (port 9000)         │
│            │  │           │  │ uploads/{id}/       │
│ SQLAlchemy │  │ Celery    │  │ profiles/{id}/      │
│ 2.0 async  │  │ results   │  │ reports/{id}/       │
└────────────┘  └─────┬─────┘  └────────────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │  Celery Workers          │
         │  ┌────────────────────┐  │
         │  │  assessment queue  │  │  13-step pipeline
         │  │  (4 concurrency)   │  │  profiler → 15 scorers →
         │  └────────────────────┘  │  CQI → PRS → Release →
         │  ┌────────────────────┐  │  Reports → Webhook
         │  │  webhook queue     │  │
         │  │  (2 concurrency)   │  │  → POST to AIKosh
         │  └────────────────────┘  │
         └──────────────────────────┘
                      │
                      ▼
         ┌──────────────────────┐
         │  Flower (port 5555)  │  Celery monitoring (dev only)
         └──────────────────────┘
```

**Key decisions:**
- Frontend is the **primary** interface; everything auth-gated
- API serves **both** browser users (cookie auth) and programmatic consumers (Bearer API key)
- Assessment processing is **fully async** — Celery, never blocks API thread
- Files live in S3/MinIO permanently until user deletes them
- **Dual auth** must never break — both cookie and Bearer work on all protected endpoints

---

## 3. Agents Must Follow These Rules

> These override whatever your training data says. Follow them exactly.

| Rule | Why |
|---|---|
| **BE HONEST** — if you don't know, say so. Never hallucinate file paths, function names, or doc content | Wrong information wastes hours of debugging |
| **BE EXPLICIT** — list every file you check, every assumption you make, every gap you find | Future agents need to pick up where you left off |
| **DON'T GUESS** — read the actual file instead of assuming what it contains | Assumptions are the #1 source of bugs |
| **DON'T ASSUME** — never assume a library, function, or pattern exists without verifying in the codebase | The codebase is the source of truth |
| **STOP AND ASK** — if unsure about intent, design, or approach, ask before proceeding | Prevents wasted work |
| **SEARCH WEB** when you lack information about a library, API, or security practice | Don't guess API behavior |
| **Update AGENTS.md session block** when ending a session (see §9) | So next agent doesn't lose context |

**Code rules:**
- No comments in code unless the user asks. The code should be self-documenting
- No emojis in code (docs are fine)
- Prefer editing existing files over creating new ones
- Match existing patterns in the file you're editing (import style, naming, error handling)
- Always check `package.json` or `requirements.txt` before adding a dependency
- Never store raw dataset rows in PostgreSQL (S3 only)
- Never delete from `audit_logs` — PostgreSQL rule silently no-ops it
- Never use ML/neural models in scorers — deterministic rules from YAML only
- Never return partial assessment results on failure — all-or-nothing
- Never hardcode scoring logic in Python — criteria come from `config/domain_criteria.yaml`
- Never set `CORS_ORIGINS = ["*"]` — it breaks `allow_credentials=True`

---

## 4. Doc Authority Hierarchy

> These docs disagree with each other in places. When they do, use this order.

| Priority | Doc | Treat as | Use for |
|---|---|---|---|
| 1 (highest) | `docs/OpenAPI.md` | **Bible** — API contract | Endpoint paths, request/response schemas, field names, status codes |
| 2 | `docs/Questionnaire.md` | **Bible** — metadata schema | Form field names, types, enum values, validation rules |
| 3 | `docs/SECURITY_AUDIT_CHECKLIST.md` | **Bible** — security posture | Every item is a requirement; implement all before production |
| 4 | `docs/BUGS_AND_GAPS.md` | **Action list** — known issues | Fix in priority order before adding new features |
| 5 | `docs/PRD_AIKosh_Dataset_Quality_Toolkit.md` | Reference — business logic | User stories, domain framework, workflow intent |
| 6 (lowest) | `docs/TDD_AIKosh_Dataset_Quality_Toolkit.md` | **Guide only** — aspirational design | Understanding intent; **do not blindly implement from TDD** — code has deviated intentionally |

**When docs disagree with code:**
1. Code wins for runtime behavior (what actually happens)
2. OpenAPI wins for API contract (what should happen)
3. Questionnaire wins for metadata field definitions
4. Fix code to match OpenAPI/Questionnaire unless the code has a good reason (then update the doc)
5. Document any deviation in `docs/BUGS_AND_GAPS.md`

---

## 5. Commands

### Backend (Python 3.10+, FastAPI, Celery)

```powershell
# Run API server (dev, hot-reload)
docker-compose up backend

# Run ALL Celery workers (assessment + webhook) + Flower
docker-compose up worker_assessment worker_webhook flower

# Run full stack
docker-compose up --build

# Run DB migrations inside container
docker exec tkt_backend alembic upgrade head

# Run ALL tests
docker exec tkt_backend pytest -v

# Run a specific test file
docker exec tkt_backend pytest backend/tests/test_auth_bola.py -v --tb=short

# Run SAST security scan (Python)
pip install bandit; bandit -r backend/app/ -ll

# Check Python dependencies for CVEs
pip install pip-audit; pip-audit -r backend/requirements.txt
```

### Frontend (Next.js 14, TypeScript, Tailwind)

```powershell
# Build (catches TypeScript errors)
cd frontend; npm run build

# Dev server
cd frontend; npm run dev

# Check dependencies for CVEs
cd frontend; npm audit --audit-level=high

# TypeScript strict check
cd frontend; npx tsc --noEmit --strict
```

### Database

```powershell
# Create a new migration
docker exec tkt_backend alembic revision --autogenerate -m "description"

# Apply all pending migrations
docker exec tkt_backend alembic upgrade head

# Rollback one step
docker exec tkt_backend alembic downgrade -1

# View migration history
docker exec tkt_backend alembic history
```

---

## 6. E2E Verification Checklist

> Run these after fixing P0/P1 bugs to validate the full pipeline:

| Step | What | How |
|---|---|---|
| Build | `docker-compose build --no-cache` | All images build |
| Start | `docker-compose up -d` | 8 containers healthy |
| Migrate | `docker exec tkt_backend alembic upgrade head` | No errors |
| Register | `POST /api/v1/auth/register` | 201 + cookie |
| Login | `POST /api/v1/auth/login` | 200 + cookie |
| Upload URL | `POST /api/v1/assess/upload-url` | 201 + URL |
| Upload file | `PUT {upload_url}` with test CSV | 200 |
| Submit | `POST /api/v1/assess` with file_key + metadata | 202 + queued |
| Poll | `GET /api/v1/assess/{id}` every 5s | Eventually complete with scores |
| Report | `GET /api/v1/assess/{id}/report?format=html` | 302 → loads |
| BOLA | User A fetches User B's assessment | 403 |
| Admin | Admin fetches any assessment | 403 |
| No auth | `GET /api/v1/assess/` without cookie/bearer | 401 |
| Rate limit | 6 rapid auth POSTs | 429 on 6th |

---

## 7. Key File Map

### Backend

| Path | Purpose |
|---|---|
| `backend/app/main.py` | FastAPI entry point, middleware stack |
| `backend/app/api/v1/auth.py` | Register, login, logout, API key generation |
| `backend/app/api/v1/assess.py` | Upload URL, submit, status poll, list |
| `backend/app/api/v1/reports.py` | Report download redirect |
| `backend/app/api/v1/admin.py` | User management |
| `backend/app/api/v1/health.py` | Health check (postgres, redis, s3) |
| `backend/app/api/deps.py` | Dual auth guard (`get_current_user`, `get_user_assessment`), admin/reviewer guards |
| `backend/app/worker/celery_app.py` | Celery app config (no task_routes — needs fix) |
| `backend/app/worker/tasks.py` | 13-step assessment pipeline |
| `backend/app/engine/domains/base.py` | `BaseDomainScorer` + `DomainScoreResult` |
| `backend/app/engine/domains/` | 15 individual scorers (LIVE code) |
| `backend/app/engine/profiler/profiler.py` | Dataset profiling |
| `backend/app/engine/scoring/cqi.py` | CQI computation |
| `backend/app/engine/scoring/prs.py` | PRS computation |
| `backend/app/engine/scoring/release_classifier.py` | Release classification |
| `backend/app/reports/generator.py` | Report generation (JSON/HTML/PDF) |
| `backend/app/storage/s3_client.py` | S3/MinIO client wrapper |
| `backend/app/integration/aikosh_webhook.py` | Webhook sender (no SSRF protection) |
| `backend/app/audit/logger.py` | Audit event logger |
| `backend/app/schemas/` | Pydantic request/response models |
| `backend/app/models/` | SQLAlchemy ORM models (9 tables) |
| `backend/app/config.py` | Pydantic Settings, env vars |
| `backend/alembic/versions/` | 6 migration files |
| `backend/config/domain_criteria.yaml` | Scoring rules and thresholds |
| `backend/requirements.txt` | Python deps |
| `backend/Dockerfile` | Backend image (no non-root user) |

### Frontend

| Path | Purpose |
|---|---|
| `frontend/app/(auth)/login/page.tsx` | Login page |
| `frontend/app/(auth)/register/page.tsx` | Registration page |
| `frontend/app/(app)/upload/page.tsx` | Assessment submission wizard (8-step form) |
| `frontend/app/(app)/dashboard/[id]/page.tsx` | Assessment results & domain scores |
| `frontend/app/(app)/admin/page.tsx` | User management (admin only) |
| `frontend/lib/api/client.ts` | API client (fetch wrapper) |
| `frontend/lib/types/index.ts` | TypeScript type definitions |
| `frontend/next.config.ts` | Next.js config (check for security headers) |

### Infra

| Path | Purpose |
|---|---|
| `docker-compose.yml` | 8 services (postgres, redis, minio, backend, worker_assessment, worker_webhook, flower, frontend) |
| `k8s/` | Kubernetes manifests (6 yamls, missing MinIO, Flower, NetworkPolicy) |
| `.env.example` | Environment variable template (needs updating for Next.js) |

---

## 8. Known Bugs (must read before any work)

See `docs/BUGS_AND_GAPS.md` for the full audit report. Critical items:

- **P0.1**: `backend/app/engine/domains.py` is dead code with an import error. Delete it
- **P1.1**: Missing `GET /api/v1/assess/{id}/audit` endpoint
- **P1.2**: Missing `GET /api/v1/datasets/{dataset_id}/assessments` endpoint
- **P1.3**: Webhook payload sends flat `{"1": 3}` instead of `{"1_name": {"score": 3, "confidence": "Medium"}}`
- **P1.4**: Missing `inferred` field on `DomainScoreObject`
- **P1.5–P1.12**: See doc for full list

**Fix order: P0 → P1 → P2 → P3 → E2E verify (see §6)**

---

## 9. Session Handoff

> **YOU MUST UPDATE THIS SECTION** before ending your session. Delete the previous agent's entry and add yours.

### Last Agent: [your name]

| Field | Value |
|---|---|
| What I checked | (list files/directories/endpoints/docs you audited) |
| What I fixed | (list files changed, bugs fixed) |
| What I did NOT check | (be explicit — list what you skipped) |
| P0/P1 bugs remaining | (list any unaddressed P0/P1s) |
| Last E2E step | (the last step from §6 that passed) |
| Important context for next agent | (anything confusing, unusual, or risky) |

---

## 10. What NOT To Do

| Never | Why |
|---|---|
| Store raw dataset rows in PostgreSQL | Statistics only. Files live in S3 |
| Delete from `audit_logs` | PostgreSQL rule silently no-ops it |
| Use ML models in scorers | Must be deterministic, auditable, from YAML |
| `allow_origins=["*"]` in CORS | Breaks `allow_credentials=True` |
| Auto-delete files after assessment | User-owned; retained until manual delete |
| Return partial results on failure | All-or-nothing. status="failed" only |
| Hardcode scoring rules in Python | All criteria in `config/domain_criteria.yaml` |
| Break dual-auth model | Both cookie + Bearer must work on every protected endpoint |
| Guess a file's contents | Always `Read` the file first |
| Create new files when existing ones can be edited | Less noise, less drift |
| Assume a library is available | Check `package.json` / `requirements.txt` first |

---

## 11. Dev Philosophy

> *"Build a fully functional, secure, end-to-end pipeline skeleton first — UI → API → Worker → DB/S3 → Polling — then implement real engines one by one. Stability and security before complexity."*

**Priority for new work:**
1. Security and auth correctness always first
2. Pipeline wiring before real scoring logic
3. Real profiler before domain scorers
4. Domain scorers before CQI/PRS engines
5. Dashboard UI after backend results are real

---

*Last updated: 28 Jun 2026 | Agent handoff required***
