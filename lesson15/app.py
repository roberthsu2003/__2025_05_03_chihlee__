import streamlit as st
import lesson15_1 as yf_stock # 匯入我們的主程式

# --- Streamlit 頁面設定 ---
st.set_page_config(page_title="台股儀表板", layout="wide")

st.title("📈 台股收盤價儀表板")
st.caption("資料來源: Yahoo Finance")

# --- 快取資料載入函式 ---
# @st.cache_data 會快取函式的回傳值。當函式被同樣的參數呼叫時，
# Streamlit 會直接回傳快取的結果，而不是重新執行函式，可以大幅提升效能。
@st.cache_data
def load_data():
    """
    從 yf_stock 模組載入並組合股價資料。
    這個函式會被快取，只有在需要時才重新從檔案讀取。
    """
    df = yf_stock.combine_close_prices()
    return df

# --- 主介面 ---

# 建立兩個欄位佈局，左邊窄右邊寬
col1, col2 = st.columns([1, 3])

with col1:
    st.header("控制面板")
    # 按鈕：觸發資料下載
    if st.button("更新/下載最新股價資料"):
        with st.spinner("正在執行資料下載與清理，請稍候..."):
            yf_stock.download_data()
            # 清除快取，以便下次能讀取到最新的資料
            st.cache_data.clear()
        st.success("資料更新完成！")

    # 載入資料
    combined_df = load_data()

    if not combined_df.empty:
        # 多選框：讓使用者選擇要顯示的股票
        st.header("圖表選項")
        all_stocks = combined_df.columns.tolist()
        selected_stocks = st.multiselect(
            "選擇要繪製的股票：",
            options=all_stocks,
            default=all_stocks  # 預設全選
        )
    else:
        st.warning("找不到任何資料，請先點擊按鈕下載。")
        selected_stocks = []

with col2:
    st.header("資料預覽與圖表")
    if not combined_df.empty and selected_stocks:
        # 顯示資料表格，並將數字格式化到小數點後兩位
        st.subheader("合併收盤價資料")
        st.dataframe(combined_df[selected_stocks].style.format("{:.2f}"))

        # 繪製圖表，並設定固定高度
        st.subheader("股價走勢圖")
        st.line_chart(combined_df[selected_stocks], height=400)
    else:
        st.info("資料載入後，將在此處顯示預覽與圖表。")