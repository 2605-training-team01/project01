import streamlit as st
import time

def show_complete():

    st.success(
        "주문이 완료되었습니다."
    )

    st.markdown(
        """
        ## 주문번호
        # A-101
        """
    )

    msg = st.empty()

    for sec in range(5, 0, -1):

        msg.info(
            f"{sec}초 후 초기화됩니다."
        )

        time.sleep(1)

    st.session_state.page = "waiting"
    st.session_state.cart = []
    st.session_state.selected_menu = None

    st.rerun()