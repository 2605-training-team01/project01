import streamlit as st
from db.database import get_cursor
import time

def add_digit(num):
    phone_digits = st.session_state.get("phone_digits", "")
    if len(st.session_state.phone_digits) < 11:
        st.session_state.phone_digits += str(num)

def backspace():
    phone_digits = st.session_state.get("phone_digits", "")
    st.session_state.phone_digits = st.session_state.phone_digits[:-1]

def clear():
    st.session_state.phone_digits = ""
    
def render():
    if "phone_digits" not in st.session_state:
        st.session_state.phone_digits = ""
        
    conn, cursor = get_cursor()
    st.title("휴대폰 번호 입력")

    # phone = st.text_input(
    #     "휴대폰 번호",
    #     placeholder="010-1234-5678"
    # )
    # digits = st.session_state.phone_digits
    digits = st.session_state.get("phone_digits", "")

    if len(digits) > 7:
        phone = f"{digits[:3]}{digits[3:7]}{digits[7:]}"
    elif len(digits) > 3:
        phone = f"{digits[:3]}{digits[3:]}"
    else:
        phone = digits

    st.markdown(
        f"""
        <div style="
            font-size:40px;
            text-align:center;
            border:2px solid gray;
            border-radius:10px;
            padding:20px;
            margin-bottom:30px;
        ">
        {phone}
        </div>
        """,
        unsafe_allow_html=True
    )

    ## 키패드
    row1 = st.columns(3)
    with row1[0]:
        st.button("1", use_container_width=True, on_click=add_digit, args=(1,))
    with row1[1]:
        st.button("2", use_container_width=True, on_click=add_digit, args=(2,))
    with row1[2]:
        st.button("3", use_container_width=True, on_click=add_digit, args=(3,))

    row2 = st.columns(3)
    with row2[0]:
        st.button("4", use_container_width=True, on_click=add_digit, args=(4,))
    with row2[1]:
        st.button("5", use_container_width=True, on_click=add_digit, args=(5,))
    with row2[2]:
        st.button("6", use_container_width=True, on_click=add_digit, args=(6,))

    row3 = st.columns(3)
    with row3[0]:
        st.button("7", use_container_width=True, on_click=add_digit, args=(7,))
    with row3[1]:
        st.button("8", use_container_width=True, on_click=add_digit, args=(8,))
    with row3[2]:
        st.button("9", use_container_width=True, on_click=add_digit, args=(9,))

    row4 = st.columns(3)
    with row4[0]:
        st.button("←", use_container_width=True, on_click=backspace)
    with row4[1]:
        st.button("0", use_container_width=True, on_click=add_digit, args=(0,))
    with row4[2]:
        st.button("C", use_container_width=True, on_click=clear)    
    
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
            st.session_state.phone_digits = ""
            st.session_state.phone = phone
            st.session_state.page = "payment"
            st.rerun()
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
        st.session_state.phone_digits = ""
        st.session_state.phone = phone
        st.session_state.page = "payment"
        st.rerun()