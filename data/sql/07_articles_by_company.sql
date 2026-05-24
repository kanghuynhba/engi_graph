select
  a.company,
  count(*) as article_count,
  min(a.created_at) as first_ingested_at,
  max(a.created_at) as latest_ingested_at
from articles a
group by a.company
order by article_count desc, a.company;
