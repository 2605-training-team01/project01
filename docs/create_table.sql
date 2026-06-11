-- mysql -u kiosk -p
-- use kiosk 

-- DROP TABLE
drop table if EXISTS payment;
drop table if EXISTS order_option;
drop table if EXISTS order_detail;
drop table if EXISTS orders;
drop table if EXISTS member;
drop table if EXISTS menu_option_group;
drop table if EXISTS option;
drop table if EXISTS option_group;
drop table if EXISTS menu;
drop table if EXISTS category;

-- 강유진 start

-- =====================================
-- CATEGORY
-- =====================================


create table CATEGORY(
    category_code int AUTO_INCREMENT PRIMARY KEY,
    category_name varchar(30) not null
);

-- =====================================
-- MENU
-- =====================================
CREATE TABLE MENU (
    menu_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    category_code INT NOT NULL,
    menu_name VARCHAR(50) NOT NULL,
    menu_price INT NOT NULL,

    CONSTRAINT MENU_CATEGORY_FK
    FOREIGN KEY (category_code)
    REFERENCES CATEGORY(category_code)
);

-- =====================================
-- OPTION_GROUP
-- =====================================

create table OPTION_GROUP(
    group_id int,
    group_name varchar(30) not null
);

alter table OPTION_GROUP
add constraint OPTION_GROUP_PK
primary key(group_id);


-- =====================================
-- OPTION
-- =====================================

create table OPTION(
    option_id int,
    group_id int,
    option_name varchar(50) not null,
    extra_price int default 0
);

alter table OPTION
add constraint OPTION_PK
primary key(option_id);

alter table OPTION
add constraint OPTION_GROUP_FK
foreign key(group_id)
references OPTION_GROUP(group_id);


-- =====================================
-- MENU_OPTION_GROUP
-- =====================================


create table MENU_OPTION_GROUP(
    menu_id int,
    group_id int
);

alter table MENU_OPTION_GROUP
add constraint MENU_OPTION_GROUP_PK
primary key(menu_id, group_id);

alter table MENU_OPTION_GROUP
add constraint MOG_MENU_FK
foreign key(menu_id)
references MENU(menu_id);
#mog는 menu option group의 줄임말입니당

alter table MENU_OPTION_GROUP
add constraint MOG_GROUP_FK
foreign key(group_id)
references OPTION_GROUP(group_id);
-- 강유진 end

-- 박종민 start
create table member(
	member_id INT,
	phone_number VARCHAR(11) Not Null,
	stamp INT DEFAULT 0,
	grade VARCHAR(20)
	);

ALTER TABLE member
ADD CONSTRAINT member_pk
PRIMARY KEY(member_id);

-- 박종민 end

-- 서지윤 start
-- 주문
CREATE TABLE orders (
    order_id       INT PRIMARY KEY AUTO_INCREMENT,
    member_id      INT NULL,
    takeout_type   CHAR(1) NOT NULL,   -- Y/N
    order_date     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount   DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_orders_member
        FOREIGN KEY (member_id)
        REFERENCES member(member_id)
);

-- 주문 상세
CREATE TABLE order_detail (
    detail_id      INT PRIMARY KEY AUTO_INCREMENT,
    order_id       INT NOT NULL,
    menu_id        INT NOT NULL,
    quantity       INT NOT NULL,
    menu_price     DECIMAL(10,2) NOT NULL, -- 주문 당시 메뉴 가격
    amount         DECIMAL(10,2) NOT NULL, -- menu_price * quantity

    CONSTRAINT fk_order_detail_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_detail_menu
        FOREIGN KEY (menu_id)
        REFERENCES menu(menu_id)
);

-- 주문 옵션
CREATE TABLE order_option (
    detail_id      INT NOT NULL,
    option_id      INT NOT NULL,
    option_price   DECIMAL(10,2) NOT NULL, -- 주문 당시 옵션 가격

    PRIMARY KEY (detail_id, option_id),

    CONSTRAINT fk_order_option_detail
        FOREIGN KEY (detail_id)
        REFERENCES order_detail(detail_id),

    CONSTRAINT fk_order_option_option
        FOREIGN KEY (option_id)
        REFERENCES option(option_id)
);
-- 서지윤 end


-- 이경진 start
CREATE TABLE payment (
pay_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '결제번호',
member_id INT NOT NULL COMMENT '회원번호',
order_id INT NOT NULL COMMENT '주문번호',
final_amt DECIMAL(15,0) NOT NULL COMMENT '총결제금액',
pay_date DATE NOT NULL COMMENT '결제일자',
pay_type VARCHAR(10) NOT NULL COMMENT '결제방법',
CONSTRAINT fk_payment_member
FOREIGN KEY (member_id)
REFERENCES member(member_id),
CONSTRAINT fk_payment_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id)
);

CREATE INDEX idx_payment_member
ON payment(member_id);
CREATE INDEX idx_payment_order
ON payment(order_id);
-- 이경진 end