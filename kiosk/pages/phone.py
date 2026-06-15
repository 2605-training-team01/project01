import streamlit as st


def render():

    st.title("휴대폰 번호 입력")

    phone = st.text_input(
        "휴대폰 번호",
        placeholder="01012345678"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("뒤로가기"):

            st.session_state.page = "membership"

            st.rerun()

    with col2:

        if st.button("적립"):

            st.session_state.phone = phone

            # 실제 회원조회 로직 추가 가능

            st.session_state.page = "receipt"

            st.rerun()