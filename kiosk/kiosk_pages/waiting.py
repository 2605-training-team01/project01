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

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([9, 1])

    with col_right:
        if st.button("⚙️"):
            st.session_state.page = "admin_login"
            st.rerun()