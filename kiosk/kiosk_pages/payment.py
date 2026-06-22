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
        SELECT coupon_count, grade
        FROM member
        WHERE member_id=%s
        """,(member_id,))

        result = cursor.fetchone()
        grade = "BRONZE"
        if result:
            coupon_count = result["coupon_count"]
            grade = result["grade"]

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
# 등급 할인 계산
    grade_discount = 0

    if grade.upper() == "SILVER":
        grade_discount = int(total_amount * 0.03)

    elif grade.upper() == "GOLD":
        grade_discount = int(total_amount * 0.05)

    # 결제금액 표시
    total_discount = discount + grade_discount

    final_amount = max(
        total_amount - total_discount,
        0
    )

    
    # st.write(f"주문금액 : {total_amount:,}원")
    # st.write(f"할인금액 : {discount:,}원")
    # st.write(f"결제금액 : {final_amount:,}원")
    st.write(f"회원등급 : {grade}")

    st.write(f"주문금액 : {total_amount:,}원")

    st.write(
        f"등급할인 : {grade_discount:,}원"
    )

    st.write(
        f"쿠폰할인 : {discount:,}원"
    )

    st.write(
        f"총 할인금액 : {total_discount:,}원"
    )

    st.write(
        f"결제금액 : {final_amount:,}원"
    )

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
            final_amount
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
        
        
        # 등급재계산
        if member_id:

            # 현재 등급 조회
            cursor.execute("""
            SELECT grade
            FROM member
            WHERE member_id=%s
            """, (member_id,))

            old_grade = cursor.fetchone()["grade"]



            # 누적 구매액 계산
            cursor.execute("""
            SELECT
                SUM(total_amount) AS total_purchase
            FROM orders
            WHERE member_id = %s
            """, (member_id,))

            result = cursor.fetchone()

            total_purchase = result["total_purchase"] or 0

            new_grade = "BRONZE"

            if total_purchase >= 300000:
                new_grade = "GOLD"

            elif total_purchase >= 100000:
                new_grade = "SILVER"

            cursor.execute("""
            UPDATE member
            SET grade = %s
            WHERE member_id = %s
            """, (
                new_grade,
                member_id
            ))
            
            if old_grade != new_grade:
                st.success(
            f"🎉 등급이 {old_grade} → {new_grade}로 승급되었습니다!"
            )


        conn.commit()

        cursor.close()
        conn.close()

        st.session_state.payment = payment
        st.session_state.total_amount = total_amount

        st.session_state.discount = discount
        st.session_state.grade_discount = grade_discount
        st.session_state.total_discount = total_discount

        st.session_state.final_amount = final_amount
        st.session_state.grade = grade

        st.session_state.page = "receipt"

        st.rerun()