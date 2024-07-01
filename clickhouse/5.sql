-- Реализовать через буфферную таблицу заполнение stg слоя
create table if not exists stg.tareLoad
(
    tare_id     UInt64,
    is_load     UInt8,
    dt          DateTime
)
engine = MergeTree()
order by (is_load, tare_id);

create table if not exists buffer.tareLoad_buff
(
    tare_id     UInt64,
    is_load     UInt8,
    dt          DateTime
)
engine = Buffer(stg, tareLoad, 16, 1, 10, 10000, 1000000, 10000000, 100000000);