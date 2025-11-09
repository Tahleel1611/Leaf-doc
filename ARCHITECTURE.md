# LeafDoc Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                    http://localhost:5173                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    React Frontend (Vite)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │   Detect    │  │   History    │  │      About         │    │
│  │    Page     │  │     Page     │  │       Page         │    │
│  └──────┬──────┘  └──────┬───────┘  └────────────────────┘    │
│         │                 │                                      │
│         └────────┬────────┘                                      │
│                  │                                               │
│         ┌────────▼──────────┐                                   │
│         │   API Client      │                                   │
│         │  (api-client.ts)  │                                   │
│         └────────┬──────────┘                                   │
└──────────────────┼──────────────────────────────────────────────┘
                   │
                   │ REST API Calls
                   │ (JSON + FormData)
                   │
┌──────────────────▼──────────────────────────────────────────────┐
│              FastAPI Backend (Uvicorn)                           │
│                 http://localhost:8000                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                          │  │
│  │  POST /api/predict    GET /api/history                   │  │
│  │  POST /api/feedback   GET /health                        │  │
│  └────┬──────────────────────┬──────────────────────────────┘  │
│       │                      │                                  │
│  ┌────▼──────┐  ┌───────────▼────────┐  ┌─────────────────┐  │
│  │  Predict  │  │     History        │  │    Feedback     │  │
│  │  Router   │  │     Router         │  │     Router      │  │
│  └────┬──────┘  └───────────┬────────┘  └────────┬────────┘  │
│       │                     │                     │            │
│  ┌────▼─────────────────────▼─────────────────────▼────────┐  │
│  │                   Service Layer                          │  │
│  │  ┌──────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐ │  │
│  │  │Inference │  │ GradCAM │  │ Storage │  │   Tips   │ │  │
│  │  │ Service  │  │ Service │  │ Service │  │ Service  │ │  │
│  │  └────┬─────┘  └────┬────┘  └────┬────┘  └──────────┘ │  │
│  └───────┼─────────────┼────────────┼────────────────────┘  │
│          │             │            │                        │
│  ┌───────▼─────────────▼────────────▼──────────────────┐   │
│  │          Data Access Layer (SQLAlchemy)              │   │
│  │  ┌─────────┐  ┌──────────┐  ┌────────────────────┐  │   │
│  │  │ Models  │  │ Schemas  │  │     Database       │  │   │
│  │  │ (ORM)   │  │(Pydantic)│  │    Connection      │  │   │
│  │  └─────────┘  └──────────┘  └────────────────────┘  │   │
│  └──────────────────────────┬───────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    Persistence Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Database   │  │   Storage    │  │    ML Models       │   │
│  │ (SQLite/PG)  │  │ (Filesystem) │  │  (TorchScript)     │   │
│  │              │  │              │  │                    │   │
│  │ leafdoc.db   │  │ storage/     │  │ models/            │   │
│  │              │  │  ├─images/   │  │  └─mobilev3.ts     │   │
│  │              │  │  └─heatmaps/ │  │                    │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Request Flow

### 1. Image Upload & Prediction

```
User                Frontend              Backend               Database
 │                     │                     │                      │
 │  Upload Image       │                     │                      │
 ├────────────────────>│                     │                      │
 │                     │                     │                      │
 │                     │  POST /api/predict  │                      │
 │                     │  (FormData)         │                      │
 │                     ├────────────────────>│                      │
 │                     │                     │                      │
 │                     │                     │  Save Image          │
 │                     │                     │  storage/images/     │
 │                     │                     │                      │
 │                     │                     │  Run Inference       │
 │                     │                     │  (PyTorch Model)     │
 │                     │                     │                      │
 │                     │                     │  Generate Heatmap    │
 │                     │                     │  storage/heatmaps/   │
 │                     │                     │                      │
 │                     │                     │  Insert Record       │
 │                     │                     ├─────────────────────>│
 │                     │                     │                      │
 │                     │                     │<─────────────────────│
 │                     │                     │  Prediction Saved    │
 │                     │                     │                      │
 │                     │  PredictResponse    │                      │
 │                     │  (JSON)             │                      │
 │                     │<────────────────────┤                      │
 │                     │                     │                      │
 │  Show Results       │                     │                      │
 │<────────────────────┤                     │                      │
 │  (Disease + Tips)   │                     │                      │
 │                     │                     │                      │
```

### 2. View History

```
User                Frontend              Backend               Database
 │                     │                     │                      │
 │  Navigate to        │                     │                      │
 │  History            │                     │                      │
 ├────────────────────>│                     │                      │
 │                     │                     │                      │
 │                     │  GET /api/history   │                      │
 │                     │  ?page=1&limit=20   │                      │
 │                     ├────────────────────>│                      │
 │                     │                     │                      │
 │                     │                     │  Query Predictions   │
 │                     │                     │  JOIN Feedback       │
 │                     │                     ├─────────────────────>│
 │                     │                     │                      │
 │                     │                     │<─────────────────────│
 │                     │                     │  Results (paginated) │
 │                     │                     │                      │
 │                     │  HistoryResponse    │                      │
 │                     │  (JSON)             │                      │
 │                     │<────────────────────┤                      │
 │                     │                     │                      │
 │  Display Table      │                     │                      │
 │<────────────────────┤                     │                      │
 │                     │                     │                      │
```

### 3. Submit Feedback

```
User                Frontend              Backend               Database
 │                     │                     │                      │
 │  Click "Incorrect"  │                     │                      │
 ├────────────────────>│                     │                      │
 │                     │                     │                      │
 │                     │  POST /api/feedback │                      │
 │                     │  {id, correct,      │                      │
 │                     │   true_label}       │                      │
 │                     ├────────────────────>│                      │
 │                     │                     │                      │
 │                     │                     │  Validate Prediction │
 │                     │                     ├─────────────────────>│
 │                     │                     │                      │
 │                     │                     │<─────────────────────│
 │                     │                     │  Prediction Found    │
 │                     │                     │                      │
 │                     │                     │  Insert/Update       │
 │                     │                     │  Feedback            │
 │                     │                     ├─────────────────────>│
 │                     │                     │                      │
 │                     │                     │<─────────────────────│
 │                     │                     │  Feedback Saved      │
 │                     │                     │                      │
 │                     │  HistoryItem        │                      │
 │                     │  (with feedback)    │                      │
 │                     │<────────────────────┤                      │
 │                     │                     │                      │
 │  Show Success       │                     │                      │
 │<────────────────────┤                     │                      │
 │                     │                     │                      │
```

## Technology Stack

```
┌───────────────────────────────────────────────────────────┐
│                      Frontend                              │
│                                                            │
│  Framework:    React 18 + TypeScript                      │
│  Build Tool:   Vite                                       │
│  Styling:      Tailwind CSS + shadcn/ui                  │
│  State:        TanStack Query (React Query)              │
│  HTTP Client:  Fetch API                                 │
│  Router:       React Router                              │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                      Backend                               │
│                                                            │
│  Framework:    FastAPI 0.104+                             │
│  Server:       Uvicorn (ASGI)                             │
│  ML:           PyTorch 2.1, TorchVision                   │
│  Database:     SQLAlchemy 2.0                             │
│  Migrations:   Alembic                                    │
│  Validation:   Pydantic 2.5                               │
│  Image Proc:   PIL, OpenCV                                │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                    Data Storage                            │
│                                                            │
│  Database:     SQLite (dev) / PostgreSQL (prod)           │
│  Files:        Local filesystem                           │
│  Models:       TorchScript (.ts files)                    │
└───────────────────────────────────────────────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  1. CORS Policy                                          │
│     Allow specific frontend origins                      │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│  2. Input Validation                                     │
│     - Pydantic schemas validate all inputs               │
│     - File type checking (images only)                   │
│     - Size limits on uploads                             │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│  3. SQL Injection Prevention                             │
│     - SQLAlchemy ORM (parameterized queries)            │
│     - No raw SQL execution                               │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│  4. Error Handling                                       │
│     - Consistent error responses                         │
│     - No sensitive data in errors                        │
│     - Request ID tracking                                │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture (Production)

```
Internet
    │
    │ HTTPS
    │
┌───▼────────────────┐
│  Reverse Proxy     │
│  (Nginx/Caddy)     │
│  - SSL/TLS         │
│  - Rate Limiting   │
└──┬─────────────┬───┘
   │             │
   │             │
   ▼             ▼
┌──────────┐  ┌──────────┐
│ Frontend │  │ Backend  │
│ (Static) │  │ (Uvicorn)│
│  Vercel  │  │  Railway │
└──────────┘  └────┬─────┘
                   │
                   ▼
             ┌──────────┐
             │PostgreSQL│
             │  Server  │
             └──────────┘
```

---

**Legend:**

- `─>` HTTP Request
- `<─` HTTP Response
- `├─>` Database Query
- `│` Data Flow
