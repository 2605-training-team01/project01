import streamlit as st
from db.database import get_cursor


def render():

    st.title("결제")

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제", "쿠폰"]
    )

    if st.button("결제 완료"):

        conn, cursor = get_cursor()

        total_amount = sum(
            item["price"]
            for item in st.session_state.cart
        )

        # 주문 저장
        cursor.execute("""
        INSERT INTO orders(
            member_id,
            takeout_type,
            total_amount
        )
        VALUES(%s,%s,%s)
        """, (
            None,
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
            None,
            order_id,
            total_amount,
            payment
        ))

        conn.commit()

        cursor.close()
        conn.close()

        st.session_state.payment = payment

        st.session_state.page = "membership"

        st.rerun()