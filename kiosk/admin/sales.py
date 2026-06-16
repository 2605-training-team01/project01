import streamlit as st
from db.database import get_cursor

def render():

    st.title("📊 매출 통계")

    conn, cursor = get_cursor()

    # 총 매출
    cursor.execute("""
        SELECT SUM(total_amount) AS total_sales
        FROM orders
    """)

    total_sales = cursor.fetchone()["total_sales"] or 0

    # 주문 건수
    cursor.execute("""
        SELECT COUNT(*) AS order_count
        FROM orders
    """)

    order_count = cursor.fetchone()["order_count"]

    # 인기 메뉴 TOP 5
    cursor.execute("""
        SELECT
            m.menu_name,
            SUM(od.quantity) AS total_qty
        FROM order_detail od
        JOIN menu m
            ON od.menu_id = m.menu_id
        GROUP BY m.menu_name
        ORDER BY total_qty DESC
        LIMIT 5
    """)

    top_menus = cursor.fetchall()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "총 매출",
            f"{int(total_sales):,}원"
        )

    with col2:
        st.metric(
            "총 주문 수",
            order_count
        )

    st.divider()

    st.subheader("🔥 인기 메뉴 TOP 5")

    for idx, menu in enumerate(top_menus, start=1):

        st.write(
            f"{idx}. {menu['menu_name']} "
            f"({menu['total_qty']}개)"
        )

    st.divider()

    if st.button("뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()

    conn.close()