select
  c.id,
  c.name,
  c.slug,
  c.created_by,
  count(a.id) as article_count
from categories c
left join articles a on a.category_id = c.id
group by c.id, c.name, c.slug, c.created_by
order by article_count desc, c.name;
