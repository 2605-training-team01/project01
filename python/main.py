# app.py
import streamlit as st
import time
import pymysql
from dotenv import load_dotenv
import os

env_path='./test.env'
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

cursor = conn.cursor(pymysql.cursors.DictCursor)

st.set_page_config(
    page_title="키오스크",
    layout="wide"
)

# -------------------------
# 초기 상태
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "waiting"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_type" not in st.session_state:
    st.session_state.order_type = ""

if "membership" not in st.session_state:
    st.session_state.membership = False

if "order_id" not in st.session_state:
    st.session_state.order_id = None
# -------------------------
# 샘플 메뉴
# -------------------------
cursor.execute("""
SELECT
    c.category_name,
    m.menu_id,
    m.menu_name,
    m.menu_price
FROM menu m
JOIN category c
ON m.category_code = c.category_code
""")

menu_rows = cursor.fetchall()
# 카테고리 생성
categories = list(
    set(row["category_name"] for row in menu_rows)
)
# -------------------------
# 대기 화면
# -------------------------
if st.session_state.page == "waiting":

    st.markdown(
        "<h1 style='text-align:center;margin-top:200px;'>☕ KIOSK</h1>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button(
            "화면을 터치하세요",
            use_container_width=True
        ):
            st.session_state.page = "order_type"
            st.rerun()

# -------------------------
# 매장 / 포장
# -------------------------
elif st.session_state.page == "order_type":

    st.title("이용 방법 선택")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("매장", use_container_width=True):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with c2:
        if st.button("포장", use_container_width=True):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()

# -------------------------
# 메뉴 선택
# -------------------------
elif st.session_state.page == "menu":

    st.title("메뉴 선택")

    st.sidebar.write(
        f"장바구니 : {len(st.session_state.cart)}개"
    )

    if st.sidebar.button("장바구니 보기"):
        st.session_state.page = "summary"
        st.rerun()

    category = st.sidebar.radio(
    "카테고리",
    categories
)
    

    filtered_menu = [
    row for row in menu_rows
    if row["category_name"] == category
]

    for menu in filtered_menu:

        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(menu["menu_name"])

        with col2:
            st.write(f"{menu['menu_price']:,}원")

        with col3:
            if st.button(
                    "추가",
                key=menu["menu_id"]
            ):
                st.session_state.selected_menu = menu
                st.session_state.page = "option"
                st.rerun()

# -------------------------
# 옵션 선택
# -------------------------
elif st.session_state.page == "option":

    menu = st.session_state.selected_menu

    st.title("옵션 선택")

    st.subheader(menu["menu_name"])

    cursor.execute("""
    SELECT
        o.option_id,
        o.option_name,
        o.extra_price
    FROM option o
    JOIN menu_option_group mog
        ON o.group_id = mog.group_id
    WHERE mog.menu_id=%s
    """,(menu["menu_id"],))

    options = cursor.fetchall()

    selected_options = []

    total_price = menu["menu_price"]

    for op in options:

        if st.checkbox(
            f"{op['option_name']} (+{op['extra_price']}원)"
        ):
            selected_options.append(op)
            total_price += op["extra_price"]

    st.metric(
        "금액",
        f"{total_price:,}원"
    )
# #############################여기부터
    if st.button("장바구니 담기"):

        st.session_state.cart.append({
            "menu_id": menu["menu_id"],
            "menu_name": menu["menu_name"],
            "price": total_price,
            "options": selected_options
        })

        st.session_state.page = "menu"
        st.rerun()
# -------------------------
# 주문 확인
# -------------------------

elif st.session_state.page == "summary":

    st.title("주문 내역")

    total = 0

    for item in st.session_state.cart:
        st.write(
        f"{item['menu_name']} / {item['price']:,}원"
        )
        total += item["price"]

    st.divider()

    st.subheader(f"총 금액 : {total:,}원")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("메뉴 추가"):
            st.session_state.page = "menu"
            st.rerun()

    with c2:
        if st.button("결제하기"):
            st.session_state.page = "payment"
            st.rerun()

# -------------------------
# 결제
# -------------------------
elif st.session_state.page == "payment":

    st.title("결제")

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제", "쿠폰"]
    )

    if st.button("결제 완료"):

        total_amount = sum(
            item["price"]
            for item in st.session_state.cart
        )

        cursor.execute("""
        INSERT INTO orders(
            member_id,
            takeout_type,
            total_amount
        )
        VALUES(%s,%s,%s)
        """,(
            None,
            "Y" if st.session_state.order_type=="포장"
            else "N",
            total_amount
        ))

        order_id = cursor.lastrowid
        st.session_state.order_id = order_id

        for item in st.session_state.cart:

            cursor.execute("""
            INSERT INTO order_detail(
                order_id,
                menu_id,
                quantity,
                menu_price,
                amount
            )
            VALUES(%s,%s,%s,%s,%s)
            """,(
                order_id,
                item["menu_id"],
                1,
                item["price"],
                item["price"]
            ))

            detail_id = cursor.lastrowid

            for op in item["options"]:

                cursor.execute("""
                INSERT INTO order_option(
                    detail_id,
                    option_id,
                    option_price
                )
                VALUES(%s,%s,%s)
                """,(
                    detail_id,
                    op["option_id"],
                    op["extra_price"]
                ))
        cursor.execute("""
            INSERT INTO payment(
                member_id,
                order_id,
                final_amt,
                pay_date,
                pay_type
            )
            VALUES(%s,%s,%s,NOW(),%s)
            """,(
                None,
                order_id,
                total_amount,
                payment
            ))
        conn.commit()

        st.session_state.payment = payment
        st.session_state.page = "membership"
        st.rerun()
    
# -------------------------
# 멤버십
# -------------------------
elif st.session_state.page == "membership":

    st.title("멤버십 적립")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("적립 안함"):
            st.session_state.page = "receipt"
            st.rerun()

    with c2:
        if st.button("적립하기"):
            st.session_state.page = "phone"
            st.rerun()

# -------------------------
# 번호 입력
# -------------------------
elif st.session_state.page == "phone":

    st.title("휴대폰 번호 입력")

    phone = st.text_input(
        "휴대폰 번호",
        placeholder="01012345678"
    )

    if st.button("적립"):
        st.session_state.phone = phone
        st.session_state.page = "receipt"
        st.rerun()

# -------------------------
# 영수증
# -------------------------
elif st.session_state.page == "receipt":

    st.title("영수증 발행")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("영수증 발행"):
            st.session_state.page = "complete"
            st.rerun()

    with c2:
        if st.button("발행 안함"):
            st.session_state.page = "complete"
            st.rerun()

# -------------------------
# 완료
# -------------------------
elif st.session_state.page == "complete":

    st.success("주문이 완료되었습니다.")

    st.markdown(
        f"""
        ## 주문번호
        # A-{st.session_state.order_id}
        """
    )

    st.info("10초 후 초기화")

    time.sleep(10)

    st.session_state.page = "waiting"
    st.session_state.cart = []

    st.rerun()