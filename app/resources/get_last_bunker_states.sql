with bunkers as (select *
                 from ddl.bunker
                 where 1 = 1
                   AND is_aas = :is_aas
                   AND deleted_flg = False),
     ordered as (select b.bunker_id as bunker_id,
                        b.capacity,
                        bs.quantity,
                        bs.measure_dt,
                        ROW_NUMBER()   OVER (PARTITION BY b.bunker_id ORDER BY bs.measure_dt DESC) AS rn
                 from bunkers b
                          LEFT JOIN ddl.bunker_state bs
                                    on b.bunker_id = bs.bunker_id
                 where (:include_est = 1 or bs.is_estimate = (:include_est = 2)))

select o.bunker_id,
       o.capacity,
       o.quantity,
       o.measure_dt
from ordered o
where rn = 1