import streamlit as st

def render():

    st.title("메뉴 관리")

    st.write("메뉴 관리 페이지")

    if st.button("뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()