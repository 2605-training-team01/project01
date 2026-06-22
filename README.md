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
> 프로젝트 구조
```
kiosk/
│
├── app.py                  # 메인 실행 파일
├── requirements.txt
├── 실행방법.md
│
├── admin/                  # 관리자 기능
│   ├── __init__.py
│   ├── change_password.py  # 비밀번호 변경
│   ├── menu_manage.py      # 메뉴 관리
│   ├── option_manage.py    # 옵션 관리
│   └── sales.py            # 매출 조회
│
├── db/
│   └── database.py         # DB 연결 및 커서 생성
│
├── kiosk_pages/            # 사용자 화면
│   ├── admin_dashboard.py  # 관리자 대시보드
│   ├── admin_login.py      # 관리자 로그인
│   ├── complete.py         # 주문 완료
│   ├── membership.py       # 회원 적립
│   ├── menu.py             # 메뉴 선택
│   ├── option.py           # 옵션 선택
│   ├── order_type.py       # 매장/포장 선택
│   ├── payment.py          # 결제
│   ├── phone.py            # 전화번호 입력
│   ├── receipt.py          # 영수증
│   ├── summary.py          # 장바구니/주문 요약
│   └── waiting.py          # 대기 화면
│
├── utils/                  # 공통 기능
│   ├── cookies.py
│   └── session.py
│
├── db/
│   └── database.py
│
├── images/                 # 메뉴 및 배경 이미지
│   ├── americano.png
│   ├── coldbrew.png
│   ├── latte.png
│   ├── rabbit.png
│   ├── no-image.png
│   └── ...
│
├── fonts/
│   ├── GmarketSansTTFBold.ttf
│   └── PretendardVariable.ttf
│
└── in_charge/
    ├── waiting2.py
    ├── store.png
    ├── takeout.png
    ├── drink.jpg
    └── drink2.jpg
```