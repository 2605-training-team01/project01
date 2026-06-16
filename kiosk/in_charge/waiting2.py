import streamlit as st
import base64

def render():

    with open("in_charge/drink.jpg", "rb") as img_file:
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

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        div.stButton > button {{
            background-color: rgba(123,87,61,0.85);
            color: white;
            font-size: 24px;
            font-weight: bold;
            border-radius: 15px;
            height: 90px;
            border: none;

            box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 8px 25px rgba(255,255,255,0.25);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:550px'></div>", unsafe_allow_html=True)

    st.markdown(
        """
    <h2 style="
        text-align:center;
        color:white;
        margin-bottom:20px;
        margin-left:980px;
        text-shadow:2px 2px 5px rgba(0,0,0,0.5);
    ">
         👇 주문 방식을 선택해 주세요
    </h2>
    """,
    unsafe_allow_html=True
)
    space, col1, col2 = st.columns([3, 1, 1])

    with col1:
        if st.button("🏪 매장", use_container_width=True):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with col2:
        if st.button("🥡 포장", use_container_width=True):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()