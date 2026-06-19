import streamlit as st
from db.database import get_cursor


def render():

    if st.button("←"):
        st.session_state.page = "summary"
        st.rerun()

    st.title("결제 및 할인 적용")

    member_id = st.session_state.get("member_id")

    coupon_count = 0
    discount = 0
    use_coupon = False

    # 회원 쿠폰(스탬프) 조회

    if member_id:

        conn, cursor = get_cursor()

        # 🚨 수정: coupon_count -> stamp
        cursor.execute("""
        SELECT stamp
        FROM member
        WHERE member_id = %s
        """, (member_id,))

        result = cursor.fetchone()

        if result:
            coupon_count = result["stamp"] # 🚨 수정: stamp

        cursor.close()
        conn.close()


    # 쿠폰 사용 여부

    if coupon_count > 0:

        st.write(f"보유 쿠폰 : {coupon_count}장")

        use_coupon = st.checkbox(
            "쿠폰 사용 (2,000원 할인)"
        )

        if use_coupon:
            discount = 2000


    # 총 주문금액 계산

    total_amount = 0

    for item in st.session_state.cart:

        item_total = item["price"]

        if item.get("options"):

            item_total += sum(
                op["extra_price"]
                for op in item["options"]
            )

        total_amount += item_total

    final_amount = max(
        total_amount - discount,
        0
    )

    st.write(f"주문금액 : {total_amount:,}원")
    st.write(f"할인금액 : {discount:,}원")
    st.write(f"결제금액 : {final_amount:,}원")


    # 결제수단 선택

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제"]
    )


    # 결제 완료

    if st.button("결제 완료"):

        if len(st.session_state.cart) == 0:
            st.error("장바구니가 비어 있습니다.")
            return

        conn, cursor = get_cursor()

        try:

            # ======================
            # ORDERS 저장
            # ======================

            takeout_yn = (
                "Y"
                if st.session_state.get("order_type") == "포장"
                else "N"
            )

            # 🚨 수정: ERD 구조에 맞게 member_id와 total_amount 제외
            cursor.execute("""
            INSERT INTO orders(
            member_id,
            takeout_type,
            order_date,
            total_amount
            )
            VALUES(%s,%s,NOW(),%s)
            """, (
            member_id,
            takeout_yn,
            final_amount 
            ))

            order_id = cursor.lastrowid

            st.session_state.order_id = order_id

            # ORDERS_DETAIL 저장

            for item in st.session_state.cart:

                item_total = item["price"]

                if item.get("options"):

                    item_total += sum(
                        op["extra_price"]
                        for op in item["options"]
                    )

                # 수정: order_detail -> orders_detail, 컬럼명 menu_amt 로 통일
                cursor.execute("""
                INSERT INTO orders_detail(
                    order_id,
                    menu_id,
                    quantity,
                    menu_amt
                )
                VALUES(%s,%s,%s,%s)
                """, (
                    order_id,
                    item["menu_id"],
                    1,
                    item_total
                ))

                detail_id = cursor.lastrowid
            
                # 옵션 저장

                if item.get("options"):

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

            # PAYMENT 저장

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

            # 쿠폰 차감

            if use_coupon and member_id:

                # 🚨 수정: coupon_count -> stamp
                cursor.execute("""
                UPDATE member
                SET stamp = stamp - 1
                WHERE member_id = %s
                """, (member_id,))

            conn.commit()

            # 영수증 전달용

            st.session_state.payment = payment
            st.session_state.total_amount = total_amount
            st.session_state.discount = discount
            st.session_state.final_amount = final_amount

            st.session_state.page = "receipt"

            st.rerun()

        except Exception as e:

            conn.rollback()

            st.error(
                f"결제 처리 중 오류 발생 : {e}"
            )

        finally:

            cursor.close()
            conn.close()

        # 영수증 화면을 위해 데이터 저장
        st.session_state.payment = payment
        st.session_state.total_amount = total_amount
        st.session_state.discount = discount
        st.session_state.final_amount = final_amount
        st.session_state.page = "receipt"

        st.rerun()