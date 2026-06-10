-- =====================================
-- CATEGORY
-- =====================================

create table CATEGORY(
    category_code int,
    category_name varchar(30) not null
);

alter table CATEGORY
add constraint CATEGORY_PK
primary key(category_code);


-- =====================================
-- MENU
-- =====================================

create table MENU(
    menu_id int not null,
    category_code int not null,
    menu_name varchar(50) not null,
    menu_price int not null
);

alter table MENU
add constraint MENU_PK
primary key(menu_id);

alter table MENU
add constraint MENU_CATEGORY_FK
foreign key(category_code)
references CATEGORY(category_code);


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


______________________________________________________________________

-- =====================================
-- CATEGORY
-- =====================================

insert into CATEGORY values(10,'커피');
insert into CATEGORY values(20,'티');
insert into CATEGORY values(30,'디저트');
insert into CATEGORY values(40,'굿즈');


-- =====================================
-- MENU
-- =====================================

insert into MENU values(1,10,'아메리카노',1500);
insert into MENU values(2,10,'카페라떼',1500);
insert into MENU values(3,20,'복숭아아이스티',2000);
insert into MENU values(4,20,'레몬아이스티',2000);
insert into MENU values(5,30,'쿠키',3000);
insert into MENU values(6,30,'케이크',3000);
insert into MENU values(7,40,'키링',3000);
insert into MENU values(8,40,'텀블러',10000);


-- =====================================
-- OPTION_GROUP
-- =====================================

insert into OPTION_GROUP values(1,'temperature');
insert into OPTION_GROUP values(2,'size');
insert into OPTION_GROUP values(3,'shot');
insert into OPTION_GROUP values(4,'color');
insert into OPTION_GROUP values(5,'cream');


-- =====================================
-- OPTION
-- =====================================

insert into OPTION values(1,1,'차가운',500);
insert into OPTION values(2,1,'뜨거운',0);

insert into OPTION values(3,2,'중간사이즈',0);
insert into OPTION values(4,2,'큰사이즈',500);

insert into OPTION values(5,3,'샷_01',500);
insert into OPTION values(6,3,'샷_02',1000);
insert into OPTION values(7,3,'샷_없음',0);

insert into OPTION values(8,4,'하얀색',0);
insert into OPTION values(9,4,'검정색',0);

insert into OPTION values(10,5,'휘핑크림',500);


-- =====================================
-- MENU_OPTION_GROUP
-- =====================================

insert into MENU_OPTION_GROUP values(1,1);
insert into MENU_OPTION_GROUP values(1,2);
insert into MENU_OPTION_GROUP values(1,3);

insert into MENU_OPTION_GROUP values(2,1);
insert into MENU_OPTION_GROUP values(2,2);
insert into MENU_OPTION_GROUP values(2,3);
insert into MENU_OPTION_GROUP values(2,5);

insert into MENU_OPTION_GROUP values(3,1);
insert into MENU_OPTION_GROUP values(3,2);

insert into MENU_OPTION_GROUP values(4,1);
insert into MENU_OPTION_GROUP values(4,2);

insert into MENU_OPTION_GROUP values(8,4);
-- =====================================
-- MEMBER
-- =====================================

insert into MEMBER values
(1,'01012341234',1,'bronze');

insert into MEMBER values
(2,'01012354567',0,'silver');

insert into MEMBER values
(3,'01055556666',6,'gold');


-- =====================================
-- ORDERS
-- =====================================

insert into ORDERS values
(1001,1,'Y','2026-06-08 10:10:00',9000);

insert into ORDERS values
(1002,2,'Y','2026-06-08 13:00:00',5500);

insert into ORDERS values
(1003,null,'Y','2026-06-10 15:30:00',3000);


-- =====================================
-- ORDER_DETAIL
-- =====================================

-- 주문 1001

insert into ORDER_DETAIL values
(1,1001,1,1,1500,1500);

insert into ORDER_DETAIL values
(2,1001,3,2,2000,4000);

insert into ORDER_DETAIL values
(3,1001,2,1,1500,1500);

-- 주문 1002

insert into ORDER_DETAIL values
(4,1002,1,1,1500,1500);

insert into ORDER_DETAIL values
(5,1002,3,2,2000,4000);

-- 주문 1003

insert into ORDER_DETAIL values
(6,1003,5,1,3000,3000);

-- =====================================
-- ORDER_OPTION
-- =====================================

-- detail_id=1
-- 아메리카노
-- 차가운 + 큰사이즈

insert into ORDER_OPTION values
(1,1,500);

insert into ORDER_OPTION values
(1,4,500);

-- detail_id=2
-- 복숭아아이스티

insert into ORDER_OPTION values
(2,1,500);

insert into ORDER_OPTION values
(2,4,500);

-- detail_id=3
-- 라떼

insert into ORDER_OPTION values
(3,2,0);

insert into ORDER_OPTION values
(3,3,0);

-- detail_id=4
-- 아메리카노

insert into ORDER_OPTION values
(4,2,0);

insert into ORDER_OPTION values
(4,3,0);



-- =====================================
-- PAYMENT
-- =====================================

insert into PAYMENT values
(1,1,1001,9000,'2026-06-08 10:15:00','CARD');

insert into PAYMENT values
(2,2,1002,5500,'2026-06-08 13:05:00','CARD');

insert into PAYMENT values
(3,3,1003,3000,'2026-06-10 15:35:00','CASH');