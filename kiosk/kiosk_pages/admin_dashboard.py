import streamlit as st

def render():

    if not st.session_state.get("is_admin", False):
        st.error("접근 권한이 없습니다.")
        return

    st.title("관리자 페이지")

    st.subheader("관리 메뉴")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("메뉴 관리"):
            st.session_state.page = "menu_manage"
            st.rerun()

    with col2:
        if st.button("매출 통계"):
            st.session_state.page = "sales"
            st.rerun()

    st.divider()

    if st.button("로그아웃"):
        st.session_state.is_admin = False
        st.session_state.page = "waiting"
        st.rerun()