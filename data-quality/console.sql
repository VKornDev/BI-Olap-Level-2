create table if not exists default.tareLoad
(
    tare_id       UInt64,
    tare_type     String,
    dt            DateTime,
    is_load       UInt8,
    office_id     UInt32,
    office_name   String,
    dst_office_id UInt32 comment 'load>0, unload=0',
    dt_reported   DateTime,
    licence_plate String,
    dt_load       DateTime materialized now()
)
engine = MergeTree()
PARTITION BY toYYYYMMDD(dt)
ORDER BY (is_load, tare_id)
TTL toStartOfDay(dt) + toIntervalDay(90)
SETTINGS index_granularity = 8192, merge_with_ttl_timeout = 72000, ttl_only_drop_parts = 1
;

select *
from tareLoad
order by dt desc
limit 100;

drop table if exists tmp.office_chart;
create table if not exists tmp.office_chart engine=MergeTree() order by(office_id) as
select office_id
     , any(office_name)                                 office_name
     , uniq(tare_id, dt)                                uniq_tares
     , count(tare_id)                                   all_tares
     , all_tares - uniq_tares                           non_uniq_tares
     , uniqIf((tare_id, dt), tare_type = 'CON')         qty_tares_CON
     , uniqIf((tare_id, dt), tare_type = 'TBX')         qty_tares_TBX
     , uniqIf((tare_id, dt), tare_type = 'MPB')         qty_tares_MPB
     , uniqIf((tare_id, dt), tare_type = '')            qty_tares_empty_type
     , countIf(tare_id < 1)                             qty_zero_id
     , countIf(licence_plate = 'б/н' and is_load = 1)   qty_unknown_licence
from tareLoad
where office_id != dst_office_id
  and office_id in (select office_id
                    from tareLoad
                    group by office_id
                    order by uniqIf((tare_id, dt), is_load = 1) desc
                    limit 10)
group by office_id
;

drop table if exists tmp.load_by_hour_chart;
create table if not exists tmp.load_by_hour_chart engine=MergeTree() order by(dt_h, office_id) as
select toStartOfHour(dt)                        dt_h
     , office_id
     , any(office_name)                         office_name
     , uniqIf((tare_id, dt), is_load = 1)       qty_tares
from tareLoad
where office_id != dst_office_id
  and office_id in (select office_id
                    from tareLoad
                    group by office_id
                    order by uniqIf((tare_id, dt), is_load = 1) desc
                    limit 10)
group by office_id, dt_h
;