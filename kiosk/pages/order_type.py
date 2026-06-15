import streamlit as st

def show_order_type():

    st.title("이용 방법 선택")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "매장",
            use_container_width=True
        ):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with col2:
        if st.button(
            "포장",
            use_container_width=True
        ):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()