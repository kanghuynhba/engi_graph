select
  a.id,
  a.company,
  c.name as category_name,
  a.title,
  a.url,
  a.created_at
from articles a
left join categories c on c.id = a.category_id
where lower(coalesce(a.title, '')) like '%' || lower(:term) || '%'
order by a.id desc
limit 50;
