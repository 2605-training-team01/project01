import streamlit as st

from database.order_repository import save_order

def create_order():

    total = sum(
        item["price"]
        for item in st.session_state.cart
    )

    order_id = save_order(
        st.session_state.order_type,
        st.session_state.payment_type,
        total
    )

    return order_id