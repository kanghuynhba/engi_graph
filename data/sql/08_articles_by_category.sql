select
  coalesce(c.name, 'Uncategorized') as category_name,
  count(*) as article_count
from articles a
left join categories c on c.id = a.category_id
group by coalesce(c.name, 'Uncategorized')
order by article_count desc, category_name;
