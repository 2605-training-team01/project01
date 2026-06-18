import streamlit as st
import base64

def render():

    # 배경 이미지 불러오기
    with open("in_charge/drink.jpg", "rb") as img_file:
        img = base64.b64encode(img_file.read()).decode()

    # 배경 이미지 적용
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0,0,0,0.35),
                rgba(0,0,0,0.35)
            ),
            url("data:image/jpeg;base64,{img}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        div.stButton > button {{
            background-color: rgba(123,87,61,0.85);
            color: white;

            height: 140px;
            border-radius: 15px;
            border: none;

            box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }}

        div.stButton > button p {{
            font-size: 30px !important;
            font-weight: bold !important;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 8px 25px rgba(255,255,255,0.25);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

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

    # 문구
    st.markdown(
        """
        <p style="
            text-align:center;
            color:white;
            font-size:50px;
            font-weight:600;
            margin-bottom:80px;
            text-shadow:2px 2px 8px rgba(0,0,0,0.7);
        ">
            일상의 여유로움을 선물합니다
        </p>
        """,
        unsafe_allow_html=True
    )

    # 매장 / 포장 버튼
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏪 매장", use_container_width=True):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with col2:
        if st.button("🛍️ 포장", use_container_width=True):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([9, 1])

    with col_right:
        if st.button("⚙️"):
            st.session_state.page = "admin_login"
            st.rerun()