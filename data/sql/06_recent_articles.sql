select
  a.id,
  a.company,
  s.name as source_name,
  c.name as category_name,
  a.status,
  a.title,
  a.url,
  a.published_at,
  a.created_at
from articles a
join sources s on s.id = a.source_id
left join categories c on c.id = a.category_id
order by a.id desc
limit 50;
