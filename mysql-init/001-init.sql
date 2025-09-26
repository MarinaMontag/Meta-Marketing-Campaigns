CREATE DATABASE IF NOT EXISTS db_airflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'db_user'@'%' IDENTIFIED BY 'db_password';

GRANT ALL PRIVILEGES ON db_app.*     TO 'db_user'@'%';
GRANT ALL PRIVILEGES ON db_airflow.* TO 'db_user'@'%';
FLUSH PRIVILEGES;