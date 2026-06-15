import streamlit as st

def show_payment():

    st.title("결제")

    payment = st.radio(
        "결제 수단",
        [
            "카드",
            "간편결제"
        ]
    )

    if st.button("결제 완료"):

        st.session_state.payment_type = payment

        st.session_state.page = "complete"

        st.rerun()