# EngiGraph

EngiGraph is a FastAPI backend for building a RAG-powered knowledge base from engineering blogs. It crawls configured sources, extracts article content, chunks and embeds articles, stores metadata in SQLite, and exposes search/RAG APIs.

## Requirements

- Python 3.13
- uv
- Docker, optional

Install uv if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Local Setup

Install dependencies and create the local virtual environment:

```bash
uv sync
```

Run the API:

```bash
uv run uvicorn app.main:app --reload
```

The API starts at:

```text
http://127.0.0.1:8000
```

Interactive docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Configuration

The app reads environment variables directly or from `.env`.

Useful defaults:

```bash
DATABASE_URL=sqlite:///./data/engigraph.db
VECTOR_STORE=in_memory
EMBEDDER=dummy
LLM_PROVIDER=dummy
MAX_ARTICLE_WORKERS=5
MAX_DB_WRITERS=1
```

Create the data directory before running locally if it does not exist:

```bash
mkdir -p data
```

## Database

On startup, the app initializes the SQLite schema if needed and seeds default categories/sources.

The default database file is:

```text
data/engigraph.db
```

## Common Commands

Check the uv environment:

```bash
uv run python --version
uv run python -c "import fastapi; print(fastapi.__version__)"
uv run python -c "import lxml; print(lxml.__version__)"
```

Compile-check the app:

```bash
uv run python -m compileall app
```

## Ingestion

List seeded sources:

```bash
curl http://127.0.0.1:8000/api/sources
```

Start a background crawl for a source:

```bash
curl -X POST http://127.0.0.1:8000/api/ingestion/sources/1/crawl
```

Check crawl runs:

```bash
curl http://127.0.0.1:8000/api/ingestion/crawl-runs
```

Ingest one URL directly:

```bash
curl -X POST http://127.0.0.1:8000/api/ingestion/articles/ingest-url \
  -H "Content-Type: application/json" \
  -d '{"source_id": 1, "url": "https://example.com/article"}'
```

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

The API is exposed at:

```text
http://127.0.0.1:8000
```

## Project Layout

```text
app/api/          FastAPI routes
app/core/         configuration, database, startup helpers
app/ingestion/    crawling, extraction, chunking, persistence pipeline
app/repositories/ database access
app/services/     application services and factories
app/rag/          query rewriting, retrieval, answer generation
data/             local SQLite data
```
