# EngiGraph Query Commands

Set the API base URL once:

```bash
export API_URL=http://127.0.0.1:8000
```

## App

Run locally:

```bash
uv run uvicorn app.main:app --reload
```

Open API docs:

```bash
open "$API_URL/docs"
```

## Sources And Categories

List sources:

```bash
curl "$API_URL/api/sources"
```

List categories:

```bash
curl "$API_URL/api/categories"
```

Create a feed source:

```bash
curl -X POST "$API_URL/api/sources" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Engineering Blog",
    "company": "Example",
    "base_url": "https://example.com/engineering",
    "feed_url": "https://example.com/engineering/feed.xml",
    "allowed_domains": ["example.com"],
    "crawl_mode": "feed",
    "enabled": true
  }'
```

Create an HTML index source:

```bash
curl -X POST "$API_URL/api/sources" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Engineering Index",
    "company": "Example",
    "base_url": "https://example.com/engineering",
    "allowed_domains": ["example.com"],
    "crawl_mode": "html_index",
    "enabled": true
  }'
```

## Ingestion

Start a background crawl for source `1`:

```bash
curl -X POST "$API_URL/api/ingestion/sources/1/crawl"
```

List crawl runs:

```bash
curl "$API_URL/api/ingestion/crawl-runs"
```

Get one crawl run:

```bash
curl "$API_URL/api/ingestion/crawl-runs/1"
```

Ingest one URL directly:

```bash
curl -X POST "$API_URL/api/ingestion/articles/ingest-url" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": 1,
    "url": "https://example.com/engineering/example-article"
  }'
```

## Articles

List articles:

```bash
curl "$API_URL/api/articles?limit=20&offset=0"
```

Get article details:

```bash
curl "$API_URL/api/articles/1"
```

Get article chunks:

```bash
curl "$API_URL/api/articles/1/chunks"
```

Delete an article:

```bash
curl -X DELETE "$API_URL/api/articles/1"
```

## Search

Search chunks:

```bash
curl -X POST "$API_URL/api/search/chunks" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "database sharding architecture",
    "top_k": 5
  }'
```

Search chunks with filters:

```bash
curl -X POST "$API_URL/api/search/chunks" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "edge caching and CDN reliability",
    "companies": ["Cloudflare"],
    "category_names": ["Content Delivery / CDN", "Reliability / Resilience"],
    "top_k": 10
  }'
```

Search articles:

```bash
curl -X POST "$API_URL/api/search/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "stream processing data platform",
    "top_k": 10
  }'
```

Get the best matching full article:

```bash
curl -X POST "$API_URL/api/search/full-article" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how Netflix handles distributed systems reliability",
    "companies": ["Netflix"],
    "top_k": 5
  }'
```

## RAG

Ask a general question:

```bash
curl -X POST "$API_URL/api/rag/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are common patterns for reliable distributed systems?",
    "top_k": 8,
    "return_sources": true
  }'
```

Ask with filters:

```bash
curl -X POST "$API_URL/api/rag/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do companies optimize API latency?",
    "companies": ["Uber", "Cloudflare"],
    "category_names": ["Performance Optimization", "Infrastructure"],
    "top_k": 8,
    "return_sources": true
  }'
```

Preview the query plan:

```bash
curl -X POST "$API_URL/api/rag/query-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Find articles about observability for distributed systems",
    "top_k": 5
  }'
```

Ask a question against one article:

```bash
curl -X POST "$API_URL/api/rag/answer-from-article/1" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Summarize the main engineering lesson from this article.",
    "return_sources": true
  }'
```

## Local SQLite Checks

Count rows in the local database:

```bash
sqlite3 data/engigraph.db '
select "sources", count(*) from sources
union all select "categories", count(*) from categories
union all select "articles", count(*) from articles
union all select "article_chunks", count(*) from article_chunks
union all select "crawl_runs", count(*) from crawl_runs;
'
```

Show recent crawl runs:

```bash
sqlite3 -header -column data/engigraph.db '
select id, source_id, status, articles_found, articles_created, articles_skipped, articles_failed, started_at, finished_at
from crawl_runs
order by id desc
limit 10;
'
```

Show recent articles:

```bash
sqlite3 -header -column data/engigraph.db '
select id, company, title, url, created_at
from articles
order by id desc
limit 10;
'
```
