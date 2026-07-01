# pages/menu.py
import streamlit as st
import base64
from db.database import get_cursor

def render():

    # 폰트 읽기
    try:
        with open("fonts/PretendardVariable.ttf", "rb") as font_file:
            pretendard_base64 = base64.b64encode(font_file.read()).decode()
    except FileNotFoundError:
        pretendard_base64 = ""

    # f""" 내부에서 CSS의 { } 중괄호와 충돌하지 않도록 폰트 주입 부분만 분리
    st.markdown(f"""
    <style>
    @font-face {{
        font-family: "Pretendard";
        src: url(data:font/ttf;base64,{pretendard_base64}) format("truetype");
    }}
    </style>
    """, unsafe_allow_html=True)

    # 나머지 일반 CSS는 f를 제외한 순수 """ 문자열로 처리하여 중괄호 에러 차단
    st.markdown("""
    <style>
    
    /* 전체 앱 요소에 프리텐다드 폰트 적용 */
    html, body, [class*="st-"], div, p, h1, h2, h3, button {
        font-family: "Pretendard", sans-serif !important;
    }
    
    /* 💡 최상단 타이틀 h1 요소를 완전한 볼드체(800)로 지정 */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin: 0 !important;
        display: inline-block !important;
    }

    h3 {
        margin: 16px 0 0 0 !important;
        color: #666666 !important;
        font-weight: 500 !important;
        font-size: 18px !important;
    }
                
    .stApp {
        background:
            radial-gradient(circle at top left, #FFF8F0 0%, transparent 35%),               
            radial-gradient(circle at bottom right, #F5EFE7 0%, transparent 30%),
            linear-gradient(
                180deg,  
                #FCFBF8 0%,
                #F8F4EE 50%,
                #FCFBF8 100%
            );
    }

    /* layout="wide" 상태에서 전체 화면의 최대 너비를 1200px로 제한하고 중앙 정렬 */
    .block-container {
        max-width: 1200px !important; 
        margin: 0 auto !important;    
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
                                
    div[data-testid="stButton"] > button {
        background-color: white !important;
        color: #222 !important;
                
        border: none;
        border-bottom: 3px solid transparent;
        border-radius: 0;
                
        font-size: 24px;
        font-weight: 700;
        height: 58px;
    }

    div[data-testid="stButton"] > button p {
             font-size: 25px !important;
             font-weight: 700 !important;
    }
                                                       
    div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }                        
                
    /* 선택된 탭 */            
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #f2f2f2 !important;
        color: #222 !important;
        border-bottom: 3px solid #222 !important;
    }
                
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #222 !important;
        color: white !important;   

        border-radius: 10px !important;
        border: none !important;  

        height: 48px !important;

        font-size: 16px !important;
        font-weight: 600 !important;
                
        box-shadow: none !important;
    }        
                                              
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background:#333 !important;  
    }
                
    div[data-testid="stButton"] > button:hover {
        border-bottom: 3px solid #222;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0px !important; /* 카드 내부 요소들이 붕 뜨는 현상 방지 */
    }
                
    /* 상단 카테고리 전체 박스 스타일링 */
    [class*="st-key-category_box"] {
        background: #ffffff !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.10) !important;
        padding: 16px 24px !important; 
        margin-top: 35px !important;    
        margin-bottom: 50px !important; 
        border: none !important; 
        overflow: hidden !important;        
    }
                
    /* 메뉴 카드 컨테이너 스타일링 */
    [class*="st-key-card_"] {
        background: #ffffff !important;
        border: none !important; 
        border-radius: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.10) !important;  
        padding: 12px !important; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 50px !important; 
        overflow: hidden !important; 
    }            

    [class*="st-key-card_"]:hover {
        transform: translateY(-6px);  
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
    }

    /* 2열 레이아웃 카드 사이의 좌우 간격(gap) 넓히기 */
    div[data-testid="stColumnsHorizontal"] {
        gap: 50px !important; 
    }

    /* 💡 [수정] 식상함 제로! 깊이감 있는 입체적 그림자 + 모던 감성 소프트 브라운 타원형 박스 */
    .order-badge-style {
        display: inline-block !important;
        white-space: nowrap !important;
        background-color: #5E5049 !important; /* ☕ 따뜻하고 세련된 카페 감성의 마일드 딥 브라운 */
        color: #ffffff !important;
        padding: 10px 28px !important; /* 내부 여백을 더 넓혀 글자가 웅장하고 시원하게 배치되도록 수정 */
        border-radius: 50px !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        
        /* 다층 구조의 고급스러운 소프트 입체 그림자(Box-shadow) 적용 */
        box-shadow: 
            0 8px 24px rgba(94, 80, 73, 0.25), 
            0 2px 6px rgba(94, 80, 73, 0.15) !important;
    }
     
    </style>
    """, unsafe_allow_html=True)                

    conn, cursor = get_cursor()    

    # 카테고리 조회
    cursor.execute("""
    SELECT category_name
    FROM category
    ORDER BY category_code
    """)

    categories = [
        row["category_name"]
        for row in cursor.fetchall()
    ]

    # 메뉴 조회
    cursor.execute("""
    SELECT
        c.category_name,
        m.menu_id,
        m.menu_name,
        m.menu_price,
        m.menu_image
    FROM menu m
    JOIN category c
        ON m.category_code = c.category_code
    ORDER BY
        c.category_code,
        m.menu_id
    """)

    menu_rows = cursor.fetchall()

    # 최근 7일 간 3개 이상 판매된 메뉴 조회    
    cursor.execute(
    """SELECT
        c.category_name,
        od.menu_id,
        SUM(od.quantity) AS total_qty
    FROM order_detail od
    JOIN orders om
        ON od.order_id = om.order_id
    JOIN menu m
        ON od.menu_id = m.menu_id
    JOIN category c
        ON m.category_code = c.category_code
    WHERE
        om.order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    GROUP BY
        c.category_name,
        od.menu_id
    HAVING
        SUM(od.quantity) >= 3;
    """
    )
    best_rows = cursor.fetchall()
    
    # 메뉴 그룹화
    menu_dict = {}

    for row in menu_rows:
        category_name = row["category_name"]
        if category_name not in menu_dict:
            menu_dict[category_name] = []
        menu_dict[category_name].append(dict(row))

    order_type = st.session_state.get("order_type", "매장")

    # 💡 상단 마진을 더 확보하여 웅장하게 출력
    st.markdown(f"""
    <div style="margin-top: 35px; margin-bottom: 30px;">
        <span class="order-badge-style">{order_type} 주문</span>
        <h3>원하시는 메뉴를 선택해 주세요</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 카테고리 버튼 UI
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = categories[0] if categories else None

    # 카테고리 박스 컨테이너
    with st.container(border=True, key="category_box"):
        tab_cols = st.columns(len(categories))

        for idx, category_name in enumerate(categories):
            is_selected = (category_name == st.session_state.selected_category)
            with tab_cols[idx]:
                if st.button(
                    category_name,
                    key=f"tab_{idx}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ): 
                    st.session_state.selected_category = category_name
                    st.rerun()       
                
    selected_category = st.session_state.selected_category
    filtered_menu = menu_dict.get(selected_category, [])

    # 메뉴 출력 영역 (2열 레이아웃)
    menu_cols = st.columns(2)

    for idx, menu in enumerate(filtered_menu):
        with menu_cols[idx % 2]:
            with st.container(border=True, key=f"card_{menu['menu_id']}"):
                                
                image_path = menu.get("menu_image")

                if image_path:
                    st.image(image_path, use_container_width=True)     

                st.markdown(
                    f"""
                    <p style="
                        margin: 20px 0 16px 0; 
                        font-size: 30px; 
                        font-weight: 600;
                        text-align: center;
                    ">    
                        {menu['menu_price']:,}원
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "🛒 주문하기",
                    key=f"menu_{menu['menu_id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.selected_menu = dict(menu)
                    st.session_state.page = "option"
                    conn.close()
                    st.rerun()
             
# -----------------------------
# 하단 장바구니 영역
# -----------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    cart_count = len(st.session_state.cart)
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### 🛒 장바구니 {cart_count}개")
        
    with col2:
        st.write("")
        if st.button("장바구니 보기", use_container_width=True):
            st.session_state.page = "summary"
            st.rerun()
            
    conn.close()