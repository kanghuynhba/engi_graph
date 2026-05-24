select 'sources' as table_name, count(*) as row_count from sources
union all
select 'categories', count(*) from categories
union all
select 'articles', count(*) from articles
union all
select 'article_chunks', count(*) from article_chunks
union all
select 'crawl_runs', count(*) from crawl_runs
union all
select 'crawl_items', count(*) from crawl_items
union all
select 'rag_queries', count(*) from rag_queries
union all
select 'rag_results', count(*) from rag_results
order by table_name;
