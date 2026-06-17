import streamlit as st
from db.database import get_cursor
import time

def render():

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
            st.info(f"📱 {phone} 번호로 적립되었습니다.")
            time.sleep(1)

            st.session_state.member_id = member["member_id"]
            # 스탬프 +1
            cursor.execute("""
            UPDATE member
            SET stamp = stamp + 1
            WHERE member_id = %s
            """,(member["member_id"],))

            # 현재 스탬프 조회
            cursor.execute("""
            SELECT stamp
            FROM member
            WHERE member_id=%s
            """,(member["member_id"],))

            stamp = cursor.fetchone()["stamp"]

            # 10개 모이면 쿠폰 생성
            if stamp >= 10:

                cursor.execute("""
                UPDATE member
                SET
                    stamp = stamp - 10,
                    coupon_count = coupon_count + 1
                WHERE member_id=%s
                """,(member["member_id"],))

                st.success("🎉 쿠폰 1장이 발급되었습니다!")

            
            conn.commit()

        # 회원 아니면 신규 생성
        else:

            cursor.execute("""
            INSERT INTO member(
                phone_number,
                stamp,
                grade
            )
            VALUES(%s,1,'BRONZE')
            """,(phone,))

            conn.commit()

            st.session_state.member_id = cursor.lastrowid


        # 주문에 회원 연결
        cursor.execute("""
        UPDATE orders
        SET member_id=%s
        WHERE order_id=%s
        """,(
            st.session_state.member_id,
            st.session_state.order_id
        ))

        # 결제에 회원 연결
        cursor.execute("""
        UPDATE payment
        SET member_id=%s
        WHERE order_id=%s
        """,(
            st.session_state.member_id,
            st.session_state.order_id
        ))

        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.phone = phone
        st.session_state.page = "payment"
        st.rerun()