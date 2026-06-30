import streamlit as st
from db.database import get_cursor
import pandas as pd


def render():

    conn = None
    cursor = None

    try:
        conn, cursor = get_cursor()

        st.title("👤 회원 관리")

        st.subheader("📱 전화번호로 회원 조회")

        phone = st.text_input(
            "전화번호",
            placeholder="01012345678"
        )

        if st.button("회원 조회"):

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
                st.warning("회원을 찾을 수 없습니다.")

            else:

                member_id = member["member_id"] if isinstance(member, dict) else member[0]
                phone = member["phone_number"] if isinstance(member, dict) else member[1]
                grade = member["grade"] if isinstance(member, dict) else member[2]
                stamp = member["stamp"] if isinstance(member, dict) else member[3]
                coupon = member["coupon_count"] if isinstance(member, dict) else member[4]

                st.success("회원 정보")

                c1, c2 = st.columns(2)

                with c1:
                    st.metric("등급", grade or "-")

                with c2:
                    st.metric("스탬프", stamp)

                st.write(f"**전화번호 :** {phone}")
                st.write(f"**쿠폰 :** {coupon}개")

                st.divider()

                st.subheader("결제 내역")

                cursor.execute("""
                    SELECT
                        pay_date,
                        pay_type,
                        final_amt
                    FROM payment
                    WHERE member_id=%s
                    ORDER BY pay_date DESC
                """, (member_id,))

                payments = cursor.fetchall()

                if payments:

                    df = pd.DataFrame(payments)

                    df.columns = [
                        "결제일",
                        "결제수단",
                        "결제금액"
                    ]

                    df["결제금액"] = df["결제금액"].apply(
                        lambda x: f"{int(x):,}원"
                    )

                    st.dataframe(
                        df,
                        width="stretch"
                    )

                else:
                    st.info("결제 내역이 없습니다.")

        st.divider()

        if st.button("뒤로가기"):

            st.session_state.page = "admin_dashboard"
            st.rerun()

    except Exception as e:
        st.error(f"오류 : {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()