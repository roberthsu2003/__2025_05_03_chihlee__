import streamlit as st
import yfinance as yf
import os
import pandas as pd

def download_tw_stocks():
    stock_list = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    from datetime import datetime
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
        df = yf.download(
            stock,
            start="2010-01-01",
            end=today_str,
            auto_adjust=False
        )
        df.to_csv(filepath)

def load_adjclose_dataframe():
    code_to_name = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }
    data_dir = 'data'
    series_dict = {}
    for code, name in code_to_name.items():
        files = [f for f in os.listdir(data_dir) if f.startswith(code+'_') and f.endswith('.csv')]
        if not files:
            continue
        files.sort(reverse=True)
        filepath = os.path.join(data_dir, files[0])
        df = pd.read_csv(filepath, index_col=0)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[~df.index.isna()]
        if 'Adj Close' in df.columns:
            series_dict[name] = df['Adj Close']
    result_df = pd.DataFrame(series_dict)
    return result_df

# --- Streamlit App Start ---
# 初始化 session_state
if 'start_date_selected' not in st.session_state:
    st.session_state.start_date_selected = None
if 'end_date_selected' not in st.session_state:
    st.session_state.end_date_selected = None

with st.spinner('正在下載最新的股票資料...'):
    download_tw_stocks()
with st.spinner('正在載入股票資料...'):
    df = load_adjclose_dataframe()

st.title("台股歷史股價視覺化")
st.write("本應用程式提供台股歷史股價查詢與視覺化功能。請選擇您感興趣的股票及日期區間，即可查看股價走勢圖與詳細數據。")

options = sorted(list(df.columns))
default = [name for name in options if "台積電" in name]
selected = st.multiselect(
    "請選擇股票（可複選）",
    options=options,
    default=default
)

if not df.empty:
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[~df.index.isna()]

    today = pd.to_datetime('today').date()

    # 預設日期區間
    last_7_dates = df.index[-7:]
    start_default = last_7_dates[0].date()
    end_default = last_7_dates[-1].date()

    # 如果 session_state 中的日期為 None，則設定為預設值
    if st.session_state.start_date_selected is None:
        st.session_state.start_date_selected = start_default
    if st.session_state.end_date_selected is None:
        st.session_state.end_date_selected = end_default

    # 快速選擇按鈕
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button('近一週'):
            st.session_state.start_date_selected = max((pd.Timestamp(today) - pd.Timedelta(weeks=1)).date(), df.index[0].date())
            st.session_state.end_date_selected = min(today, df.index[-1].date())
    with col2:
        if st.button('近一月'):
            st.session_state.start_date_selected = max((pd.Timestamp(today) - pd.Timedelta(days=30)).date(), df.index[0].date())
            st.session_state.end_date_selected = min(today, df.index[-1].date())
    with col3:
        if st.button('近三月'):
            st.session_state.start_date_selected = max((pd.Timestamp(today) - pd.Timedelta(days=90)).date(), df.index[0].date())
            st.session_state.end_date_selected = min(today, df.index[-1].date())
    with col4:
        if st.button('今年以來'):
            st.session_state.start_date_selected = max(pd.to_datetime(f'{today.year}-01-01').date(), df.index[0].date())
            st.session_state.end_date_selected = min(today, df.index[-1].date())

    # 日期選擇器
    start_date_input = st.date_input("開始時間", value=st.session_state.start_date_selected, min_value=df.index[0].date(), max_value=df.index[-1].date())
    end_date_input = st.date_input("結束時間", value=st.session_state.end_date_selected, min_value=df.index[0].date(), max_value=df.index[-1].date())

    # 更新 session_state 中的日期
    if start_date_input != st.session_state.start_date_selected:
        st.session_state.start_date_selected = start_date_input
    if end_date_input != st.session_state.end_date_selected:
        st.session_state.end_date_selected = end_date_input

else:
    st.warning("資料為空，無法選擇日期。")
    st.session_state.start_date_selected = None
    st.session_state.end_date_selected = None

if selected and st.session_state.start_date_selected and st.session_state.end_date_selected:
    mask = (df.index.date >= st.session_state.start_date_selected) & (df.index.date <= st.session_state.end_date_selected)
    filtered_df = df.loc[mask, selected]
    filtered_df = filtered_df.apply(pd.to_numeric, errors='coerce')
    filtered_df = filtered_df.dropna(axis=0, how='all').dropna(axis=1, how='all')
    if not filtered_df.empty:
        for col in filtered_df.columns:
            chart_data = filtered_df[[col]].round(0)
            st.subheader(f"{col} 股價走勢")
            # 動態調整y軸起始值
            min_val = chart_data.min().min()
            max_val = chart_data.max().max()
            margin = (max_val - min_val) * 0.1 if max_val > min_val else 1
            y_min = int(min_val - margin)
            y_max = int(max_val + margin)
            # 使用plotly顯示可自訂y軸
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=chart_data.index, y=chart_data[col], mode='lines', name=col))
            fig.update_layout(
                yaxis=dict(range=[y_min, y_max], tickformat=',d'),
                xaxis_title="日期",
                yaxis_title="收盤價",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("篩選後的股價資料")
        st.dataframe(filtered_df.round(2))
    else:
        st.info("所選區間內無可用數值資料")
else:
    st.info("請選擇股票與日期區間")
# --- Streamlit App End ---

