-- MOM 테이블
select * from MOM;

update MOM
set M_PHONE = '010-4568-3675'
where M_NAME = 'M0001';

update MOM
set M_ADDR = '서울특별시 강남구 테헤란로33길 2'
where M_NAME = 'M0001';

-- DOGCARD 테이블
select * from DOGCARD;

update DOGCARD
set D_NAME = '동동이'
where D_NUMBER = 'D0001';

update DOGCARD
set D_KINDS = '파이어 불독'
where D_NUMBER = 'D0001';

update DOGCARD
set D_AGE = 23
where D_NUMBER = 'D0001';

update DOGCARD
set D_WEIGHT = 8.13
where D_NUMBER = 'D0001';

-- EMP 테이블
select * from EMP;

update EMP
set E_NAME = '이동연'
where E_NUMBER = 'E0001';

update EMP
set E_PHONE = '010-9670-0367'
where E_NUMBER = 'E0001';

update EMP
set E_AGE = 26
where E_NUMBER = 'E0001';

update EMP
set E_SAL = 5000
where E_NUMBER = 'E0001';

-- TREAT 테이블
select * from TREAT;

update TREAT
set T_COST = 123456
where T_CODE = 'T01';

-- HOSPITAL 테이블
select * from HOSPITAL;

update HOSPITAL
set H_MGR = '김동연'
where H_CODE = 'H01';

-- 커밋
commit;
