import streamlit as st
import base64

def render():

<<<<<<< HEAD
    # 배경 이미지 불러오기
    with open("in_charge/drink.jpg", "rb") as img_file:
=======
    with open("images/drink.jpg", "rb") as img_file:
>>>>>>> 7479b2a051fb8c9de94c1954f51dac94ed74a551
        img = base64.b64encode(img_file.read()).decode()

    st.markdown(   
        f""" 
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0,0,0,0.35),
                    rgba(0,0,0,0.35)
                ),
                url("data:image/jpeg;base64,{img}");

            background-size: contain;
            background-position: center top;
            background-repeat: no-repeat;
        }}

        div.stButton > button {{
            background-color: rgba(255,255,255,0.95);
            color: #222222; 
            font-size: 120px;
            font-weight: bold;
            border-radius: 15px;
            height: 220px;
            border: none;

            box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 8px 25px rgba(255,255,255,0.25);
        }}
        div.stButton > button span {{
            font-size: 60px !important;
            font-weight: 900 !important;
        }}
        div.stButton > button div {{
            font-size: 30px !important;
        }}   
        </style>
        """,
        unsafe_allow_html=True
    )

<<<<<<< HEAD
    # 제목
    st.markdown(
        """
        <h1 style="
            text-align:center;
            color:white;
            font-size:100px;
            font-weight:bold;
            margin-top:100px;
            margin-bottom:15px;
            text-shadow:2px 2px 8px rgba(0,0,0,0.7);
        ">
            CAFE NET
        </h1>
        """,
        unsafe_allow_html=True
    )
=======
    st.markdown("<div style='height:780px'></div>", unsafe_allow_html=True)
>>>>>>> 7479b2a051fb8c9de94c1954f51dac94ed74a551

    st.markdown("""
    <h2 style="
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:bold;
    text-shadow:2px 2px 5px rgba(0,0,0,0.5);
    ">
    어디서 드시겠어요?
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    text-align:center;
    color:#dddddd;
    font-size:20px;
    margin-top:15px;
    margin-bottom:100px;
    ">
    원하시는 주문 방식을 선택해주세요
    </p>
    """, unsafe_allow_html=True)

    space1, col1, gap, col2, space2 = st.columns([4, 1.2, 0.3, 1.2, 4])

    with col1:
        if st.button("매장", use_container_width=True):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with col2:
        if st.button("포장", use_container_width=True):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([9, 1])

    with col_right:
        if st.button("⚙️"):
            st.session_state.page = "admin_login"
            st.rerun()