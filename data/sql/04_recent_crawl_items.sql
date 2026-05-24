select
  ci.id,
  ci.crawl_run_id,
  ci.source_id,
  s.company,
  ci.status,
  ci.article_id,
  ci.retry_count,
  ci.max_retries,
  ci.url,
  ci.error_message,
  ci.created_at,
  ci.last_error_at
from crawl_items ci
join sources s on s.id = ci.source_id
order by ci.id desc
limit 50;
