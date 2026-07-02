-- 1. 자신의 전화번호로 회원 번호를 알고싶다. (회원이름, 회원번호)
select M_NAME, M_NUMBER from MOM where M_PHONE='010-2800-2800';

-- 2. 강아지엄마가 강아지의 병이름을 알고 싶어한다. (강아지번호, 강아지이름, 병이름)
select D.D_NUMBER, D.D_NAME, DS.DS_NAME
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join DISEASE DS on DS.DS_CODE = MD.DS_CODE
where M.M_NUMBER = 'm0001';

-- 3. d0004 환자에게 주사를 놔야하는데 몸무게와 나이를 알고 싶다.
select D_WEIGHT, D_AGE from DOGCARD where D_NUMBER = 'd0004';

-- 4. 관절염의 병명코드를 알고 싶다
select DS_CODE from DISEASE where DS_NAME = '관절염';

-- 5. d0010 환자가 어떤 병 때문에 병원에 왔고 병원비 얼마 냈는지 알고싶다
select DS.DS_NAME, (B.B_VCOST + coalesce(B.B_TCOST,0)) as 병원비
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join DISEASE DS on DS.DS_CODE = MD.DS_CODE
join BILL B on B.MD_DATE = MD.MD_DATE
where D.D_NUMBER = 'd0010';

-- 6. 오이쁨 직원이 일하는 파트의 부서장이 누구인지
select E.E_NAME, H.H_MGR
from HOSPITAL H
join EMP E on H.H_CODE = E.H_CODE
where E.E_NAME = '오이쁨';

-- 7. 21/06/21에 '치료'를 받은 댕댕이들의 목록
select D.D_NUMBER, D.D_NAME, D.D_KINDS, D.D_AGE, D.D_WEIGHT, D.D_SEX
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join BILL B on B.MD_DATE = MD.MD_DATE
where B.B_TCOST is not null and MD.MD_DATE like '250722%'; --날짜수정해야함

-- 8. 우리 애 이름이 똥이인데 첫 방문일을 YYYY-MM-DD로 출력해주세요 (회원 번호와 강아지 이름으로)
select D.D_NAME, date_format(D.D_FDATE, '%Y-%m-%d') as 첫방문일
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
where M.M_NUMBER = 'm0004' and D.D_NAME = '똥이';

-- 9. 보험처리가 가능한 치료방법을 다 보고싶습니다
select T_HOW from TREAT where T_INS = '급여';

-- 10. 맑음소녀 간호사 우리 병원에서 치료비가 제일 비싼 치료방법이 뭐지??
select T_HOW, T_COST from TREAT
where T_COST = (select max(T_COST) from TREAT);

-- 11. 강아지가 2마리 이상인 회원 리스트
select M.M_NUMBER, M.M_PHONE, M.M_NAME, M.M_ADDR, count(D.D_NUMBER) as NUM
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
group by M.M_NUMBER, M.M_PHONE, M.M_NAME, M.M_ADDR
having count(D.D_NUMBER) >= 2;

-- 12. 치료를 받지 않고 진단만 받은 회원 리스트
select distinct M.M_NUMBER, M.M_PHONE, M.M_NAME, M.M_ADDR
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
left join BILL B on B.MD_DATE = MD.MD_DATE
where B.B_TCOST is null;

-- 13. 강아지 나이가 13 이상인 회원 리스트
select distinct M.M_NUMBER, M.M_PHONE, M.M_NAME, M.M_ADDR
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
where D.D_AGE >= 13;

-- 14. 골든 리트리버 견주의 주소와 강아지 진료 및 치료 여부
select M.M_ADDR, T.T_HOW
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on MD.D_NUMBER = D.D_NUMBER
left join TREAT T on T.T_CODE = MD.T_CODE
where D.D_KINDS = '골든 리트리버';

-- 15. 치료를 받은 암컷 강아지들 견주 이름
select distinct M.M_NAME
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on MD.D_NUMBER = D.D_NUMBER
join BILL B on B.MD_DATE = MD.MD_DATE
where B.B_TCOST is not null and D.D_SEX = '암컷';

-- 16. 치료를 받은 3살 이상 10살 이하 암컷 강아지 중 20kg 이하 강아지 견주 회원번호
select distinct M.M_NUMBER
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on MD.D_NUMBER = D.D_NUMBER
join BILL B on B.MD_DATE = MD.MD_DATE
where B.B_TCOST is not null
  and D.D_AGE between 3 and 10
  and D.D_SEX = '암컷'
  and D.D_WEIGHT <= 20;

-- 17. 이보영 회원의 강아지 성별과 최초 방문일자
select D.D_SEX, D.D_FDATE
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
where M.M_NAME = '이보영';

-- 18. 3만원 이상 50만원 미만 치료방법 중 보험처리 안되는 것
select T_HOW, T_COST, T_INS
from TREAT
where T_COST between 30000 and 500000
  and T_INS = '비급여';

-- 19. 회원 전화번호 중간에 8 포함, 1로 끝나고, 병원비를 결재하지 않은 강아지 몸무게
select D.D_WEIGHT
from MOM M
join DOGCARD D on M.M_NUMBER = D.M_NUMBER
join MEDICAL MD on MD.D_NUMBER = D.D_NUMBER
join BILL B on B.MD_DATE = MD.MD_DATE
where M.M_PHONE like '%8%1' and B.B_TCOST is null;

-- 20. 2025년 병원을 찾은 환자 중 어떤 병이 제일 많았나?
select MD.DS_CODE, DS.DS_NAME, count(*) as 환자수
from MEDICAL MD
join DISEASE DS on MD.DS_CODE = DS.DS_CODE
where left(MD.MD_DATE, 2) = '25'
group by MD.DS_CODE, DS.DS_NAME
order by 환자수 desc
limit 1;

-- 21. 오늘 매출 합계
select sum(B_VCOST) + sum(coalesce(B_TCOST,0)) as 오늘매출
from BILL
where left(MD_DATE,6) = date_format(now(), '%y%m%d');

-- 22. 올해 입사한 직원 리스트
select * from EMP
where left(E_HIREDATE,4) = date_format(now(), '%Y');

-- 23. 2살 넘은 강아지 중 심장사상충에 걸린 강아지 수
select count(distinct D.D_NUMBER) as 심장사상충_강아지수
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join DISEASE DS on MD.DS_CODE = DS.DS_CODE
where DS.DS_NAME = '심장사상충' and D.D_AGE > 2;

-- 24. 피부병에 걸리고 연고로만 치료한 강아지 이름
select distinct D.D_NUMBER, D.D_NAME
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join TREAT T on MD.T_CODE = T.T_CODE
join DISEASE DS on MD.DS_CODE = DS.DS_CODE
where DS.DS_NAME = '피부병' and T.T_HOW = '연고';

-- 25. 의사부 부서장 이름 출력
select concat(H_MGR, '입니다') as 의사부_부서장
from HOSPITAL
where H_JOB = '의사부';

-- 26. 두 가지 치료를 받은 강아지 이름
select D.D_NAME
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
group by D.D_NAME
having count(distinct MD.T_CODE) >= 2;

-- 27. 직원들 중 매니저보다 나이 많은 사람 이름
select E.E_NAME, E.E_AGE
from EMP E
join HOSPITAL H on E.H_CODE = H.H_CODE
where E.E_AGE > all (
  select E2.E_AGE
  from EMP E2
  where E2.E_NAME in ('맑음소녀', '수스맨')
);

-- 28. 우리 강아지 몇 번째 방문인가요? 회원번호: m0001
select count(*) as 방문횟수
from MEDICAL MD
join DOGCARD D on MD.D_NUMBER = D.D_NUMBER
where D.M_NUMBER = 'm0001';

-- 29. 오윤희 고객 전화번호와 주소
select M_NAME, M_PHONE, M_ADDR from MOM where M_NAME = '오윤희';

-- 30. 치와와 중 내과수술 받은 강아지 이름
select distinct D.D_NUMBER, D.D_NAME
from DOGCARD D
join MEDICAL MD on D.D_NUMBER = MD.D_NUMBER
join TREAT T on MD.T_CODE = T.T_CODE
where T.T_HOW = '내과수술';
