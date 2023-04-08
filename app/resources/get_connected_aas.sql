with loads as (select *,
                      row_number() over (partition by al.bunker_id order by al.load_dt desc ) as rn
               from ddl.alumina_load al
               where al.source_bunker_id = :source_id)
select distinct bunker_id
from loads
where rn = 1