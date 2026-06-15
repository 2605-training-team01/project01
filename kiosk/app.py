import streamlit as st

from pages.waiting import show_waiting
from pages.order_type import show_order_type
from pages.menu import show_menu
from pages.option import show_option
from pages.cart import show_cart
from pages.payment import show_payment
from pages.complete import show_complete

st.set_page_config(
    page_title="카페 키오스크",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "waiting"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = None

page = st.session_state.page

if page == "waiting":
    show_waiting()

elif page == "order_type":
    show_order_type()

elif page == "menu":
    show_menu()

elif page == "option":
    show_option()

elif page == "cart":
    show_cart()

elif page == "payment":
    show_payment()

elif page == "complete":
    show_complete()