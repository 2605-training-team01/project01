2026년 교육 과정 팀01 프로젝트01
===
1. 주제 선정
2. 밴치 마킹
3. 요구 사항 ( 가상 시나리오  )
4. 개념적 -> 논리적(LERD) -> 물리적(PERD)모델링
5. SQL 작성
   - ( DDL, DML, DQL )
6. DBMS에  install
   - 생성 ( 새 계정 , 새 DB , 권한부여 )
   - DDL, DML 실행
   - DQL 실행하여 모델링 검증
7. Python와 연동
--------
> (3) 요구 사항
[ 요구사항 (카페 키오스크)]
<1> 메뉴 관리
판매되는 메뉴는 카테고리별로 구분하여 관리하기를 원한다.
```sql
-- 메뉴와 카테고리를 함께 조회
SELECT
    m.menu_id,
    c.category_name,
    m.menu_name,
    m.menu_price
FROM MENU m
JOIN CATEGORY c
    ON m.category_code = c.category_code;

-- 특정 카테고리의 메뉴만 조회
SELECT
    c.category_name,
    m.menu_name,
    m.menu_price
FROM MENU m
JOIN CATEGORY c
    ON m.category_code = c.category_code
WHERE c.category_code = '20';
```
<2> 메뉴 관리
각 메뉴의 메뉴명, 판매가격 정보를 관리하기를 원한다.

<3> 메뉴 옵션 관리
메뉴별 옵션 그룹(사이즈, 온도 등)과 옵션별 추가금액 정보를 관리하기를 원한다.
<4> 메뉴 옵션 관리
하나의 메뉴는 여러 개의 옵션 그룹을 가질 수 있도록 관리하기를 원한다.
<5> 주문 관리
고객은 메뉴를 선택하여 주문할 수 있으며 주문번호를 생성하여 관리하기를 원한다.
<6> 주문 관리
주문 시 선택한 메뉴, 수량, 주문금액 및 옵션 정보를 저장하고 관리하기를 원한다.
<7> 주문 관리
고객은 매장 이용 또는 포장 여부를 선택하여 주문할 수 있도록 하기를 원한다.
<8> 회원 관리
회원의 전화번호, 등급, 스탬프 정보를 관리하기를 원한다.
<9> 회원 관리
회원 주문 시 스탬프를 적립하고 누적 스탬프를 관리하기를 원한다.
<10> 결제 관리
주문에 대한 결제금액, 결제일자, 결제수단 정보를 관리하기를 원한다.
<11> 결제 관리
회원별 결제 내역을 조회할 수 있도록 하기를 원한다.
```sql
SELECT
    m.member_id,
    m.phone_number,
    o.order_id,
    p.final_amt,
    p.pay_type,
    p.pay_date
FROM MEMBER m
JOIN ORDERS o
    ON m.member_id = o.member_id
JOIN PAYMENT p
    ON o.order_id = p.order_id
WHERE m.phone_number = 1
ORDER BY p.pay_date DESC;
```
<12> 통계 관리
메뉴별 판매 수량 및 판매 금액을 조회할 수 있도록 하기를 원한다.
<13> 통계 관리
가장 많이 판매된 메뉴 순위를 조회할 수 있도록 하기를 원한다.
<14> 통계 관리
일별, 월별, 연도별 매출 현황과 특정 기간의 주문 내역을 조회할 수 있도록 하기를 원한다.
<15> 통계 관리
카테고리별 판매 현황 및 회원별 구매 현황을 분석할 수 있도록 하기를 원한다.

> (4) 기능 명세
+ 메뉴 조회 및 선택 기능
    + 포장/매장 선택
    + 인기 메뉴 조회    
    + 카테고리(category) 조회, 선택
    + 메뉴(menu) 조회
        + 선택한 카테고리에 해당하는 메뉴 조회, 선택 

+ 옵션 관리
    + 메뉴별 옵션 조회
    + 옵션 선택

+ 주문 기능
    + 주문 내역 화면 표시 
    + 스탬프 조회 및 적용 (스탬프는 10개 단위 사용)
    + 최종 결제 금액 표시
    + 스탬프 적립
    + 결제 후 주문 완료 

+ 영수증 기능
    + 영수증 발급 여부 선택
      + (yes) 영수증 화면 출력
      + (no) 주문 완료 

------
> (8) 팀원 역할
+ 박소연
   + 기획서 & 산출물 작성
   + 요구 사항 정의
   + 가상 시나리오 작성

   + 
+ 박종민
   + 화면 흐름도 구성
   + 데이터베이스 DDL (테이블: member)  

+ 이경진
   + 데이터베이스 DDL (테이블: payment) 

+ 강재환
   + 팀 매니징
   + 데이터베이스 모델링
   + 데이터베이스 DDL 
      + 데이터 베이스, 유저 생성 및 권한 설정
   + 데이터베이스 DML (요구사항)

+ 강유진
   + 데이터베이스 모델링
   + 데이터베이스 DDL (테이블: category, menu, menu_option_group, option_group, option )
   + 데이터베이스 DML (예제 데이터 입력) 
   + 기능별 DML 플로우(화면 흐름에 따른 기능별)

+ 서지윤
   + 데이터베이스 DDL (테이블: orders, order_detail, order_option )
   + UI 디자인 