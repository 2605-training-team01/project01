import streamlit as st


def render():

    st.markdown(
        "<h1 style='text-align:center;margin-top:200px;'>☕ KIOSK</h1>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "화면을 터치하세요",
            use_container_width=True
        ):
            st.session_state.page = "order_type"
            st.rerun()