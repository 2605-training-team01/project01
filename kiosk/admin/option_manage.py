import streamlit as st
from db.database import get_cursor


def render():

    st.title("옵션 관리")

    conn, cursor = get_cursor()

    # -----------------
    # 옵션 그룹 조회
    # -----------------

    cursor.execute("""
        SELECT *
        FROM option_group
        ORDER BY group_id
    """)

    groups = cursor.fetchall()

    st.subheader("현재 옵션 그룹")

    for group in groups:

        col1, col2 = st.columns([3,1])

        with col1:
            st.write(group["group_name"])

        with col2:

            if st.button(
                "삭제",
                key=f"del_group_{group['group_id']}"
            ):

                cursor.execute("""
                    DELETE FROM option_group
                    WHERE group_id=%s
                """, (
                    group["group_id"],
                ))

                conn.commit()
                st.rerun()

    st.divider()

    st.subheader("옵션 그룹 추가")

    group_name = st.text_input(
        "그룹명"
    )

    if st.button("그룹 추가"):

        cursor.execute("""
            INSERT INTO option_group
            (
                group_name
            )
            VALUES (%s)
        """, (
            group_name,
        ))

        conn.commit()
        st.rerun()

    st.divider()

    # -----------------
    # 옵션 추가
    # -----------------

    st.subheader("옵션 추가")

    group_map = {
        g["group_name"]: g["group_id"]
        for g in groups
    }

    selected_group = st.selectbox(
        "옵션 그룹",
        list(group_map.keys())
    )

    option_name = st.text_input(
        "옵션명"
    )

    extra_price = st.number_input(
        "추가금액",
        min_value=0,
        step=500
    )

    if st.button("옵션 등록"):

        cursor.execute("""
            INSERT INTO option
            (
                group_id,
                option_name,
                extra_price
            )
            VALUES (%s,%s,%s)
        """, (
            group_map[selected_group],
            option_name,
            extra_price
        ))

        conn.commit()

        st.success("등록 완료")
        st.rerun()

    st.divider()

    if st.button("뒤로가기"):

        st.session_state.page = (
            "admin_dashboard"
        )

        st.rerun()

    conn.close()