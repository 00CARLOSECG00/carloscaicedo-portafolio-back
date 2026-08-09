# Carlos Caicedo Portfolio — Backend API

FastAPI backend for the [carloscaicedo-portfolio](../carloscaicedo-portfolio) frontend. Implements every REST endpoint documented in the frontend's `endpoints.txt`.

## What this backend provides

| Feature | Endpoints | External service |
|---------|-----------|------------------|
| AI Assistant | `POST /api/ai/chat` | [Groq Cloud](https://console.groq.com) (free tier) |
| NLP Playground | `POST /api/nlp/*` | TextBlob, langdetect, YAKE (local) |
| Database Lab | `GET/POST /api/databases/*` | In-memory dataset (optional Supabase) |
| Knowledge Graph | `GET /api/knowledge-graph` | Supabase PostgreSQL or static data |

---

## Quick start (Docker Compose)

### 1. Configure environment

```bash
cd Back
cp .env.example .env
```

Edit `.env` and add at minimum your **Groq API key** (for the AI assistant):

```env
GROQ_API_KEY=gsk_your_key_here
```

### 2. Run with Docker

```bash
docker compose up --build
```

API available at:

- **Base URL:** http://localhost:8000
- **Swagger docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

### 3. Connect the frontend

In `carloscaicedo-portfolio`, create or edit `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Then run the frontend:

```bash
cd ../carloscaicedo-portfolio
pnpm install
pnpm dev
```

Open http://localhost:3000 — all features will use the live backend.

---

## Local development (without Docker)

Requirements: Python 3.12+

```bash
cd Back
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m textblob.download_corpora lite

cp .env.example .env
# Edit .env with your keys

uvicorn app.main:app --reload --port 8000
```

---

## Deploy to Vercel

This backend is configured for Vercel serverless via `vercel.json` and `api/index.py` (Mangum ASGI adapter).

### Steps

1. Push the `Back` folder to a Git repository (or deploy as a separate Vercel project).

2. In [Vercel Dashboard](https://vercel.com/dashboard) → **New Project** → import the repo.

3. Set **Root Directory** to `Back` (if the repo contains both frontend and backend).

4. Add **Environment Variables** (Settings → Environment Variables):

   | Variable | Required | Description |
   |----------|----------|-------------|
   | `GROQ_API_KEY` | Yes (for AI) | Groq Cloud API key |
   | `GROQ_MODEL` | No | Default: `llama-3.3-70b-versatile` |
   | `SUPABASE_URL` | No | Supabase project URL |
   | `SUPABASE_SERVICE_KEY` | No | Supabase service role key |
   | `CORS_ORIGINS` | Yes | Your frontend URL(s), comma-separated |
   | `USE_GROQ_AI` | No | `true` / `false` |
   | `USE_SUPABASE_KNOWLEDGE` | No | `true` / `false` |

5. Deploy. Your API URL will be something like:

   ```
   https://your-backend.vercel.app
   ```

6. In the **frontend** Vercel project, set:

   ```env
   NEXT_PUBLIC_API_BASE_URL=https://your-backend.vercel.app
   ```

### Vercel notes

- NLP libraries (TextBlob, YAKE) work on Vercel but cold starts may be slower on the free tier.
- If NLP times out, the frontend falls back to local heuristics automatically.
- For heavy workloads, consider Railway, Render, or Fly.io with the same Docker image.

---

## External services setup

### 1. Groq Cloud (AI Assistant) — **Recommended**

The AI chat uses Groq's free tier for fast LLM inference.

1. Go to https://console.groq.com and create an account.
2. Navigate to **API Keys** → **Create API Key**.
3. Copy the key into `.env`:

   ```env
   GROQ_API_KEY=gsk_xxxxxxxx
   GROQ_MODEL=llama-3.3-70b-versatile
   USE_GROQ_AI=true
   ```

4. On Vercel, add the same variables in **Project Settings → Environment Variables**.

**Without Groq:** the backend still works using intent-based fallback responses (same logic as the frontend mock).

**Security:** never put `GROQ_API_KEY` in the frontend. Only the backend uses it.

---

### 2. Supabase (Knowledge Graph + future RAG) — **Optional**

Supabase provides free PostgreSQL hosting. Use it to store the knowledge graph and optionally conversation history.

#### Create project

1. Go to https://supabase.com/dashboard → **New project**.
2. Choose a name, password, and region (pick one close to your users).
3. Wait for the database to provision (~2 minutes).

#### Get credentials

In **Project Settings → API**:

| Field | Env variable |
|-------|--------------|
| Project URL | `SUPABASE_URL` |
| `service_role` key (secret) | `SUPABASE_SERVICE_KEY` |

In **Project Settings → Database → Connection string**:

| Field | Env variable |
|-------|--------------|
| URI (Session mode) | `DATABASE_URL` |

> Use the **service_role** key only on the backend. Never expose it in the frontend.

#### Run database migrations

1. Open **SQL Editor** in Supabase.
2. Paste and run `supabase/schema.sql`.
3. Paste and run `supabase/seed.sql`.

#### Enable in backend

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOi...
USE_SUPABASE_KNOWLEDGE=true
```

The backend reads `knowledge_nodes` and `knowledge_edges` tables. If Supabase is unavailable, it falls back to static data automatically.

#### Future: RAG with pgvector

The schema includes commented SQL for `pgvector` embeddings. To enable:

1. In Supabase SQL Editor: `CREATE EXTENSION IF NOT EXISTS vector;`
2. Uncomment the `document_embeddings` table in `schema.sql`.
3. Extend `app/services/ai_service.py` to retrieve context before calling Groq.

---

### 3. Database Lab data

The Database Lab uses an in-memory fictional dataset (`app/data/dataset.py`) — the same data as the frontend fallback. No external database is required.

To persist this data in Supabase later, set `USE_SUPABASE_DATABASES=true` and extend `database_service.py`.

---

## API endpoints

All paths are prefixed with `/api` (configurable via `API_PREFIX`).

```
GET  /health
POST /api/ai/chat
POST /api/nlp/sentiment
POST /api/nlp/emotion
POST /api/nlp/language
POST /api/nlp/keywords
POST /api/nlp/entities
POST /api/nlp/summarize
GET  /api/databases/relational
GET  /api/databases/document
GET  /api/databases/columnar
GET  /api/databases/key-value
POST /api/databases/vector/search
GET  /api/databases/graph
GET  /api/databases/geospatial
GET  /api/knowledge-graph
GET  /api/knowledge-graph/nodes/{id}
```

Full contracts: see `carloscaicedo-portfolio/endpoints.txt`.

Interactive docs: http://localhost:8000/docs

---

## Environment variables reference

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `development` or `production` |
| `API_PREFIX` | `/api` | Route prefix for all API endpoints |
| `CORS_ORIGINS` | `localhost:3000` | Comma-separated allowed frontend origins |
| `GROQ_API_KEY` | — | Groq API key (server-side only) |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model name |
| `USE_GROQ_AI` | `true` | Enable Groq for AI chat |
| `SUPABASE_URL` | — | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | — | Supabase service role key |
| `DATABASE_URL` | — | Direct Postgres connection string |
| `USE_SUPABASE_KNOWLEDGE` | `true` | Load knowledge graph from Supabase |
| `USE_SUPABASE_DATABASES` | `false` | Load database lab from Supabase |
| `MAX_NLP_INPUT_LENGTH` | `4000` | Max characters for NLP input |
| `MAX_AI_MESSAGE_LENGTH` | `4000` | Max characters for AI messages |

---

## Project structure

```
Back/
├── app/
│   ├── main.py              # FastAPI app + CORS
│   ├── config.py            # Settings from env vars
│   ├── api/                 # Route handlers
│   │   ├── ai.py
│   │   ├── nlp.py
│   │   ├── databases.py
│   │   └── knowledge.py
│   ├── models/
│   │   └── schemas.py       # Pydantic models (API contracts)
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # Groq + intent fallback
│   │   ├── nlp_service.py   # TextBlob, langdetect, YAKE
│   │   ├── database_service.py
│   │   └── knowledge_service.py
│   └── data/                # Static dataset + knowledge
├── api/
│   └── index.py             # Vercel serverless entry
├── supabase/
│   ├── schema.sql           # PostgreSQL tables
│   └── seed.sql             # Knowledge graph seed data
├── docker-compose.yml
├── Dockerfile
├── vercel.json
├── requirements.txt
├── .env.example
└── README.md
```

---

## Troubleshooting

### CORS errors in the browser

Add your frontend URL to `CORS_ORIGINS`:

```env
CORS_ORIGINS=http://localhost:3000,https://your-portfolio.vercel.app
```

### AI returns fallback responses instead of Groq

- Verify `GROQ_API_KEY` is set and `USE_GROQ_AI=true`.
- Check logs: `docker compose logs -f api`
- Test Groq key at https://console.groq.com

### Supabase knowledge graph empty

- Run `schema.sql` and `seed.sql` in Supabase SQL Editor.
- Verify `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`.
- Backend falls back to static data if Supabase fails — the frontend still works.

### NLP slow on Vercel cold start

Normal on serverless free tier. Options:

- Use Docker on Railway/Render for always-on instances.
- Frontend automatically falls back to local NLP heuristics on timeout.

### Frontend still uses fallback data

- Confirm `NEXT_PUBLIC_API_BASE_URL` points to the backend (no trailing slash).
- Restart the Next.js dev server after changing `.env.local`.
- Check browser Network tab for requests to `/api/*`.

---

## Checklist before going live

- [ ] `GROQ_API_KEY` set in Vercel backend project
- [ ] `CORS_ORIGINS` includes your frontend Vercel URL
- [ ] `NEXT_PUBLIC_API_BASE_URL` set in frontend Vercel project
- [ ] Supabase schema + seed executed (optional)
- [ ] Test `/health` and `/docs` on deployed backend
- [ ] Test AI chat, NLP, Database Lab, Knowledge Graph from live frontend
