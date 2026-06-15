import streamlit as st

def show_option():

    menu = st.session_state.selected_menu

    st.title("옵션 선택")

    st.subheader(
        menu["menu_name"]
    )

    size = st.radio(
        "사이즈",
        ["Small", "Medium", "Large"]
    )

    shot = st.checkbox(
        "샷 추가 (+500원)"
    )

    price = menu["price"]

    if shot:
        price += 500

    st.metric(
        "금액",
        f"{price:,}원"
    )

    if st.button("장바구니 담기"):

        st.session_state.cart.append({
            "name": menu["menu_name"],
            "size": size,
            "shot": shot,
            "price": price
        })

        st.session_state.page = "menu"
        st.rerun()