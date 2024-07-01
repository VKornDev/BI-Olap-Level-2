-- Настроить пользователя администратора
create user admin_user identified with sha256_password by 'password';
grant current grants on *.* to admin_user with grant option;