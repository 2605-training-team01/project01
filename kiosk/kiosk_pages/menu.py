# pages/menu.py
import streamlit as st
from db.database import get_cursor

def render():

    conn, cursor = get_cursor()

    # 카테고리 조회
    cursor.execute("""
    SELECT category_name
    FROM category
    ORDER BY category_code
    """)

    categories = [
        row["category_name"]
        for row in cursor.fetchall()
    ]

    # 메뉴 조회
    cursor.execute("""
    SELECT
        c.category_name,
        m.menu_id,
        m.menu_name,
        m.menu_price,
        m.menu_image
    FROM menu m
    JOIN category c
        ON m.category_code = c.category_code
    ORDER BY
        c.category_code,
        m.menu_id
    """)

    menu_rows = cursor.fetchall()

    # 최근 7일 간 3개 이상 판매된 메뉴 조회    
    cursor.execute(
    """SELECT
        c.category_name,
        od.menu_id,
        SUM(od.quantity) AS total_qty
    FROM order_detail od
    JOIN orders om
        ON od.order_id = om.order_id
    JOIN menu m
        ON od.menu_id = m.menu_id
    JOIN category c
        ON m.category_code = c.category_code
    WHERE
        om.order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    GROUP BY
        c.category_name,
        od.menu_id
    HAVING
        SUM(od.quantity) >= 3;
    """
    )
    best_rows = cursor.fetchall()
    
    # ---------------------------------
    # 메뉴 그룹화 (개선사항 2)
    # ---------------------------------
    menu_dict = {}

    for row in menu_rows:

        category_name = row["category_name"]

        if category_name not in menu_dict:
            menu_dict[category_name] = []

        menu_dict[category_name].append(
            dict(row)
        )

    st.title("☕ 메뉴 선택", text_alignment="center")
    
    # ---------------------------------
    # 카테고리 버튼 UI (개선사항 5)
    # ---------------------------------
    if (
        "selected_category"
        not in st.session_state
    ):
        st.session_state.selected_category = (
            categories[0]
            if categories
            else None
        )

    cols = st.columns(len(categories))

    for idx, category_name in enumerate(categories):

        with cols[idx]:

            if st.button(
                category_name,
                width='stretch',
                key=f"cat_{idx}"
            ):

                st.session_state.selected_category = (
                    category_name
                )

                st.rerun()

    selected_category = (
        st.session_state.selected_category
    )

    filtered_menu = menu_dict.get(
        selected_category,
        []
    )

    # ---------------------------------
    # 카드형 메뉴 UI
    # ---------------------------------
    # best_menu_set = set()
    # for row in best_rows:
    #     best_menu_set.add(row["menu_id"])
    best_menu_set = {
        row["menu_id"] for row in best_rows
    }
    
    menu_cols = st.columns(4)
    for idx, menu in enumerate(filtered_menu):

        with menu_cols[idx % 4]:

            with st.container(border=True):
                if menu["menu_id"] in best_menu_set:
                    st.markdown(
                        """
                        <div style="text-align:center;margin-bottom:8px;">
                            <span style="
                                background:#ff4b4b;
                                color:white;
                                padding:4px 10px;
                                border-radius:15px;
                                font-size:13px;
                                font-weight:bold;
                            ">
                                BEST
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                image_path = menu.get("menu_image")

                if image_path:
                    st.image(
                        image_path,
                        width='stretch'
                    )
                else:
                    st.image(
                        "images/no-image.jpg",
                        width='stretch'
                    )
                    
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <div style="
                            font-size:22px;
                            font-weight:bold;
                            margin-bottom:8px;
                        ">
                            {menu['menu_name']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p style='text-align:center;font-size:15px;'>{menu['menu_price']:,}원</p>",
                    unsafe_allow_html=True
                )

                if st.button(
                    "주문하기",
                    key=f"menu_{menu['menu_id']}",
                    width='stretch'
                ):

                    st.session_state.selected_menu = (
                        dict(menu)
                    )

                    st.session_state.page = (
                        "option"
                    )

                    conn.close()

                    st.rerun()

# -----------------------------
# 하단 장바구니 영역
# -----------------------------

    st.markdown("<br><br>", unsafe_allow_html=True)

    cart_count = len(st.session_state.cart)

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            f"""
            ### 🛒 장바구니 {cart_count}개
            """
        )
        
    with col2:

        st.write("")

        if st.button(
            "장바구니 보기",
            # use_container_width=True
            width='stretch'
        ):

            st.session_state.page = "summary"
            st.rerun()
            
    conn.close()