import streamlit as st
import pandas as pd
from population_density import PopulationDensity

# 設定 Page 的基本資訊
st.set_page_config(
    page_title="台灣人口密度分析",
    page_icon="🇹🇼",
    layout="wide"
)

st.title("台灣各鄉鎮市區人口密度")

# 建立 PopulationDensity 的實例
population_data = PopulationDensity('各鄉鎮市區人口密度.csv')

# 取得處理後的資料
df = population_data.get_processed_data()

# 顯示資料表
st.header("各鄉鎮市區人口密度資料表")
st.dataframe(df)

# 依據'縣市'進行統計
st.header("各縣市人口統計")

# 計算每個縣市的人口總數
population_sum = df.groupby('縣市')['人口數'].sum()

# 計算每個縣市的平均人口密度
population_density_mean = df.groupby('縣市')['人口密度'].mean()

# 建立新的統計結果表格
summary_df = pd.DataFrame({
    '人口總數': population_sum,
    '平均人口密度': population_density_mean.round(2)
})

# 顯示統計結果
st.dataframe(summary_df)
