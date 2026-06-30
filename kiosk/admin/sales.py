import streamlit as st
from db.database import get_cursor
import pandas as pd

def render():
    conn, cursor = get_cursor()
    st.title("📊 매출 통계")

    tab_day, tab_month, tab_year, tab_search = st.tabs([
    "일별",
    "월별",
    "연도별",
    "기간검색"
    ])
    with tab_day:

        cursor.execute("""
            SELECT
                DATE(order_date) AS day,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY day DESC
        """)

        day_sales = cursor.fetchall()
        df = pd.DataFrame(day_sales)

        df.columns = [
            "날짜",
            "매출액",
            "주문수"
        ]
        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )
        st.dataframe(
            df,
            width='stretch'
        )

    with tab_month:

        cursor.execute("""
            SELECT
                DATE_FORMAT(order_date, '%Y-%m') AS month,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY month DESC
        """)

        month_sales = cursor.fetchall()
        df = pd.DataFrame(month_sales)
        df.columns = [
            "월",
            "매출액",
            "주문수"
        ]

        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )


        st.dataframe(
            df,
            width='stretch'
        )

    with tab_year:

        cursor.execute("""
            SELECT
                YEAR(order_date) AS year,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY YEAR(order_date)
            ORDER BY year DESC
        """)

        year_sales = cursor.fetchall()
        df = pd.DataFrame(year_sales)
        df.columns = [
            "연도",
            "매출액",
            "주문수"
        ]

        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )
        
        st.dataframe(
            df,
            width='stretch'
        )

    with tab_search:

        st.subheader("기간별 매출 조회")

        start_date = st.date_input(
            "시작일"
        )

        end_date = st.date_input(
            "종료일"
        )
        
        
        if st.button("검색"):   

            # 총 매출
            cursor.execute("""
                SELECT
                        SUM(total_amount) AS sales,
                        COUNT(*) AS orders
                    FROM orders
                    WHERE DATE(order_date)
                        BETWEEN %s AND %s
            """, (start_date, end_date))

            result = cursor.fetchone()

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "총매출",
                    f"{int(result['sales'] or 0):,}원"
                )

            with col2:
                st.metric(
                    "주문수",
                    result['orders']
                )


            cursor.execute("""
                SELECT
                    c.category_name,
                    SUM(od.amount) AS sales
                FROM order_detail od

                JOIN menu m
                    ON od.menu_id = m.menu_id

                JOIN category c
                    ON m.category_code = c.category_code

                JOIN orders o
                    ON od.order_id = o.order_id

                WHERE DATE(o.order_date)
                    BETWEEN %s AND %s

                GROUP BY c.category_name
                ORDER BY sales DESC
            """,(start_date,end_date))
            category_sales = cursor.fetchall()

            st.subheader("카테고리별 매출")

            st.dataframe(
                category_sales,
                width='stretch'
            )
            




        # 메뉴별 판매량
            cursor.execute("""
                SELECT
                    m.menu_name,
                    SUM(od.quantity) AS qty,
                    SUM(od.amount) AS sales
                FROM order_detail od

                JOIN menu m
                    ON od.menu_id = m.menu_id

                JOIN orders o
                    ON od.order_id = o.order_id

                WHERE DATE(o.order_date)
                    BETWEEN %s AND %s

                GROUP BY m.menu_name
                ORDER BY qty DESC
            """,(start_date,end_date))

            menu_sales = cursor.fetchall()

            st.subheader(
                "메뉴별 판매 현황"
            )
            
            st.dataframe(
                menu_sales,
                width='stretch'
            )

<<<<<<< HEAD
        # 일별
        with tab_day:
            cursor.execute("SELECT pay_date, SUM(final_amt) AS sales, COUNT(*) AS orders FROM payment GROUP BY pay_date ORDER BY pay_date DESC")
            st.dataframe(format_sales_df(cursor.fetchall(), ["날짜", "매출액", "결제건수"]), width='stretch')

        # 월별
        with tab_month:
            cursor.execute("SELECT DATE_FORMAT(pay_date,'%Y-%m') AS month, SUM(final_amt) AS sales, COUNT(*) AS orders FROM payment GROUP BY month ORDER BY month DESC")
            st.dataframe(format_sales_df(cursor.fetchall(), ["월", "매출액", "결제건수"]), width='stretch')

        # 연도별
        with tab_year:
            cursor.execute("SELECT YEAR(pay_date) AS year, SUM(final_amt) AS sales, COUNT(*) AS orders FROM payment GROUP BY year ORDER BY year DESC")
            st.dataframe(format_sales_df(cursor.fetchall(), ["연도", "매출액", "결제건수"]), width='stretch')

        # 기간 검색
        with tab_search:
            st.subheader("기간별 매출 조회")
            c1, c2 = st.columns(2)
            start_date = c1.date_input("시작일")
            end_date = c2.date_input("종료일")

            if st.button("검색", key="sales_search"):
                # 총매출
                cursor.execute("SELECT SUM(final_amt) AS sales, COUNT(*) AS orders FROM payment WHERE pay_date BETWEEN %s AND %s", (start_date, end_date))
                result = cursor.fetchone()
                
                # 결과값이 딕셔너리인지 튜플인지에 따른 처리
                sales = result['sales'] if isinstance(result, dict) else result[0]
                orders = result['orders'] if isinstance(result, dict) else result[1]

                col1, col2 = st.columns(2)
                col1.metric("총매출", f"{int(sales or 0):,}원")
                col2.metric("결제건수", orders or 0)

                # 결제수단별
                cursor.execute("SELECT pay_type, COUNT(*) AS cnt, SUM(final_amt) AS sales FROM payment WHERE pay_date BETWEEN %s AND %s GROUP BY pay_type", (start_date, end_date))
                st.subheader("결제수단별 통계")
                st.dataframe(format_sales_df(cursor.fetchall(), ["결제수단", "결제건수", "매출액"], {"pay_type":"결제수단", "cnt":"결제건수", "sales":"매출액"}), width='stretch')

                # 카테고리별
                cursor.execute("SELECT c.category_name, SUM(od.amount) AS sales FROM order_detail od JOIN menu m ON od.menu_id = m.menu_id JOIN category c ON m.category_code = c.category_code JOIN orders o ON od.order_id = o.order_id WHERE DATE(o.order_date) BETWEEN %s AND %s GROUP BY c.category_name ORDER BY sales DESC", (start_date, end_date))
                st.subheader("카테고리별 매출")
                st.dataframe(format_sales_df(cursor.fetchall(), ["카테고리", "매출액"], {"category_name":"카테고리", "sales":"매출액"}), width='stretch')

                # 메뉴별
                cursor.execute("SELECT m.menu_name, SUM(od.quantity) AS qty, SUM(od.amount) AS sales FROM order_detail od JOIN menu m ON od.menu_id = m.menu_id JOIN orders o ON od.order_id = o.order_id WHERE DATE(o.order_date) BETWEEN %s AND %s GROUP BY m.menu_name ORDER BY qty DESC", (start_date, end_date))
                st.subheader("메뉴별 판매 현황")
                st.dataframe(format_sales_df(cursor.fetchall(), ["메뉴명", "판매수량", "매출액"], {"menu_name":"메뉴명", "qty":"판매수량", "sales":"매출액"}), width='stretch')

        # 회원조회
        with tab_member:
            st.subheader("📱 전화번호로 결제내역 조회")
            phone = st.text_input("전화번호", placeholder="01012345678")
            if st.button("회원 조회", key="member_search"):
                cursor.execute("SELECT member_id, grade, stamp FROM member WHERE phone_number=%s", (phone,))
                member = cursor.fetchone()
                if not member:
                    st.warning("회원을 찾을 수 없습니다.")
                else:
                    m_id = member['member_id'] if isinstance(member, dict) else member[0]
                    st.success(f"회원등급 : {member['grade'] if isinstance(member, dict) else member[1]}")
                    st.write(f"보유 스탬프 : {member['stamp'] if isinstance(member, dict) else member[2]}개")
                    
                    cursor.execute("SELECT pay_date, pay_type, final_amt FROM payment WHERE member_id=%s ORDER BY pay_date DESC", (m_id,))
                    st.dataframe(format_sales_df(cursor.fetchall(), ["결제일", "결제수단", "결제금액"], {"pay_date":"결제일", "pay_type":"결제수단", "final_amt":"결제금액"}), width='stretch')

        # 인기 메뉴
        st.divider()
        cursor.execute("SELECT m.menu_name, SUM(od.quantity) AS total_qty FROM order_detail od JOIN menu m ON od.menu_id = m.menu_id GROUP BY m.menu_name ORDER BY total_qty DESC LIMIT 5")
=======

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

>>>>>>> parent of 1842737 (admin_sales.py 수정)
        top_menus = cursor.fetchall()



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