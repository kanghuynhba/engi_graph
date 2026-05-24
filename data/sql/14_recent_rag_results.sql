select
  rr.id,
  rr.rag_query_id,
  rq.original_query,
  rr.rank,
  rr.score,
  rr.result_type,
  rr.article_id,
  a.company,
  a.title,
  rr.chunk_id,
  rr.created_at
from rag_results rr
join rag_queries rq on rq.id = rr.rag_query_id
join articles a on a.id = rr.article_id
order by rr.id desc
limit 100;
