import streamlit as st
import time

def show_complete():

    st.success(
        "주문이 완료되었습니다."
    )

    st.markdown(
        f"""
        ## 주문번호
        # A-{st.session_state.order_id}
        """
    )

    st.info("10초 후 초기화")

    time.sleep(10)

    st.session_state.page = "waiting"
    st.session_state.cart = []
    st.session_state.selected_menu = None

    st.rerun()