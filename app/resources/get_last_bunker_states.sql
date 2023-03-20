with bunkers as (select *
                 from ddl.bunker
                 where is_aas = false),
     ordered as (select b.bunker_id as bunker_id,
                        b.capacity,
                        bs.quantity,
                        ROW_NUMBER()   OVER (PARTITION BY b.bunker_id ORDER BY bs.measure_dt DESC) AS rn
                 from bunkers b
                          LEFT JOIN ddl.bunker_state bs
                                    on b.bunker_id = bs.bunker_id)
select o.bunker_id,
       o.capacity,
       o.quantity
from ordered o
where rn = 1