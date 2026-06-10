--mysql -u root -p

-- create User
drop user if exists 'kiosk'@'localhost';
create user 'kiosk'@'localhost' IDENTIFIED BY 'kiosk1234';

-- create Database
drop database if exists kiosk;
CREATE DATABASE kiosk;

-- grant CRUD
GRANT ALL PRIVILEGES ON kiosk.* to 'kiosk'@'localhost';

FLUSH PRIVILEGES;