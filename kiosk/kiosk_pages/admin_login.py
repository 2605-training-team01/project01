import streamlit as st
from db.database import get_cursor


def render():

    st.title("관리자 로그인")

    admin_name = st.text_input(
        "아이디"
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("로그인"):

            conn, cursor = get_cursor()

            cursor.execute("""
                SELECT *
                FROM admin
                WHERE admin_name = %s
                AND admin_pw = %s
            """, (
                admin_name,
                password
            ))

            admin = cursor.fetchone()

            conn.close()

            if admin:

                st.session_state.is_admin = True
                st.session_state.page = "admin_dashboard"
                st.rerun()

            else:

                st.error(
                    "아이디 또는 비밀번호가 틀렸습니다."
                )

    with col2:

        if st.button("취소"):

            st.session_state.page = "waiting"
            st.rerun()