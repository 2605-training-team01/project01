import streamlit as st
def render():
    st.title("메뉴 선택")
    if st.button("아메리카노 추가"):
        st.session_state.cart.append({"menu_id":1,"menu_name":"아메리카노","price":3000,"options":[]})
    if st.button("장바구니 보기"):
        st.session_state.page="summary"; st.rerun()
import streamlit as st
from db.database import get_cursor


def render():

    conn, cursor = get_cursor()

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

    categories = sorted(
        list(
            set(
                row["category_name"]
                for row in menu_rows
            )
        )
    )

    st.title("메뉴 선택")

    st.sidebar.write(
        f"장바구니 : {len(st.session_state.cart)}개"
    )

    if st.sidebar.button("장바구니 보기"):

        st.session_state.page = "summary"

        conn.close()

        st.rerun()

    category = st.sidebar.radio(
        "카테고리",
        categories
    )

    filtered_menu = [
        row
        for row in menu_rows
        if row["category_name"] == category
    ]

    for menu in filtered_menu:

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(menu["menu_name"])

        with col2:
            st.write(
                f"{menu['menu_price']:,}원"
            )

        with col3:

            if st.button(
                "추가",
                key=f"menu_{menu['menu_id']}"
            ):

                st.session_state.selected_menu = menu

                st.session_state.page = "option"

                conn.close()

                st.rerun()

    conn.close()