import streamlit as st
from db.database import get_cursor


def render():

    conn, cursor = get_cursor()

    # 카테고리 조회 (category_code 순서 유지)
    cursor.execute("""
    SELECT category_name
    FROM category
    ORDER BY category_code
    """)

    categories = [
        row["category_name"]
        for row in cursor.fetchall()
    ]

    # 메뉴 조회
    cursor.execute("""
    SELECT
        c.category_name,
        m.menu_id,
        m.menu_name,
        m.menu_price
    FROM menu m
    JOIN category c
    ON m.category_code = c.category_code
    ORDER BY c.category_code, m.menu_id
    """)

    menu_rows = cursor.fetchall()

    st.title("메뉴 선택")

    st.sidebar.write(
        f"장바구니 : {len(st.session_state.cart)}개"
    )

    if st.sidebar.button("장바구니 보기"):

        conn.close()

        st.session_state.page = "summary"
        st.rerun()

    category = st.sidebar.radio(
        "카테고리",
        categories
    )

    menu_dict = {}
    for row in menu_rows:
        menu_dict.setdefault(row["category_name"],[]).append(row)
    
    filtered_menu = menu_dict.get(category, [])

    for menu in filtered_menu:

        with st.container(border=True):

            st.subheader(menu["menu_name"])

            st.write(
                f" {menu['menu_price']:,}원"
            )

            if st.button(
                "주문하기",
                key=f"menu_{menu['menu_id']}"
            ):
                st.session_state.selected_menu = menu

                conn.close()

                st.session_state.page = "option"
                st.rerun()

    conn.close()