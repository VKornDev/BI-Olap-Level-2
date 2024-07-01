-- Создать матереализованное представление для перемещения данных из stg слоя в слой текущих данных
create table if not exists current.tares
(
    tare_id     UInt64,
    is_load     UInt8,
    dt          DateTime
)
engine ReplacingMergeTree()
order by tare_id;

create materialized view stg.tareLoad_view to current.tares as
select tare_id, is_load, dt
from stg.tareLoad;