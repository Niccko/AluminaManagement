with pre_last_load as (select bunker_id, MAX(load_dt) as last_load_dt
                       from ddl.alumina_load
                       group by bunker_id),
     avgs as (select bs.bunker_id,
                     AVG(extract(epoch from measure_dt)) as avg_time,
                     AVG(quantity)                       as avg_quantity
              from ddl.bunker_state bs
              join pre_last_load ON pre_last_load.bunker_id = bs.bunker_id
              where measure_dt > pre_last_load.last_load_dt
              group by bs.bunker_id),
     linear as (select bs.bunker_id,
                       sum((extract(epoch from measure_dt) - a.avg_time)),
                       sum(quantity - a.avg_quantity),
                        sum((extract(epoch from measure_dt) - a.avg_time) * (quantity - a.avg_quantity)) /
                        sum(pow(extract(epoch from measure_dt) - a.avg_time, 2)) as a_coeff
                from ddl.bunker_state bs
                         join avgs a
                              on bs.bunker_id = a.bunker_id
                GROUP BY bs.bunker_id
                )
-- select a.bunker_id,
--        l.a_coeff,
--        -(a.avg_quantity - l.a_coeff * a.avg_time) / l.a_coeff
-- from avgs a
--          join linear l
--               on a.bunker_id = l.bunker_id
select floor(extract(epoch from measure_dt)), quantity
from ddl.bunker_state
where bunker_id = 6
order by measure_dt desc




