import streamlit as st

from database.menu_repository import (
    get_categories,
    get_menu_by_category
)

def show_menu():

    st.title("메뉴 선택")

    categories = get_categories()

    cols = st.columns(len(categories))

    for idx, category in enumerate(categories):

        with cols[idx]:
            if st.button(
                category["category_name"],
                use_container_width=True
            ):
                st.session_state.category_id = category["category_id"]

    if "category_id" not in st.session_state:
        st.session_state.category_id = categories[0]["category_id"]

    menus = get_menu_by_category(
        st.session_state.category_id
    )

    for menu in menus:

        col1, col2, col3 = st.columns([4,1,1])

        with col1:
            st.write(menu["menu_name"])

        with col2:
            st.write(
                f"{menu['price']:,}원"
            )

        with col3:
            if st.button(
                "선택",
                key=menu["menu_id"]
            ):
                st.session_state.selected_menu = dict(menu)
                st.session_state.page = "option"
                st.rerun()

    if st.button("장바구니"):
        st.session_state.page = "cart"
        st.rerun()