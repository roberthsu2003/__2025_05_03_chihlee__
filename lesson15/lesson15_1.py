import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def download_data():
    """
    每日下載指定股票的資料，並儲存為CSV檔。

    1. 股票代碼: 2330.TW, 2303.TW, 2454.TW, 2317.TW
    2. 檔案會儲存在 'data' 資料夾內。
    3. 檔案名稱格式為 '代碼_YYYY-MM-DD.csv' (例如: 2330_2023-10-27.csv)。
    4. 如果當日的檔案已存在，則不會重複下載。
    5. 每次成功下載新檔案後，會刪除該股票對應的舊日期檔案，確保只保留最新的一份。
    """
    # 設定股票列表和資料夾名稱
    STOCKS = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    DATA_DIR = 'data'
    START_DATE = '2000-01-01'

    # 確保資料夾存在
    os.makedirs(DATA_DIR, exist_ok=True)

    # 獲取今天的日期字串
    today_str = datetime.now().strftime('%Y-%m-%d')

    for ticker in STOCKS:
        stock_code = ticker.split('.')[0]
        
        # 組合今天的檔案路徑
        today_filename = f"{stock_code}_{today_str}.csv"
        today_filepath = os.path.join(DATA_DIR, today_filename)

        # 1. 檢查今日檔案是否已存在，若存在則跳過
        if os.path.exists(today_filepath):
            print(f"'{today_filepath}' 今日已下載，跳過。")
            continue

        # 2. 下載資料
        print(f"正在下載 {ticker} 的資料...")
        try:
            data = yf.download(ticker, start=START_DATE, end=today_str, auto_adjust=True)
            if data.empty:
                print(f"警告：找不到 {ticker} 的資料，跳過儲存。")
                continue
            
            # 3. 儲存為今日的檔案
            data.to_csv(today_filepath)
            print(f"成功儲存資料至 '{today_filepath}'")

            # 4. 刪除此股票的舊檔案
            for filename in os.listdir(DATA_DIR):
                # 檢查檔案是否為此股票的舊CSV檔
                if filename.startswith(f"{stock_code}_") and filename.endswith(".csv") and filename != today_filename:
                    old_filepath = os.path.join(DATA_DIR, filename)
                    os.remove(old_filepath)
                    print(f"已刪除舊檔案: {old_filepath}")
        except Exception as e:
            print(f"下載 {ticker} 時發生錯誤: {e}")

def create_close_price_dataframe():
    """
    讀取 data 資料夾中的股票 CSV 檔，整合成一個包含所有收盤價的 DataFrame。

    Returns:
        pandas.DataFrame: 整合後的 DataFrame，索引為日期，欄位為股票中文名稱。
                          如果找不到任何資料，則返回 None。
    """
    DATA_DIR = 'data'
    STOCK_MAPPING = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }

    if not os.path.isdir(DATA_DIR):
        print(f"錯誤：資料夾 '{DATA_DIR}' 不存在。請先執行 download_data()。")
        return None

    all_dataframes = []
    
    try:
        files_in_data = os.listdir(DATA_DIR)
    except FileNotFoundError:
        print(f"錯誤：資料夾 '{DATA_DIR}' 不存在。")
        return None

    for code, name in STOCK_MAPPING.items():
        # 使用 next 和生成器表達式來尋找檔案，更簡潔
        stock_file = next((f for f in files_in_data if f.startswith(f"{code}_") and f.endswith(".csv")), None)
        
        if stock_file:
            filepath = os.path.join(DATA_DIR, stock_file)
            try:
                # 修正：讀取時將第一欄作為 index，並解析為日期
                df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                # 只保留 Close 欄位，並重新命名
                df = df[['Close']].rename(columns={'Close': name})
                all_dataframes.append(df)
            except Exception as e:
                print(f"處理檔案 {filepath} 時發生錯誤: {e}")
        else:
            print(f"警告：在 '{DATA_DIR}' 中找不到股票代碼 {code} 的資料檔。")

    if not all_dataframes:
        print("沒有成功讀取任何股票資料，無法建立 DataFrame。")
        return None

    # 合併所有 DataFrame
    final_df = pd.concat(all_dataframes, axis=1)
    final_df.sort_index(inplace=True)
    return final_df

def main():
    download_data()
    close_prices_df = create_close_price_dataframe()
    
    if close_prices_df is not None:
        print("\n==========================================")
        print("整合後的四支股票收盤價資料 (最新5筆):")
        print("==========================================")
        print(close_prices_df.tail())

if __name__ == '__main__':
    main()