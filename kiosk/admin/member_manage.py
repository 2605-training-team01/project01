import streamlit as st
import pandas as pd
from db.database import get_cursor


def render():

    conn, cursor = get_cursor()

    st.title("👤 회원 관리")

    keyword = st.text_input("전화번호 검색")

    sql = """
        SELECT
            member_id,
            phone_number,
            stamp,
            coupon_count,
            grade
        FROM member
    """

    params = ()

    if keyword:
        sql += " WHERE phone_number LIKE %s"
        params = (f"%{keyword}%",)

    sql += " ORDER BY member_id DESC"

    cursor.execute(sql, params)

    members = cursor.fetchall()

    if members:

        df = pd.DataFrame(members)

        df.columns = [
            "회원번호",
            "전화번호",
            "스탬프",
            "쿠폰",
            "등급"
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("총 회원 수", len(df))

        with col2:
            st.metric("총 스탬프", int(df["스탬프"].sum()))

        st.dataframe(
            df,
            width="stretch"
        )

    else:
        st.info("등록된 회원이 없습니다.")

    st.divider()

    if st.button("뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()

    conn.close()