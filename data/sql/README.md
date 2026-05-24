# SQL Query Files

These files are read-only SQLite queries for inspecting the local EngiGraph database with `litecli` or `sqlite3`.

Open the database:

```bash
litecli data/engigraph.db
```

Run a query file from inside `litecli`:

```sql
\i data/sql/03_recent_crawl_runs.sql
```

Queries that use parameters, such as `:term`, can be run in `sqlite3` with `.parameter`:

```bash
sqlite3 data/engigraph.db
```

```sql
.parameter set :term latency
.read data/sql/11_search_articles_by_title.sql
```

Useful starting points:

- `00_table_counts.sql`
- `01_sources.sql`
- `03_recent_crawl_runs.sql`
- `05_failed_crawl_items.sql`
- `06_recent_articles.sql`
- `11_search_articles_by_title.sql`
- `12_search_chunks_by_text.sql`
