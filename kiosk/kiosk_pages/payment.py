import streamlit as st
from db.database import get_cursor

def render():
    st.title("💳 결제 및 포인트 적립")

    if st.button("←"):
        st.session_state.page = "summary"
        st.rerun()

    payment = st.radio(
        "결제 수단",
        ["카드", "간편결제", "쿠폰"]
    )

    # 2. 결제 완료
    if st.button("결제 완료"):
        conn, cursor = get_cursor()

        
        total_amount = sum(
            item["price"] for item in st.session_state.cart
        )

        # 3. 주문 정보 장부에 적기
        cursor.execute("""
        INSERT INTO orders(takeout_type, order_date)
        VALUES(%s, NOW())
        """, ("Y" if st.session_state.get("order_type") == "포장" else "N"))

        order_id = cursor.lastrowid # 방금 생성된 주문번호

     
        for item in st.session_state.cart:
            cursor.execute("""
            INSERT INTO orders_detail(order_id, menu_id, quantity, menu_amt)
            VALUES(%s, %s, %s, %s)
            """, (order_id, item["menu_id"], 1, item["price"]))


        member_id = st.session_state.get("member_id", None)

        if member_id is not None:
            # 음료 한 잔당 스탬프 1개씩 적립
            earned_stamps = len(st.session_state.cart) 

            # 데이터베이스 장부(member 테이블)로 가서 해당 회원의 스탬프 개수를 늘림
            cursor.execute("""
            UPDATE member 
            SET stamp = stamp + %s 
            WHERE member_id = %s
            """, (earned_stamps, member_id))
            
           
            st.success(f"🎉 회원님! 스탬프 {earned_stamps}개가 새로 적립되었습니다!")
        else:
            
            st.info("비회원 주문이므로 포인트가 적립되지 않습니다.")


        # 4. 결제 완료 및 정보 저장
        cursor.execute("""
        INSERT INTO payment(member_id, order_id, final_amt, pay_date, pay_type)
        VALUES(%s, %s, %s, NOW(), %s)
        """, (member_id, order_id, total_amount, payment))

        conn.commit()

        cursor.close()
        conn.close()

   
        st.session_state.page = "receipt"
        st.rerun()