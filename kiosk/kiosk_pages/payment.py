import streamlit as st
from db.database import get_cursor

def render():

    if st.button("←"):
            st.session_state.page = "summary"
            st.rerun()

    st.title("💳 결제 및 포인트 적립")

    member_id = st.session_state.get("member_id")

    coupon_count = 0
    discount = 0
    use_coupon = False

    if member_id:

        conn, cursor = get_cursor()

        cursor.execute("""
        SELECT coupon_count
        FROM member
        WHERE member_id=%s
        """,(member_id,))

        result = cursor.fetchone()

        if result:
            coupon_count = result["coupon_count"]

        cursor.close()
        conn.close()


    if coupon_count > 0:

        st.write(f"🎟 보유 쿠폰 : {coupon_count}장")

        use_coupon = st.checkbox(
            "쿠폰 사용 (2000원 할인)"
        )

        if use_coupon:
            discount = 2000


    total_amount = sum(
        item["price"]
        for item in st.session_state.cart
    )

    # 결제금액 표시
    final_amount = max(
        total_amount - discount,
        0
    )

    
    st.write(f"주문금액 : {total_amount:,}원")
    st.write(f"할인금액 : {discount:,}원")
    st.write(f"결제금액 : {final_amount:,}원")

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제"]
    )


    if st.button("결제 완료"):

        conn, cursor = get_cursor()



        # 주문 저장
        cursor.execute("""
        INSERT INTO orders(
            member_id,
            takeout_type,
            total_amount
        )
        VALUES(%s,%s,%s)
        """, (
            member_id,
            "Y" if st.session_state.order_type == "포장"
            else "N",
            total_amount
        ))

        order_id = cursor.lastrowid

        st.session_state.order_id = order_id

        # 주문 상세 저장
        for item in st.session_state.cart:

            cursor.execute("""
            INSERT INTO order_detail(
                order_id,
                menu_id,
                quantity,
                menu_price,
                amount
            )
            VALUES(%s,%s,%s,%s,%s)
            """, (
                order_id,
                item["menu_id"],
                1,
                item["price"],
                item["price"]
            ))

            detail_id = cursor.lastrowid

            # 옵션 저장
            for op in item["options"]:

                cursor.execute("""
                INSERT INTO order_option(
                    detail_id,
                    option_id,
                    option_price
                )
                VALUES(%s,%s,%s)
                """, (
                    detail_id,
                    op["option_id"],
                    op["extra_price"]
                ))

        # 결제 저장
        cursor.execute("""
        INSERT INTO payment(
            member_id,
            order_id,
            final_amt,
            pay_date,
            pay_type
        )
        VALUES(%s,%s,%s,NOW(),%s)
        """, (
            member_id,
            order_id,
            final_amount,
            payment
        ))

        # 쿠폰차감
        if use_coupon and member_id:

            cursor.execute("""
            UPDATE member
            SET coupon_count = coupon_count - 1
            WHERE member_id=%s
            """,(member_id,))

        conn.commit()

        cursor.close()
        conn.close()

        st.session_state.payment = payment
        st.session_state.total_amount = total_amount
        st.session_state.discount = discount
        st.session_state.final_amount = final_amount

        st.session_state.page = "receipt"

        st.rerun()