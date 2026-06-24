import streamlit as st
from db.database import get_cursor
import time


def render():

    if st.button("←"):
        st.session_state.page = "summary"
        st.rerun()

    st.title("결제 및 할인 적용")

    member_id = st.session_state.get("member_id")

    coupon_count = 0
    discount = 0
    use_coupon = False
    grade = "비회원"

    # =====================
    # 회원 정보 조회
    # =====================

    if member_id:

        conn, cursor = get_cursor()

        cursor.execute("""
        SELECT stamp, grade
        FROM member
        WHERE member_id=%s
        """, (member_id,))

        result = cursor.fetchone()

        if result:
            coupon_count = result["stamp"]
            grade = result["grade"] or "BRONZE"

        cursor.close()
        conn.close()

    # =====================
    # 쿠폰 사용
    # =====================

    if coupon_count > 0:

        st.write(f"🎟 보유 쿠폰 : {coupon_count}장")

        use_coupon = st.checkbox(
            "쿠폰 사용 (2,000원 할인)"
        )

        if use_coupon:
            discount = 2000

    # =====================
    # 주문 금액 계산
    # =====================

    total_amount = 0

    for item in st.session_state.cart:

        item_total = item["price"]

        if item.get("options"):

            item_total += sum(
                op["extra_price"]
                for op in item["options"]
            )

        total_amount += item_total

    # =====================
    # 등급 할인
    # =====================

    grade_discount = 0

    if grade == "SILVER":

        grade_discount = int(
            total_amount * 0.03
        )

    elif grade == "GOLD":

        grade_discount = int(
            total_amount * 0.05
        )

    total_discount = (
        discount +
        grade_discount
    )

    final_amount = max(
        total_amount - total_discount,
        0
    )

    # =====================
    # 화면 표시
    # =====================

    st.write(f"회원등급 : {grade}")
    st.write(f"주문금액 : {total_amount:,}원")
    st.write(f"등급할인 : {grade_discount:,}원")
    st.write(f"쿠폰할인 : {discount:,}원")
    st.write(f"총 할인금액 : {total_discount:,}원")
    st.write(f"결제금액 : {final_amount:,}원")

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제"]
    )

    # =====================
    # 결제 완료
    # =====================

    if st.button("결제 완료"):

        if not st.session_state.cart:

            st.error(
                "장바구니가 비어 있습니다."
            )

            return

        conn, cursor = get_cursor()

        try:

            takeout_type = (
                "Y"
                if st.session_state.get(
                    "order_type"
                ) == "포장"
                else "N"
            )

            # =====================
            # 주문 저장
            # =====================

            cursor.execute("""
            INSERT INTO orders(
                member_id,
                takeout_type,
                order_date,
                total_amount
            )
            VALUES(
                %s,
                %s,
                NOW(),
                %s
            )
            """, (
                member_id,
                takeout_type,
                final_amount
            ))

            order_id = cursor.lastrowid

            # =====================
            # 주문 상세 저장
            # =====================

            for item in st.session_state.cart:

                menu_price = item["price"]

                option_price = sum(
                    op["extra_price"]
                    for op in item.get(
                        "options",
                        []
                    )
                )

                amount = (
                    menu_price +
                    option_price
                )

                cursor.execute("""
                INSERT INTO order_detail(
                    order_id,
                    menu_id,
                    quantity,
                    menu_price,
                    amount
                )
                VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """, (
                    order_id,
                    item["menu_id"],
                    1,
                    menu_price,
                    amount
                ))

                detail_id = cursor.lastrowid

                # 옵션 저장

                for op in item.get(
                    "options",
                    []
                ):

                    cursor.execute("""
                    INSERT INTO order_option(
                        detail_id,
                        option_id,
                        option_price
                    )
                    VALUES(
                        %s,
                        %s,
                        %s
                    )
                    """, (
                        detail_id,
                        op["option_id"],
                        op["extra_price"]
                    ))

            # =====================
            # 결제 저장
            # =====================

            cursor.execute("""
            INSERT INTO payment(
                member_id,
                order_id,
                final_amt,
                pay_date,
                pay_type
            )
            VALUES(
                %s,
                %s,
                %s,
                CURDATE(),
                %s
            )
            """, (
                member_id,
                order_id,
                final_amount,
                payment
            ))

            # =====================
            # 스탬프 처리
            # =====================

            if member_id:

                if use_coupon:

                    cursor.execute("""
                    UPDATE member
                    SET stamp = stamp - 1
                    WHERE member_id=%s
                    """, (
                        member_id,
                    ))

                # 주문 시 스탬프 1 적립

                cursor.execute("""
                UPDATE member
                SET stamp = stamp + 1
                WHERE member_id=%s
                """, (
                    member_id,
                ))

            # =====================
            # 등급 계산
            # =====================

            if member_id:

                cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(final_amt),
                        0
                    ) total_purchase
                FROM payment
                WHERE member_id=%s
                """, (
                    member_id,
                ))

                total_purchase = cursor.fetchone()[
                    "total_purchase"
                ]

                new_grade = "BRONZE"

                if total_purchase >= 300000:

                    new_grade = "GOLD"

                elif total_purchase >= 100000:

                    new_grade = "SILVER"

                cursor.execute("""
                UPDATE member
                SET grade=%s
                WHERE member_id=%s
                """, (
                    new_grade,
                    member_id
                ))

            conn.commit()

            # =====================
            # 영수증 전달
            # =====================

            st.session_state.order_id = order_id
            st.session_state.payment = payment
            st.session_state.grade = grade

            st.session_state.total_amount = total_amount
            st.session_state.discount = discount
            st.session_state.grade_discount = grade_discount
            st.session_state.total_discount = total_discount
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