import streamlit as st

def render():
    st.title("관리자 로그인")

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("로그인"):

            if password == "1234":
                st.session_state.is_admin = True
                st.session_state.page = "admin_dashboard"
                st.rerun()

            else:
                st.error("비밀번호가 틀렸습니다.")

    with col2:
        if st.button("취소"):
            st.session_state.page = "waiting"
            st.rerun()