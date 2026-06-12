# app.py
import streamlit as st
import time

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

# -------------------------
# 샘플 메뉴
# -------------------------
menus = {
    "커피": [
        {"name": "아메리카노", "price": 3000},
        {"name": "카페라떼", "price": 4000},
        {"name": "바닐라라떼", "price": 4500},
    ],
    "음료": [
        {"name": "레몬에이드", "price": 5000},
        {"name": "자몽에이드", "price": 5500},
    ]
}

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

    category = st.sidebar.radio(
        "카테고리",
        list(menus.keys())
    )

    for menu in menus[category]:

        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(menu["name"])

        with col2:
            st.write(f"{menu['price']:,}원")

        with col3:
            if st.button(
                "추가",
                key=menu["name"]
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

    st.subheader(menu["name"])

    size = st.radio(
        "사이즈",
        ["Small", "Medium", "Large"]
    )

    extra_shot = st.checkbox("샷 추가 (+500원)")

    price = menu["price"]

    if extra_shot:
        price += 500

    st.metric("금액", f"{price:,}원")

    if st.button("장바구니 담기"):
        st.session_state.cart.append({
            "name": menu["name"],
            "size": size,
            "shot": extra_shot,
            "price": price
        })

        st.session_state.page = "summary"
        st.rerun()

# -------------------------
# 주문 확인
# -------------------------
elif st.session_state.page == "summary":

    st.title("주문 내역")

    total = 0

    for item in st.session_state.cart:
        st.write(
            f"{item['name']} / {item['size']} / {item['price']:,}원"
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
        """
        ## 주문번호
        # A-101
        """
    )

    st.info("10초 후 초기화")

    time.sleep(10)

    st.session_state.page = "waiting"
    st.session_state.cart = []

    st.rerun()