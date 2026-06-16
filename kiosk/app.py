import streamlit as st

from utils.session import init_session

from kiosk_pages.waiting import render as waiting_page
from kiosk_pages.order_type import render as order_type_page
from kiosk_pages.menu import render as menu_page
from kiosk_pages.option import render as option_page
from kiosk_pages.summary import render as summary_page
from kiosk_pages.payment import render as payment_page
from kiosk_pages.membership import render as membership_page
from kiosk_pages.phone import render as phone_page
from kiosk_pages.receipt import render as receipt_page
from kiosk_pages.complete import render as complete_page
from kiosk_pages.admin_login import render as admin_login_page
from kiosk_pages.admin_dashboard import render as admin_dashboard_page
from admin.menu_manage import render as menu_manage_page
from admin.sales import render as sales_page

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
    "complete": complete_page,
    "admin_login": admin_login_page,
    "admin_dashboard": admin_dashboard_page,
    "menu_manage": menu_manage_page,
    "sales": sales_page
}

PAGE_MAP[st.session_state.page]()