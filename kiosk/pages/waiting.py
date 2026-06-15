import streamlit as st

def show_waiting():

    st.markdown(
        "<h1 style='text-align:center;'>☕ KIOSK</h1>",
        unsafe_allow_html=True
    )

    if st.button(
        "화면을 터치하세요",
        use_container_width=True
    ):
        st.session_state.page = "order_type"
        st.rerun()