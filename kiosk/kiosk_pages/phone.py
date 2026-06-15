import streamlit as st
from db.database import get_cursor

def render():

    # st.title("휴대폰 번호 입력")

    # phone = st.text_input(
    #     "휴대폰 번호",
    #     placeholder="01012345678"
    # )

    # col1, col2 = st.columns(2)

    # with col1:

    #     if st.button("뒤로가기"):

    #         st.session_state.page = "membership"

    #         st.rerun()

    # with col2:

    #     if st.button("적립"):

    #         st.session_state.phone = phone

    #         # 실제 회원조회 로직 추가 가능

    #         st.session_state.page = "receipt"

    #         st.rerun()
    conn, cursor = get_cursor()
    st.title("휴대폰 번호 입력")

    phone = st.text_input(
        "휴대폰 번호",
        placeholder="01012345678"
    )

    if st.button("적립"):

        cursor.execute("""
        SELECT member_id
        FROM member
        WHERE phone_number=%s
        """,(phone,))

        member = cursor.fetchone()

        # 이미 회원이면
        if member:
            st.session_state.member_id = member["member_id"]

        # 회원 아니면 신규 생성
        else:

            cursor.execute("""
            INSERT INTO member(
                phone_number,
                stamp,
                grade
            )
            VALUES(%s,0,'BRONZE')
            """,(phone,))

            conn.commit()

            st.session_state.member_id = cursor.lastrowid

        st.session_state.phone = phone
        st.session_state.page = "receipt"
        st.rerun()