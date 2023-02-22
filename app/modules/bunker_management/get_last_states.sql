with ordered as (
    select 
        b.bunker_id as bunker_id,
        b.capacity,
        bs.quantity,
        ROW_NUMBER() OVER (PARTITION BY b.bunker_id ORDER BY bs.measure_dt DESC) AS rn
    from ddl.bunker b
    LEFT JOIN ddl.bunker_state bs
        on b.bunker_id = bs.bunker_id
)
select * from ordered where rn = 1