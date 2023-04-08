select sum(fd.quantity)
from ddl.alumina_feed fd
JOIN ddl.bunker b ON 1=1
    AND b.bunker_id = fd.bunker_id
    AND fd.feed_dt > :load_time
    AND b.bunker_id IN (:connected_aas)