-- Создать роль только для чтения и роль с возможность создавать и заполнять данные в БД стейджинга(stg)
-- Создать двух пользователей с такими правами по умолчанию
create role readonly_role;
grant select on *.* to readonly_role;

create role stg_role;
grant create, insert on stg.* to stg_role;

create user readonly_user identified with sha256_password by 'readonly_password';
grant readonly_role to readonly_user;

create user stg_user identified with sha256_password by 'stg_password';
grant stg_role to stg_user;