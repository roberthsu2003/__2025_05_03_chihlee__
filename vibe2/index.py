import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm  # 用於計算常態分佈的PDF
import matplotlib.font_manager as fm # 匯入字型管理員

def main():
    st.title("Vibe2 App")
    st.write("Welcome to the Vibe2 application!")

    # --- 設定中文字型 ---
    # 確保 'ChineseFont.ttf' 檔案與您的 index.py 在同一個目錄，或者提供正確的路徑
    font_path = 'ChineseFont.ttf'
    try:
        # 載入字型屬性
        chinese_font = fm.FontProperties(fname=font_path, size=12)
        title_font = fm.FontProperties(fname=font_path, size=12)
    except FileNotFoundError:
        st.error(f"字型檔案未找到：{font_path}。請確保檔案路徑正確，中文將無法正常顯示。")
        # 如果找不到字型，就使用預設字型
        chinese_font = fm.FontProperties(size=14)
        title_font = fm.FontProperties(size=16, weight='bold')


    # 使用 Matplotlib 的物件導向 API
    fig, ax = plt.subplots()

    # --- Streamlit 互動元件 ---
    loc_param = st.slider("選擇常態分佈的平均值 (loc)", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
    # 修正：移除多餘的 scale_param 指派
    scale_param = st.slider("選擇常態分佈的標準差 (scale)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    size_param = st.slider("選擇樣本數量 (size)", min_value=10, max_value=1000, value=50, step=10)
    
    # 產生常態分佈數據
    normal_distribution: np.ndarray = np.random.normal(loc=loc_param, scale=scale_param, size=size_param)

    # 繪製直方圖
    ax.hist(normal_distribution, bins=30, color='#B47157', alpha=0.5, density=True, label='樣本直方圖')

    # 繪製常態分佈的機率密度函數(PDF)曲線
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, loc=loc_param, scale=scale_param)
    ax.plot(x, p, color='red', linewidth=2, label='理論PDF曲線')

    # --- 設定圖表中文標籤 ---
    # 使用 fontproperties 參數來設定中文字型
    ax.set_title("常態分佈與機率密度函數(PDF)疊圖", fontproperties=title_font)
    ax.set_xlabel("數值", fontproperties=chinese_font)
    ax.set_ylabel("密度", fontproperties=chinese_font)
    ax.legend(prop=chinese_font) # 圖例也需要設定字型

    # 在 Streamlit app 中顯示圖表
    st.pyplot(fig)

if __name__ == "__main__":
    main()