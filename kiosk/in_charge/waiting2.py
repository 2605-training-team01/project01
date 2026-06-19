import streamlit as st
import base64
import os


def render():

    with open("in_charge/drink.jpg", "rb") as img_file:
        img = base64.b64encode(img_file.read()).decode()

    with open("fonts/GmarketSansTTFBold.ttf", "rb") as font_file:
        font_base64 = base64.b64encode(font_file.read()).decode()

    st.markdown(
        f"""
        <style>  

        @font-face {{
            font-family: 'GmarketSans';
            src: url(data:font/ttf;base64,{font_base64}) format('truetype');
        }}  

        .block-container {{
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }}

        [data-testid="stHeader"] {{
            display: none;
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

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
            background-color: rgba(195,170,145,0.95);
            color: #222222;

            font-family: 'GmarketSans' !important;

            font-size: 120px;
            font-weight: bold;
            border-radius: 15px;
            height: 120px;
            border: none;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 8px 25px rgba(255,255,255,0.25);
        }}

        div.stButton > button * {{
            font-family: 'GmarketSans' !important;
            font-size: 30px !important;
            font-weight: 300 !important;
        }}

        div.stButton > button div {{
            font-size: 30px !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='height:58vh'></div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <h2 style="
        text-align:center;
        color:#F8F1E6;
        font-size:50px;
        font-weight:bold;
        font-family:'GmarketSans';
        text-shadow:2px 2px 5px rgba(0,0,0,0.5);
    ">
    🍃오늘도  NET' 하게 
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
        text-align:center;
        color:#F5F7FA;
        font-size:20px;
        margin-top:30px;
        margin-bottom:60px;
        ont-family:'GmarketSans';
    ">
    매장 이용 또는 포장을 선택해주세요
    </p>
    """, unsafe_allow_html=True)

    space1, col1, gap1, col2, gap2, col3, space2 = st.columns([3.5, 1.1, 0.3, 1.1, 0.3, 0.4, 3])

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

    with col3:
        if st.button("⚙️"):
            st.session_state.page = "admin_login"
            st.rerun() 