import streamlit as st


def render():

    st.title("영수증 발행")

    st.write(
        f"주문번호 : A-{st.session_state.order_id}"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "영수증 발행",
            use_container_width=True
        ):

            # 실제 영수증 출력 API 연동 가능

            st.session_state.page = "complete"

            st.rerun()

    with c2:

        if st.button(
            "발행 안함",
            use_container_width=True
        ):

            st.session_state.page = "complete"

            st.rerun()