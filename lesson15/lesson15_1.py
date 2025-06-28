import yfinance as yf
from datetime import datetime
import os

def download_data():
    """
    1. 下載yfinance的4檔股票資料,股票有:2330.TW,2303.TW,2454.TW,2317.TW
    2. 在目前目錄下建立一個data的資料夾,如果已經有這個資料夾,就不建立
    3. 下載的4檔股票必需儲存為4個csv檔,檔名為2330.csv,2303.csv,2454.csv,2317.csv
    4. 如果已經有這些檔案,就不下載
    """    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    today = datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists('data/2330.csv'):
        tw2330 = yf.download('2330.TW', start='2000-01-01', end=today, auto_adjust=True)
        tw2330.to_csv('data/2330.csv')
    if not os.path.exists('data/2303.csv'):
        tw2303 = yf.download('2303.TW', start='2000-01-01', end=today, auto_adjust=True)
        tw2303.to_csv('data/2303.csv')
    if not os.path.exists('data/2454.csv'):
        tw2454 = yf.download('2454.TW', start='2000-01-01', end=today, auto_adjust=True)
        tw2454.to_csv('data/2454.csv')
    if not os.path.exists('data/2317.csv'):
        tw2317 = yf.download('2317.TW', start='2000-01-01', end=today, auto_adjust=True)
        tw2317.to_csv('data/2317.csv')
        
    
def main():
    download_data()

if __name__ == '__main__':
    main()