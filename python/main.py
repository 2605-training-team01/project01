import streamlit as st
import pandas as pd

st.title("카페 키오스크")

# 메뉴 데이터
menu_data = [
    {"category": "커피", "name": "아메리카노", "price": 4500},
    {"category": "커피", "name": "카페라떼", "price": 5000},
    {"category": "커피", "name": "카푸치노", "price": 5500},

    {"category": "음료", "name": "레몬에이드", "price": 6000},
    {"category": "음료", "name": "자몽에이드", "price": 6500},

    {"category": "디저트", "name": "치즈케이크", "price": 7000},
    {"category": "디저트", "name": "초코머핀", "price": 3500}
]

df = pd.DataFrame(menu_data)

# 카테고리 목록 생성
categories = df["category"].unique()

# 카테고리 선택
selected_category = st.selectbox(
    "카테고리를 선택하세요",
    categories
)

# 선택한 카테고리 메뉴 조회
filtered_df = df[df["category"] == selected_category]

st.subheader(f"{selected_category} 메뉴")

st.dataframe(
    filtered_df[["name", "price"]],
    use_container_width=True
)