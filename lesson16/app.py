import streamlit as st
import yfinance as yf
import os
from datetime import datetime

st.title("台股歷史股價視覺化")

def download_tw_stocks():
    stock_list = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    today_str = datetime.today().strftime('%Y-%m-%d')
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for stock in stock_list:
        stock_code = stock.split('.')[0]
        filename = f"{stock_code}_{today_str}.csv"
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            continue
        # 明確指定 auto_adjust=False，並設定下載日期範圍
        df = yf.download(
            stock,
            start="2010-01-01",
            end=today_str,
            auto_adjust=False
        )
        df.to_csv(filepath)

#可在此呼叫 function 進行測試
download_tw_stocks()

