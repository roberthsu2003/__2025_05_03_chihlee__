import streamlit as st

st.set_page_config(page_title="Streamlit App 樣板", layout="centered")

st.title("🎈 Streamlit App 樣板")
st.write("這是一個基本的 Streamlit 應用程式範例。你可以在這裡開始開發你的互動式網頁應用。")

st.header("輸入區")
user_input = st.text_input("請輸入一些文字：")

if user_input:
    st.success(f"你輸入的是：{user_input}")

st.header("資料展示區")
st.write("這裡可以放置資料表格、圖表等內容。")

# 範例資料表格
import pandas as pd
data = pd.DataFrame({
    '數字': [1, 2, 3, 4],
    '平方': [1, 4, 9, 16]
})
st.dataframe(data)

st.header("結語")
st.info("歡迎使用 Streamlit，開始打造你的資料應用！")
