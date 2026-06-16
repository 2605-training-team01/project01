import os
import streamlit as st
from db.database import get_cursor


def render():

    st.title("메뉴 관리")

    conn, cursor = get_cursor()

    # ------------------------
    # 카테고리 조회
    # ------------------------
    cursor.execute("""
        SELECT
            group_id,
            group_name
        FROM option_group
        ORDER BY group_id
    """)

    option_groups = cursor.fetchall()

    cursor.execute("""
        SELECT
            category_code,
            category_name
        FROM category
        ORDER BY category_code
    """)

    categories = cursor.fetchall()

    category_map = {
        row["category_name"]: row["category_code"]
        for row in categories
    }

    # ------------------------
    # 메뉴 조회
    # ------------------------
    cursor.execute("""
        SELECT
            m.menu_id,
            c.category_name,
            m.menu_name,
            m.menu_price,
            m.menu_image
        FROM menu m
        JOIN category c
            ON m.category_code = c.category_code
        ORDER BY m.menu_id
    """)

    menus = cursor.fetchall()

    st.subheader("현재 메뉴")

    for menu in menus:

        col1, col2, col3, col4 = st.columns(
            [2, 2, 2, 1]
        )

        with col1:
            st.write(menu["category_name"])

        with col2:
            st.write(menu["menu_name"])

        with col3:
            st.write(
                f"{menu['menu_price']:,}원"
            )

        with col4:

            if st.button(
                "삭제",
                key=f"del_{menu['menu_id']}"
            ):

                cursor.execute("""
                    DELETE FROM menu
                    WHERE menu_id = %s
                """, (
                    menu["menu_id"],
                ))

                conn.commit()

                st.success(
                    "메뉴가 삭제되었습니다."
                )

                st.rerun()

    st.divider()

    # ------------------------
    # 메뉴 추가
    # ------------------------
    st.subheader("메뉴 추가")

    menu_name = st.text_input(
        "메뉴명"
    )

    menu_price = st.number_input(
        "가격",
        min_value=0,
        step=500
    )

    selected_category = st.selectbox(
        "카테고리",
        list(category_map.keys())
    )

    uploaded_file = st.file_uploader(
        "메뉴 이미지",
        type=["png", "jpg", "jpeg"]
    )

    st.subheader("옵션 설정")

    selected_groups = []

    for group in option_groups:

        if st.checkbox(
            group["group_name"],
            key=f"group_{group['group_id']}"
        ):
            selected_groups.append(
                group["group_id"]
            )

    if st.button("메뉴 추가"):

        image_path = None

        if uploaded_file:

            os.makedirs(
                "images",
                exist_ok=True
            )

            image_path = (
                f"images/{uploaded_file.name}"
            )

            with open(
                image_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

        cursor.execute("""
            INSERT INTO menu
            (
                category_code,
                menu_name,
                menu_price,
                menu_image
            )
            VALUES (%s, %s, %s, %s)
        """, (
            category_map[
                selected_category
            ],
            menu_name,
            menu_price,
            image_path
        ))

        new_menu_id = cursor.lastrowid

        for group_id in selected_groups:

            cursor.execute("""
                INSERT INTO menu_option_group
                (
                    menu_id,
                    group_id
                )
                VALUES (%s, %s)
            """, (
                new_menu_id,
                group_id
            ))

        conn.commit()

        st.success(
            "메뉴가 추가되었습니다."
        )

        st.rerun()

    st.divider()

    if st.button("뒤로가기"):

        st.session_state.page = (
            "admin_dashboard"
        )

        st.rerun()

    conn.close()