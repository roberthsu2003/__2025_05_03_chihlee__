import streamlit as st
from population_density import PopulationDensity
import os

st.title("各鄉鎮市區人口密度資料表")

csv_path = os.path.join(os.path.dirname(__file__), "各鄉鎮市區人口密度.csv")
pd_module = PopulationDensity(csv_path)
data = pd_module.get_dataframe()
err = pd_module.get_error()
if data is not None:
    # 移除最後7行，將 None/NaN 轉為 0，型態轉換
    display_data = data.iloc[:-7] if len(data) > 7 else data
    display_data = display_data.fillna(0)
    display_data['人口數'] = display_data['人口數'].astype(int)
    display_data['面積'] = display_data['面積'].astype(float)
    display_data['人口密度'] = display_data['人口密度'].astype(float)
    # 拆分「鄉鎮市區」欄位
    display_data = display_data.reset_index()
    display_data['縣市'] = display_data['鄉鎮市區'].str[:3]
    display_data['鄉鎮市區'] = display_data['鄉鎮市區'].str[3:]
    display_data.set_index('縣市', inplace=True)
    # 千分位格式化
    display_data['人口數'] = display_data['人口數'].map(lambda x: f"{x:,}")
    display_data['面積'] = display_data['面積'].map(lambda x: f"{x:,.2f}")
    st.dataframe(display_data)
    
    # 依據縣市分組統計
    st.subheader("各縣市人口總數與平均人口密度統計表")
    # 將人口數與人口密度欄位還原為數值型態以便計算
    stat_data = data.iloc[:-7] if len(data) > 7 else data
    stat_data = stat_data.reset_index()
    stat_data['縣市'] = stat_data['鄉鎮市區'].str[:3]
    stat_data['人口數'] = stat_data['人口數'].fillna(0).astype(int)
    stat_data['人口密度'] = stat_data['人口密度'].fillna(0).astype(float)
    # 分組計算
    stat_table = stat_data.groupby('縣市').agg(人口總數=('人口數', 'sum'), 平均人口密度=('人口密度', 'mean')).reset_index()
    # 千分位格式化
    stat_table['人口總數'] = stat_table['人口總數'].map(lambda x: f"{x:,}")
    stat_table['平均人口密度'] = stat_table['平均人口密度'].map(lambda x: f"{x:,.2f}")
    st.dataframe(stat_table)
elif err:
    st.error(err)
else:
    st.warning("找不到或無法讀取 各鄉鎮市區人口密度.csv 檔案。請確認檔案已放在 lesson17 資料夾內。")
