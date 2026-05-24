select
  id,
  name,
  company,
  crawl_mode,
  enabled,
  base_url,
  feed_url,
  allowed_domains,
  created_at
from sources
order by id;
