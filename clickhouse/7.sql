-- Смоделировать вставку данных в буфферную таблицу для stg слоя. В конечном итоге данные должны быть заполнены и в stg слое, и в слое текущих данных.
insert into buffer.tareLoad_buff (tare_id, is_load, dt)
select 114, 1, now()
;

select tare_id
    , is_load
    , dt
from stg.tareLoad
order by dt
;

select *
from current.tares final;