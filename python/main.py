import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os

# ------------------
# DB 연결
# ------------------

env_path='./.env'
load_dotenv(dotenv_path=env_path)

HOST=os.getenv('DB_HOST')
PORT=os.getenv('DB_PORT')
USER=os.getenv('DB_USER')
PASS=os.getenv('DB_PASS')
NAME=os.getenv('DB_NAME')

conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASS,
    database=NAME,
    charset="utf8"
)

cursor = conn.cursor()


# ------------------
# 1단계 : 카테고리 조회
# ------------------
st.title("☕ 카페 키오스크")

sql = """
SELECT category_code,
       category_name
FROM CATEGORY
ORDER BY category_code
"""

category_df = pd.read_sql(sql, conn)

st.subheader("메뉴선택")

selected_category = st.selectbox(
    "카테고리 선택",
    category_df["category_name"]
)


# ------------------
# 2단계 : 선택한 카테고리 메뉴 조회
# ------------------
menu_sql = f"""
SELECT
    menu_id,
    menu_name,
    menu_price
FROM MENU
WHERE category_code =
(
    SELECT category_code
    FROM CATEGORY
    WHERE category_name = '{selected_category}'
)
"""

menu_df = pd.read_sql(menu_sql, conn)

# # ------------------
# # 3단계 : 메뉴 출력
# # ------------------


# st.subheader("메뉴")

# for _, row in menu_df.iterrows():

#     col1, col2 = st.columns([3,1])

#     with col1:
#         st.write(row["menu_name"])

#     with col2:
#         st.write(f"{row['menu_price']}원")


# ------------------
# 4단계 : 메뉴 선택
# ------------------
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = None

for _, row in menu_df.iterrows():

    col1,col2,col3 = st.columns([3,2,1])

    with col1:
        st.write(row["menu_name"])

    with col2:
        st.write(f"{row['menu_price']}원")

    with col3:
        if st.button(
            "선택",
            key=row["menu_id"]
        ):
            st.session_state.selected_menu = row["menu_id"]
# 여기수정
if st.session_state.selected_menu:

    st.success(
        f"선택된 메뉴 번호 : "
        f"{st.session_state.selected_menu}"
    )

quantity = st.number_input(
    "수량",
    min_value=1,
    value=1
)
# ------------------
# 1. 선택된 메뉴의 이름 표시
# ------------------

if st.session_state.selected_menu:

    sql = """
    SELECT menu_name,
           menu_price
    FROM MENU
    WHERE menu_id = %s
    """

    cursor.execute(
        sql,
        (st.session_state.selected_menu,)
    )

    menu_info = cursor.fetchone()

    st.subheader("선택 메뉴")

    st.write(
        f"{menu_info[0]} "
        f"({menu_info[1]}원)"
    )

# ------------------
# 2. 해당 메뉴의 옵션 조회
# ------------------
if st.session_state.selected_menu:

    option_sql = """
    SELECT
        og.group_name,
        o.option_id,
        o.option_name,
        o.extra_price

    FROM MENU_OPTION_GROUP mog

    JOIN OPTION_GROUP og
    ON mog.group_id = og.group_id

    JOIN OPTION o
    ON og.group_id = o.group_id

    WHERE mog.menu_id = %s

    ORDER BY og.group_id
    """

    option_df = pd.read_sql(
        option_sql,
        conn,
        params=(st.session_state.selected_menu,)
    )

# ------------------
# 3. 옵션 화면 생성
# ------------------
if st.session_state.selected_menu:
    selected_options = []
    option_total = 0

    for group_name in option_df["group_name"].unique():

        st.write(f"### {group_name}")

    group_df = option_df[
        option_df["group_name"] == group_name
    ]

    selected = st.radio(
        label="",
        options=group_df["option_name"],
        key=group_name
    )

    option_row = group_df[
        group_df["option_name"] == selected
    ].iloc[0]

    selected_options.append(
        {
            "option_id": option_row["option_id"],
            "option_name": option_row["option_name"],
            "extra_price": option_row["extra_price"]
        }
    )

    option_total += option_row["extra_price"]

# ------------------
# 4. 총금액 계산
# ------------------
if st.session_state.selected_menu:
    menu_price = menu_info[1]

    # total_price = menu_price + option_total
    total_price = (menu_price + option_total) * quantity

    st.subheader("금액")

    st.write(f"메뉴금액 : {menu_price}원")
    st.write(f"옵션금액 : {option_total}원")

    st.success(
        f"총 금액 : {total_price}원"
    )

# ------------------
# 5. 장바구니 생성
# ------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ------------------
# 6. 장바구니 담기 버튼
# ------------------

if st.button("장바구니 담기"):
        
    st.session_state.cart.append(
        {
            "menu_id":
            st.session_state.selected_menu,

            "menu_name":
            menu_info[0],

            "menu_price":
            menu_price,

            "quantity": 
            quantity,

            "options":
            selected_options,

            "total":
            total_price
        }
    )

    st.success("장바구니에 추가됨")

# ------------------
# 7. 장바구니 출력
# ------------------

st.divider()

st.subheader("장바구니")
cart_total = 0

for item in st.session_state.cart:

    st.write(
        f"☕ {item['menu_name']} "
        f"({item['total']}원)"
    )

    for option in item["options"]:

        st.write(
            f" └ {option['option_name']}"
        )

    cart_total += item["total"]

    st.success(
    f"총 주문금액 : {cart_total}원"
)
    
# ------------------
# 7. 주문내역 확인 화면
# ------------------
st.divider()
st.subheader("주문내역 확인")

cart_total = 0

for item in st.session_state.cart:

    st.write(
        f"{item['menu_name']} x {item['quantity']}"
    )

    st.write(
        f"{item['total']}원"
    )

    cart_total += item['total']

    st.success(
    f"결제예정금액 : {cart_total}원"
)
    
# ------------------
# 7. 주문내역 확인 화면
# ------------------
if st.button("결제하기"):
    st.session_state.page = "payment"

if "page" not in st.session_state:
    st.session_state.page = "menu"

# ------------------
# 7. 결제
# ------------------

if st.session_state.page == "payment":

    st.title("결제")
# ------------------
# 7. 포장
# ------------------

takeout_type = st.radio(
    "이용방식",
    ["포장", "매장"]
)




# ------------------
# 7. 포장
# ------------------
phone_number = st.text_input(
    "전화번호"
)




# 조회
sql = """
SELECT member_id,
       stamp,
       grade
FROM MEMBER
WHERE phone_number=%s
"""

cursor.execute(
    sql,
    (phone_number,)
)

member = cursor.fetchone()


if member:
    st.success(
        f"{member[2]} 회원"
    )

# ------------------
# 7. 결제수단
# ------------------
pay_type = st.radio(
    "결제수단",
    ["CARD","CASH"]
)

if st.button("결제 완료"):
    order_sql = """
INSERT INTO ORDERS
(
 member_id,
 takeout_type,
 order_date,
 total_amount
)
VALUES
(
 %s,
 %s,
 NOW(),
 %s
)
"""

cursor.execute(
    order_sql,
    (
        member[0] if member else None,
        "Y" if takeout_type=="포장" else "N",
        cart_total
    )
)

conn.commit()

order_id = cursor.lastrowid

# 장바구니 반복
for item in st.session_state.cart:
    detail_sql = """
INSERT INTO ORDER_DETAIL
(
 order_id,
 menu_id,
 quantity,
 menu_price,
 amount
)
VALUES
(
 %s,
 %s,
 %s,
 %s,
 %s
)
"""


payment_sql = """
INSERT INTO PAYMENT
(
 member_id,
 order_id,
 final_amt,
 pay_date,
 pay_type
)
VALUES
(
 %s,
 %s,
 %s,
 CURDATE(),
 %s
)
"""

st.success("주문 완료")