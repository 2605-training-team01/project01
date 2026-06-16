import streamlit as st

def render():

    st.title("매출 통계")

    st.metric("총 매출", "35,000원")
    st.metric("주문 수", "12건")

    if st.button("뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()