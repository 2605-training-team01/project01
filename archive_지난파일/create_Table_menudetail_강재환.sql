--mysql -u kiosk -p
--Enter password: kiosk1234

--show databases;
--use kiosk
--show tables;


drop table if exists menu_detail;

create table menu_detail (
    menu_code int AUTO_INCREMENT PRIMARY KEY,
    name varchar(20) not null,           
    price DECIMAL(15, 0) not null,  -- 소수점 없는 정수형. 최대 100조 원(999조)까지
    menu_category_id int(2)
    constraint MENU_CATEGOTY_ID FOREIGN KEY (menu_category_id)
    REFERENCES main_menu (menu_category_id)
) engine=innodb default charset=utf8mb4;