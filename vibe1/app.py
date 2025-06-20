import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib
import matplotlib.font_manager as fm

# 設定 matplotlib 字型
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['ChineseFont']
matplotlib.rcParams['axes.unicode_minus'] = False
fm.fontManager.addfont('ChineseFont.ttf')

st.title("常態分佈（高斯分佈）視覺化應用程式")
st.markdown("""
本應用程式可讓你互動式調整常態分佈的平均值、標準差與樣本數，
並即時在網頁上呈現直方圖與常態分佈曲線。
""")

mean = st.number_input("平均值 (mean)", value=80.0)
std = st.number_input("標準差 (std)", value=0.1, min_value=0.01, step=0.01)
size = st.slider("樣本數 (size)", min_value=10, max_value=1000, value=50, step=10)

normal_distribution = np.random.normal(loc=mean, scale=std, size=size)

fig, ax = plt.subplots()
ax.hist(normal_distribution, bins=30, color='#B47157', alpha=0.5, density=True)
xmin, xmax = ax.get_xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, loc=np.mean(normal_distribution), scale=np.std(normal_distribution))
ax.plot(x, p, color='red', linewidth=2)
ax.set_xlabel('Value')
ax.set_ylabel('Density')
ax.set_title('常態分佈直方圖與PDF曲線')
st.pyplot(fig)

with st.expander("顯示產生的 x 值陣列"):
    st.write(x)
