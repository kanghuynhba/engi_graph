select
  ci.id,
  ci.crawl_run_id,
  s.name as source_name,
  s.company,
  ci.status,
  ci.retry_count,
  ci.max_retries,
  ci.url,
  ci.error_message,
  ci.last_error_at
from crawl_items ci
join sources s on s.id = ci.source_id
where ci.status in ('failed', 'retry_pending')
order by ci.last_error_at desc, ci.id desc;
