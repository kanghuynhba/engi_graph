select
  cr.id,
  cr.source_id,
  s.name as source_name,
  s.company,
  cr.status,
  cr.articles_found,
  cr.articles_created,
  cr.articles_updated,
  cr.articles_skipped,
  cr.articles_failed,
  cr.started_at,
  cr.finished_at,
  cr.error_message
from crawl_runs cr
join sources s on s.id = cr.source_id
order by cr.id desc
limit 20;
