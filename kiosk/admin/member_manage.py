import streamlit as st
import pandas as pd
from db.database import get_cursor


def render():

    st.title("👤 회원 관리")

    if st.button("← 뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()

    st.divider()

    phone = st.text_input(
        "전화번호",
        placeholder="01012345678"
    )

    if st.button("회원 조회"):

        if phone == "":
            st.warning("전화번호를 입력해주세요.")
            return

        conn = None
        cursor = None

        try:

            conn, cursor = get_cursor()

            ##################################################
            # 회원 조회
            ##################################################

            cursor.execute("""
                SELECT
                    member_id,
                    phone_number,
                    grade,
                    stamp,
                    coupon_count
                FROM member
                WHERE phone_number=%s
            """, (phone,))

            member = cursor.fetchone()

            if not member:
                st.error("회원을 찾을 수 없습니다.")
                return

            member_id = member["member_id"]

            ##################################################
            # 회원정보
            ##################################################

            st.subheader("회원 정보")

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "회원등급",
                    member["grade"] or "BRONZE"
                )

                st.metric(
                    "스탬프",
                    member["stamp"]
                )

            with c2:

                st.metric(
                    "쿠폰",
                    member["coupon_count"]
                )

                st.metric(
                    "전화번호",
                    member["phone_number"]
                )

            st.divider()

            ##################################################
            # 주문내역
            ##################################################

            cursor.execute("""
                SELECT
                    o.order_id,
                    o.order_date,
                    o.takeout_type,
                    o.total_amount
                FROM orders o
                WHERE o.member_id=%s
                ORDER BY o.order_date DESC
            """, (member_id,))

            orders = cursor.fetchall()

            st.subheader("주문 내역")

            if orders:

                df = pd.DataFrame(orders)

                df.rename(
                    columns={
                        "order_id":"주문번호",
                        "order_date":"주문일시",
                        "takeout_type":"포장",
                        "total_amount":"주문금액"
                    },
                    inplace=True
                )

                df["포장"] = df["포장"].replace({
                    "Y":"포장",
                    "N":"매장"
                })

                df["주문금액"] = df["주문금액"].apply(
                    lambda x: f"{int(x):,}원"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:

                st.info("주문 내역이 없습니다.")

            st.divider()

            ##################################################
            # 결제내역
            ##################################################

            cursor.execute("""
                SELECT
                    p.pay_date,
                    p.pay_type,
                    p.final_amt
                FROM payment p
                WHERE p.member_id=%s
                ORDER BY p.pay_date DESC
            """, (member_id,))

            payments = cursor.fetchall()

            st.subheader("결제 내역")

            if payments:

                df = pd.DataFrame(payments)

                df.rename(
                    columns={
                        "pay_date":"결제일",
                        "pay_type":"결제수단",
                        "final_amt":"결제금액"
                    },
                    inplace=True
                )

                df["결제금액"] = df["결제금액"].apply(
                    lambda x: f"{int(x):,}원"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:

                st.info("결제 내역이 없습니다.")

            st.divider()

            ##################################################
            # 누적 구매액
            ##################################################

            cursor.execute("""
                SELECT
                    SUM(final_amt) total
                FROM payment
                WHERE member_id=%s
            """, (member_id,))

            result = cursor.fetchone()

            total = result["total"] or 0

            st.metric(
                "누적 구매액",
                f"{int(total):,}원"
            )

        except Exception as e:

            st.error(f"오류 발생 : {e}")

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()