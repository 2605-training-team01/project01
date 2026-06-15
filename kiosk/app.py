import streamlit as st

from utils.session import init_session

from pages.waiting import render as waiting_page
from pages.order_type import render as order_type_page
from pages.menu import render as menu_page
from pages.option import render as option_page
from pages.summary import render as summary_page
from pages.payment import render as payment_page
from pages.membership import render as membership_page
from pages.phone import render as phone_page
from pages.receipt import render as receipt_page
from pages.complete import render as complete_page

st.set_page_config(
    page_title="키오스크",
    layout="wide"
)

init_session()

PAGE_MAP = {
    "waiting": waiting_page,
    "order_type": order_type_page,
    "menu": menu_page,
    "option": option_page,
    "summary": summary_page,
    "payment": payment_page,
    "membership": membership_page,
    "phone": phone_page,
    "receipt": receipt_page,
    "complete": complete_page
}

PAGE_MAP[st.session_state.page]()