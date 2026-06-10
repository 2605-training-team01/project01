--main_menu
------------------
--menu_category_id
--menu_category_name

main_menu 생성
CREATE TABLE 'main_menu' (
    menu_category_id INT PRIMARY KEY,
    menu_category_name VARCHAR(30) NOT NULL
);

--CREATE TABLE main_menu (
    --mc_code CHAR(3) NOT NULL,
    --mc_name VARCHAR(30) NOT NULL,
    --PRIMARY KEY (mc_code)
--);    

--데이터 입력
INSERT INTO main_menu VALUES ('C01', '커피');
INSERT INTO main_menu VALUES ('T02', '티');
INSERT INTO main_menu VALUES ('D03', '디저트');
INSERT INTO main_menu VALUES ('G04', '굿즈');
INSERT INTO main_menu VALUES ('M05', '회원전용');

--데이터 조회
select * from main_menu;

--UPDATE main_menu
--SET menu_category_name = 'VIP전용'
--WHERE menu_category_id = 4;

--DELETE FROM main_menu
--WHERE menu_category_id = 4;