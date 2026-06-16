# pages/menu_page.py

import streamlit as st
from db.database import get_cursor


def render():

    conn, cursor = get_cursor()

    # 카테고리 조회
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
    ORDER BY
        c.category_code,
        m.menu_id
    """)

    menu_rows = cursor.fetchall()

    # ---------------------------------
    # 메뉴 그룹화 (개선사항 2)
    # ---------------------------------
    menu_dict = {}

    for row in menu_rows:

        category_name = row["category_name"]

        if category_name not in menu_dict:
            menu_dict[category_name] = []

        menu_dict[category_name].append(
            dict(row)
        )

    st.title("☕ 메뉴 선택")

    st.sidebar.write(
        f"장바구니 : {len(st.session_state.cart)}개"
    )

    if st.sidebar.button(
        "장바구니 보기"
    ):

        conn.close()

        st.session_state.page = "summary"
        st.rerun()

    # ---------------------------------
    # 카테고리 버튼 UI (개선사항 5)
    # ---------------------------------
    if (
        "selected_category"
        not in st.session_state
    ):
        st.session_state.selected_category = (
            categories[0]
            if categories
            else None
        )

    cols = st.columns(len(categories))

    for idx, category_name in enumerate(categories):

        with cols[idx]:

            if st.button(
                category_name,
                use_container_width=True,
                key=f"cat_{idx}"
            ):

                st.session_state.selected_category = (
                    category_name
                )

                st.rerun()

    st.divider()

    selected_category = (
        st.session_state.selected_category
    )

    filtered_menu = menu_dict.get(
        selected_category,
        []
    )

    # ---------------------------------
    # 카드형 메뉴 UI (개선사항 3)
    # ---------------------------------
    menu_cols = st.columns(3)

    for idx, menu in enumerate(filtered_menu):

        with menu_cols[idx % 3]:

            with st.container(border=True):

                st.subheader(
                    menu["menu_name"]
                )

                st.write(
                    f"💰 {menu['menu_price']:,}원"
                )

                st.write("")

                if st.button(
                    "주문하기",
                    key=f"menu_{menu['menu_id']}",
                    use_container_width=True
                ):

                    # ----------------------
                    # 옵션 페이지 전달용
                    # ----------------------
                    st.session_state.selected_menu = (
                        dict(menu)
                    )

                    st.session_state.page = (
                        "option"
                    )

                    conn.close()

                    st.rerun()

    conn.close()