select
  a.id as article_id,
  a.company,
  a.title,
  count(ac.id) as chunk_count,
  sum(case when ac.vector_id is null then 1 else 0 end) as chunks_missing_vector_id
from articles a
join article_chunks ac on ac.article_id = a.id
group by a.id, a.company, a.title
having chunks_missing_vector_id > 0
order by chunks_missing_vector_id desc, a.id desc;
