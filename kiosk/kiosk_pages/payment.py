import streamlit as st
from db.database import get_cursor

def render():

    if st.button("←"):
        st.session_state.page = "summary"
        st.rerun()

    st.title("💳 결제 및 할인 적용")

    member_id = st.session_state.get("member_id")

    coupon_count = 0
    discount = 0
    use_coupon = False

    # 1. 단골손님 쿠폰(스탬프) 개수 조회
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

    # 2. 쿠폰 사용 여부 체크
    if coupon_count > 0:
        st.write(f"🎟 보유 쿠폰 : {coupon_count}장")
        use_coupon = st.checkbox("쿠폰 사용 (2,000원 할인)")

        if use_coupon:
            discount = 2000

    # 3. 옵션 가격까지 포함한 총 결제 금액
    total_amount = 0
    for item in st.session_state.cart:
        item_price = item["price"]
        if item.get("options"):
            
            item_price += sum(op["extra_price"] for op in item["options"])
        total_amount += item_price

    
    final_amount = max(total_amount - discount, 0)
    
    st.write(f"주문금액 : {total_amount:,}원")
    st.write(f"할인금액 : {discount:,}원")
    st.write(f"결제금액 : {final_amount:,}원")

    payment = st.radio("결제 수단", ["카드", "간편결제"])

    if st.button("결제 완료"):
        conn, cursor = get_cursor()

        # 4. 주문(orders) 저장
        takeout_yn = "Y" if st.session_state.get("order_type") == "포장" else "N"
        cursor.execute("""
        INSERT INTO orders(takeout_type, order_date)
        VALUES(%s, NOW())
        """, (takeout_yn,))

        order_id = cursor.lastrowid
        st.session_state.order_id = order_id

        # 5. 주문 상세 저장
        for item in st.session_state.cart:
            # 개별 메뉴의 총 금액(기본가 + 옵션가)을 다시 계산
            item_total = item["price"]
            if item.get("options"):
                item_total += sum(op["extra_price"] for op in item["options"])
                
            cursor.execute("""
            INSERT INTO orders_detail(order_id, menu_id, quantity, menu_amt)
            VALUES(%s, %s, %s, %s)
            """, (order_id, item["menu_id"], 1, item_total))

            detail_id = cursor.lastrowid

            # 6. 옵션 저장
            if item.get("options"):
                for op in item["options"]:
                    cursor.execute("""
                    INSERT INTO order_option(detail_id, option_id, option_price)
                    VALUES(%s, %s, %s)
                    """, (detail_id, op["option_id"], op["extra_price"]))

        # 7. 결제(payment) 저장
        cursor.execute("""
        INSERT INTO payment(member_id, order_id, final_amt, pay_date, pay_type)
        VALUES(%s, %s, %s, NOW(), %s)
        """, (member_id, order_id, final_amount, payment))

        # 8. 쿠폰 차감
        if use_coupon and member_id:
            cursor.execute("""
            UPDATE member
            SET coupon_count = coupon_count - 1
            WHERE member_id=%s
            """,(member_id,))

        conn.commit()

        cursor.close()
        conn.close()

        # 영수증 화면을 위해 데이터 저장
        st.session_state.payment = payment
        st.session_state.total_amount = total_amount
        st.session_state.discount = discount
        st.session_state.final_amount = final_amount
        st.session_state.page = "receipt"

        st.rerun()