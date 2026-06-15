import streamlit as st

def add_cart(item):

    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.session_state.cart.append(item)


def clear_cart():

    st.session_state.cart = []