select
  a.id as article_id,
  a.company,
  a.title,
  count(ac.id) as chunk_count,
  sum(ac.token_count) as total_tokens,
  round(avg(ac.token_count), 1) as avg_chunk_tokens,
  min(ac.token_count) as min_chunk_tokens,
  max(ac.token_count) as max_chunk_tokens
from articles a
left join article_chunks ac on ac.article_id = a.id
group by a.id, a.company, a.title
order by a.id desc
limit 50;
