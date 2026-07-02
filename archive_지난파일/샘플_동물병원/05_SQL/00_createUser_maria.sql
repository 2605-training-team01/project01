--mysql -u root -p
--Enter password: 1234

drop user if exists 'project'@'localhost';

create user 'project'@'localhost' identified by 'java';
--create database modeling_schema;

grant all privileges on modeling_schema.* to 'project'@'localhost';
flush privileges;

exit;
