import pandas as pd
import yfinance as yf
import os

def download_data():
    #上下3個雙引號寫function的說明
    """
    1.下載yfinance股價數據資料：2330 台積電、2303 聯電、2454 聯發科、2317 鴻海
    2.在目前目錄下建立一個data的資料夾，如果已經有這個資料夾，就不建立
    3.下載的四檔股票必須儲存為4個csv檔，檔名為2330_{當天日期}.csv、2303_{當天日期}.csv
    、2454_{當天日期}.csv、2317_{當天日期}.csv
    4.檔案如果當天已經有下載，就不要再下載
    5.每次下載成功後，刪除舊日期的檔案，只保留最新的一份
    """    
    
    # 定義股票代碼列表
    tickers = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']

    # 獲取今天的日期字串，格式為 YYYY-MM-DD
    today_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    # 檢查並建立data資料夾
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 遍歷所有股票代碼
    for ticker in tickers:
        base_code = ticker.split('.')[0]
        # 規則 3: 建立包含今天日期的檔名
        filename = f"{base_code}_{today_date}.csv"
        filepath = os.path.join(data_dir, filename)

        # 規則 4: 如果當天檔案已存在，則跳過
        if os.path.exists(filepath):
            print(f"{filename} 當天檔案已存在，跳過下載。")
            continue

        try:
            # 下載數據
            print(f"下載股票數據： {ticker}...")
            data = yf.download(ticker, start='2024-01-01',
                               end=today_date,
                               auto_adjust=True,
                               progress=False)  # 關閉下載進度條，讓輸出更簡潔

            if data.empty:
                print(f"找不到 {ticker} 的數據或日期範圍內無資料，跳過。")
                continue

            data.to_csv(filepath)
            print(f"儲存 {ticker} 至 {filepath}")

            # 規則 5: 刪除舊檔案
            print(f"正在清理 {base_code} 的舊檔案...")
            for old_file in os.listdir(data_dir):
                if old_file.startswith(f"{base_code}_") and old_file != filename:
                    os.remove(os.path.join(data_dir, old_file))
                    print(f"已刪除舊檔案： {old_file}")
        except Exception as e:
            print(f"下載 {ticker} 時發生錯誤: {e}")
            

def combine_close_prices():
    """
    組合這四個csv檔成為一個DataFrame，要組合的只有欄位`Close`，也就是當天的收盤價
    - 檔案名稱`2330_xxxx1`欄位名稱為`台積電`
    - 檔案名稱`2303_xxxx1`欄位名稱為`聯電`
    - 檔案名稱`2454_xxxx1`欄位名稱為`聯發科`
    - 檔案名稱`2317_xxxx1`欄位名稱為`鴻海`
    ###Date要顯示今天日期   
    由於今日是例假日或國定假日，股市沒有開盤，所以沒有資料
    解決方法：只顯示csv檔內所有的資料，而不是使用日期 
    """
    data_dir = 'data'
    combined_df = pd.DataFrame()
    
    # 定義股票代碼和對應的中文名稱
    stock_map = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }

    # 遍歷資料夾中的所有檔案
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            base_code = filename.split('_')[0]
            
            if base_code in stock_map:
                try:
                    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                    if 'Close' in df.columns:
                        # 確保 'Close' 欄位是數值型態，無法轉換的會變成 NaN
                        close_prices = pd.to_numeric(df['Close'], errors='coerce')
                        # 將處理過的收盤價加入 combined_df
                        combined_df[stock_map[base_code]] = close_prices
                    else:
                        print(f"檔案 {filename} 中找不到 'Close' 欄位。")
                except Exception as e:
                    print(f"讀取檔案 {filename} 時發生錯誤: {e}")
       
    if combined_df.empty:
        print("\n在 data 資料夾中找不到任何有效的股票數據。")
        return combined_df

    # 【關鍵修正】
    # 移除索引不是有效日期的行 (例如 'Ticker' 或 'Date' 字串)
    # pd.to_datetime 會將無法轉換的索引變成 NaT (Not a Time)
    # .notna() 會篩選出所有轉換成功的行，也就是有效的日期
    combined_df = combined_df[pd.to_datetime(combined_df.index, errors='coerce').notna()]

    # 按照日期排序，確保資料是時間序列
    combined_df.sort_index(inplace=True)

    return combined_df

    
#起始點一定寫在main
def main():
    download_data()
    combined_df = combine_close_prices()
    if not combined_df.empty:
        print("\n合併後的收盤價數據：")
        print(combined_df.head())
        print("...")
        print(combined_df.tail())

#兩個開頭底線是內建的
if __name__ == '__main__':
    main()