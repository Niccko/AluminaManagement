with ordered as (
    select 
        b.bunker_id as bunker_id,
        b.capacity,
        i.value,
        i.measure_dt,
        ROW_NUMBER() OVER (PARTITION BY b.bunker_id ORDER BY i.measure_dt DESC) AS rn
    from ddl.bunker b
    LEFT JOIN ddl.input i
        on b.input_source_id = i.input_source_id
    where b.is_aas = true
)
select 
    o.bunker_id,
    o.capacity,
    o.value,
    o.measure_dt
from ordered o where rn = 1