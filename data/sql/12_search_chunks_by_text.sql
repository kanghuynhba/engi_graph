select
  ac.id as chunk_id,
  ac.article_id,
  a.company,
  a.title,
  ac.chunk_index,
  ac.token_count,
  substr(ac.text, 1, 400) as text_preview
from article_chunks ac
join articles a on a.id = ac.article_id
where lower(ac.text) like '%' || lower(:term) || '%'
order by a.id desc, ac.chunk_index
limit 50;
