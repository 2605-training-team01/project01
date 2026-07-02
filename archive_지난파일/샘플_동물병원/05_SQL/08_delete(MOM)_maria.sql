--회원 탈회 요청 시 DOG 테이블의 데이터도 같이 삭제


-- 삭제 전 확인
select * from MOM where M_NUMBER = 'M0002';
select * from DOGCARD where M_NUMBER = 'M0002';

-- 삭제
delete from MOM where M_NUMBER = 'M0002';
commit;

-- 삭제 후 확인
select * from MOM where M_NUMBER = 'M0002';
select * from DOGCARD where M_NUMBER = 'M0002';