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

create table MENU(
    menu_id int,
    category_code int,
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

create table OPTION_TB(
    option_id int,
    group_id int,
    option_name varchar(50) not null,
    extra_price int default 0,
    is_active char(1) default 'Y'
);

alter table OPTION_TB
add constraint OPTION_PK
primary key(option_id);

alter table OPTION_TB
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

alter table MENU_OPTION_GROUP
add constraint MOG_GROUP_FK
foreign key(group_id)
references OPTION_GROUP(group_id);


-- =====================================
-- MEMBER
-- =====================================

create table MEMBER(
    member_id int,
    phone_number varchar(20) unique,
    stamp int default 0,
    grade varchar(20),
    created_at date default current_date
);

alter table MEMBER
add constraint MEMBER_PK
primary key(member_id);


-- =====================================
-- ORDERS
-- =====================================

create table ORDERS(
    order_id int,
    member_id int null,
    takeout_type char(1),
    order_date datetime,
    total_amount int
);

alter table ORDERS
add constraint ORDERS_PK
primary key(order_id);

alter table ORDERS
add constraint ORDERS_MEMBER_FK
foreign key(member_id)
references MEMBER(member_id);


-- =====================================
-- ORDER_DETAIL
-- =====================================

create table ORDER_DETAIL(
    detail_id int,
    order_id int,
    menu_id int,
    quantity int,
    menu_price int,
    amount int
);

alter table ORDER_DETAIL
add constraint ORDER_DETAIL_PK
primary key(detail_id);

alter table ORDER_DETAIL
add constraint OD_ORDER_FK
foreign key(order_id)
references ORDERS(order_id);

alter table ORDER_DETAIL
add constraint OD_MENU_FK
foreign key(menu_id)
references MENU(menu_id);


-- =====================================
-- ORDER_OPTION
-- =====================================

create table ORDER_OPTION(
    detail_id int,
    option_id int,
    option_price int
);

alter table ORDER_OPTION
add constraint ORDER_OPTION_PK
primary key(detail_id, option_id);

alter table ORDER_OPTION
add constraint OO_DETAIL_FK
foreign key(detail_id)
references ORDER_DETAIL(detail_id);

alter table ORDER_OPTION
add constraint OO_OPTION_FK
foreign key(option_id)
references OPTION_TB(option_id);


-- =====================================
-- PAYMENT
-- =====================================

create table PAYMENT(
    pay_id int,
    order_id int,
    member_id int null,
    pay_amount int,
    pay_type varchar(20),
    pay_date datetime
);

alter table PAYMENT
add constraint PAYMENT_PK
primary key(pay_id);

alter table PAYMENT
add constraint PAYMENT_ORDER_FK
foreign key(order_id)
references ORDERS(order_id);

alter table PAYMENT
add constraint PAYMENT_MEMBER_FK
foreign key(member_id)
references MEMBER(member_id);

alter table PAYMENT
add constraint PAYMENT_ORDER_UK
unique(order_id);