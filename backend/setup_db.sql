CREATE DATABASE IF NOT EXISTS campus_db;
CREATE USER IF NOT EXISTS 'campus_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON campus_db.* TO 'campus_user'@'localhost';
FLUSH PRIVILEGES;
