import streamlit as st
from db.database import get_cursor
import pandas as pd


def render():
    conn = None
    cursor = None

    try:
        conn, cursor = get_cursor()

        st.title("매출 통계")

        # 회원조회 탭 삭제
        tab_day, tab_month, tab_year, tab_search = st.tabs([
            "일별", "월별", "연도별", "기간검색"
        ])

        # --------------------------
        # 공통 함수
        # --------------------------
        def format_sales_df(data, rename_dict=None):

            if not data:
                return pd.DataFrame()

            df = pd.DataFrame(data)

            if rename_dict:
                df = df.rename(columns=rename_dict)

            if "매출액" in df.columns:
                df["매출액"] = (
                    df["매출액"]
                    .fillna(0)
                    .astype(int)
                    .apply(lambda x: f"{x:,}원")
                )

            elif "결제금액" in df.columns:
                df["결제금액"] = (
                    df["결제금액"]
                    .fillna(0)
                    .astype(int)
                    .apply(lambda x: f"{x:,}원")
                )

            return df

        # --------------------------
        # 일별
        # --------------------------
        with tab_day:

            cursor.execute("""
                SELECT
                    pay_date AS 날짜,
                    SUM(final_amt) AS 매출액,
                    COUNT(*) AS 결제건수
                FROM payment
                GROUP BY pay_date
                ORDER BY pay_date DESC
            """)

            df = format_sales_df(cursor.fetchall())

            st.dataframe(
                df,
                width="stretch"
            )

        # --------------------------
        # 월별
        # --------------------------
        with tab_month:

            cursor.execute("""
                SELECT
                    DATE_FORMAT(pay_date,'%Y-%m') AS 월,
                    SUM(final_amt) AS 매출액,
                    COUNT(*) AS 결제건수
                FROM payment
                GROUP BY DATE_FORMAT(pay_date,'%Y-%m')
                ORDER BY 월 DESC
            """)

            df = format_sales_df(cursor.fetchall())

            st.dataframe(
                df,
                width="stretch"
            )

        # --------------------------
        # 연도별
        # --------------------------
        with tab_year:

            cursor.execute("""
                SELECT
                    YEAR(pay_date) AS 연도,
                    SUM(final_amt) AS 매출액,
                    COUNT(*) AS 결제건수
                FROM payment
                GROUP BY YEAR(pay_date)
                ORDER BY 연도 DESC
            """)

            df = format_sales_df(cursor.fetchall())

            st.dataframe(
                df,
                width="stretch"
            )

        # --------------------------
        # 기간 검색
        # --------------------------
        with tab_search:

            st.subheader("기간별 매출 조회")

            c1, c2 = st.columns(2)

            start_date = c1.date_input("시작일")

            end_date = c2.date_input("종료일")

            if st.button("검색", key="sales_search"):

                cursor.execute("""
                    SELECT
                        SUM(final_amt) AS sales,
                        COUNT(*) AS orders
                    FROM payment
                    WHERE pay_date BETWEEN %s AND %s
                """, (start_date, end_date))

                result = cursor.fetchone()

                sales = result["sales"] if isinstance(result, dict) else result[0]
                orders = result["orders"] if isinstance(result, dict) else result[1]

                col1, col2 = st.columns(2)

                col1.metric(
                    "총매출",
                    f"{int(sales or 0):,}원"
                )

                col2.metric(
                    "결제건수",
                    orders or 0
                )

                # 결제수단별
                cursor.execute("""
                    SELECT
                        pay_type AS 결제수단,
                        COUNT(*) AS 결제건수,
                        SUM(final_amt) AS 매출액
                    FROM payment
                    WHERE pay_date BETWEEN %s AND %s
                    GROUP BY pay_type
                """, (start_date, end_date))

                st.subheader("결제수단별 통계")

                st.dataframe(
                    format_sales_df(cursor.fetchall()),
                    width="stretch"
                )

                # 카테고리별
                cursor.execute("""
                    SELECT
                        c.category_name AS 카테고리,
                        SUM(od.amount) AS 매출액
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
                    ORDER BY 매출액 DESC
                """, (start_date, end_date))

                st.subheader("카테고리별 매출")

                st.dataframe(
                    format_sales_df(cursor.fetchall()),
                    width="stretch"
                )

                # 메뉴별
                cursor.execute("""
                    SELECT
                        m.menu_name AS 메뉴명,
                        SUM(od.quantity) AS 판매수량,
                        SUM(od.amount) AS 매출액
                    FROM order_detail od
                    JOIN menu m
                        ON od.menu_id = m.menu_id
                    JOIN orders o
                        ON od.order_id = o.order_id
                    WHERE DATE(o.order_date)
                        BETWEEN %s AND %s
                    GROUP BY m.menu_name
                    ORDER BY 판매수량 DESC
                """, (start_date, end_date))

                st.subheader("메뉴별 판매 현황")

                st.dataframe(
                    format_sales_df(cursor.fetchall()),
                    width="stretch"
                )

        # --------------------------
        # 인기 메뉴
        # --------------------------
        st.divider()

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

        st.subheader("🔥 인기 메뉴 TOP 5")

        for idx, menu in enumerate(top_menus, start=1):

            name = menu["menu_name"] if isinstance(menu, dict) else menu[0]
            qty = menu["total_qty"] if isinstance(menu, dict) else menu[1]

            st.write(f"{idx}. {name} ({qty}개)")

        if st.button("뒤로가기", key="back_dashboard"):
            st.session_state.page = "admin_dashboard"
            st.rerun()

    except Exception as e:
        st.error(f"오류가 발생했습니다 : {e}")

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()