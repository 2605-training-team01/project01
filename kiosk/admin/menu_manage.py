import os
import streamlit as st
from db.database import get_cursor
import pandas as pd

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

    df = pd.DataFrame(menus)
    
    edited_df = st.data_editor(
        df,
        hide_index=True,
        width='stretch',
        disabled=["menu_id"],      # menu_id 수정 금지
        column_config={
            "menu_id": "번호",
            "category_name": "카테고리",
            "menu_name": "메뉴명",
            "menu_price": st.column_config.NumberColumn(
                "가격",
                format="%d원"
            ),
            "menu_image": "이미지"
        }
    )
    if st.button("수정사항 저장"):

        try:
            edited_df = edited_df.fillna('')

            for _, row in edited_df.iterrows():

                # category_name → category_code 변환
                cursor.execute("""
                SELECT category_code
                FROM category
                WHERE category_name=%s
                """,(row["category_name"],))

                category_code = cursor.fetchone()["category_code"]

                cursor.execute("""
                UPDATE menu
                SET
                    category_code=%s,
                    menu_name=%s,
                    menu_price=%s,
                    menu_image=%s
                WHERE menu_id=%s
                """,(
                    category_code,
                    row["menu_name"],
                    int(row["menu_price"]),
                    row["menu_image"],
                    row["menu_id"]
                ))

            conn.commit()
            st.success("수정 완료")
            st.rerun()

        except Exception as e:
            conn.rollback()
            st.error(e)    

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

    st.divider()

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