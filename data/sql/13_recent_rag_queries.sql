select
  id,
  original_query,
  rewritten_query,
  intent,
  return_type,
  filters_json,
  created_at
from rag_queries
order by id desc
limit 50;
