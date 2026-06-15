import streamlit as st

def show_cart():

    st.title("장바구니")

    total = 0

    for idx, item in enumerate(
        st.session_state.cart
    ):

        col1, col2 = st.columns([5,1])

        with col1:
            st.write(
                f"{item['name']} "
                f"({item['size']}) "
                f"{item['price']:,}원"
            )

        with col2:
            if st.button(
                "삭제",
                key=f"del_{idx}"
            ):
                st.session_state.cart.pop(idx)
                st.rerun()

        total += item["price"]

    st.divider()

    st.subheader(
        f"총 금액 : {total:,}원"
    )

    if st.button("결제하기"):
        st.session_state.page = "payment"
        st.rerun()