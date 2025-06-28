**專案目標 (Project Goal)** 我們要建立一個使用 Streamlit 驅動的 Web 應用程式，用於視覺化台股歷史股價。

**核心功能 (Core Features)**

1. **資料獲取**：能夠使用 `yfinance` 套件下載指定的台股歷史資料。
2. **專案資料夾**:lesson16
2. **互動介面**：
    - 提供股票選單，讓使用者可以選擇想查詢的股票。
    - 提供日期區間選擇器，讓使用者能篩選特定時間範圍的資料。
    - 以表格形式顯示篩選後的股價資料。
    - 以折線圖形式視覺化所選股票在指定時間內的價格走勢。

**開發流程與規則 (Development Workflow & Rules)**

1. **迭代開發**：我們將採用迭代（step-by-step）的方式完成這個專案。
2. **任務清單 (Todolist)**：在每一次的互動中，我會提供一個任務清單。
3. **您的任務**：
    - 請先檢查清單中已完成的項目 (`[x]`)。
    - 接著，請完成清單中**尚未**完成的項目 (`[]`)。
    - 完成後，請在您的回覆中更新任務清單，將您剛完成的項目打勾 (`[x]`)。

---

**本階段任務 (Current Task)**

**Todolist**
- [x] yfinance套件已經安裝
- [x] 建立streamlit專案的初始檔案 `app.py`。
- [x] 請建立一個下載台股歷史資料的 function，具體需求如下：

    1. 使用 `yfinance` 套件下載以下四檔股票的歷史資料：`2330.TW`, `2303.TW`, `2454.TW`, `2317.TW`。
    2. 下載後，將每一檔股票的資料儲存為 CSV 檔案，檔名格式為：`2330_YYYY-MM-DD.csv`，其中 `YYYY-MM-DD` 為當天日期。
    3. 如果專案資料夾中沒有 `data` 資料夾，請自動建立一個 `data` 資料夾。
    4. 如果 `data` 資料夾中已經有當天的檔案，請不要重複下載。
    5. 如果沒有當天的檔案，才進行下載並儲存。每一檔股票每天只需一個檔案。
- [x] 請修改 `download_tw_stocks()` function，具體需求如下：

    1. 修正 yfinance 的 FutureWarning 警告：  
       警告內容為 `YF.download() has changed argument auto_adjust default to True`。請在呼叫 `yf.download()` 時，明確指定 `auto_adjust=False` 參數，以消除警告。
    2. 下載資料的起始日期需設定為 `2010-01-01`，結束日期為當天日期（即 `end` 參數為今天）。

- [x] 請建立一個 function，具體需求如下：

    1. 讀取 `data` 資料夾內的每個 csv 檔案。
    2. 對每個 csv 檔案，僅取出 `Adj Close` 欄位（不需要 `Ticker` 欄位），並將其轉為 pandas Series。
    3. 將這 4 個 Series 合併成一個 DataFrame，DataFrame 需有 4 個欄位，且欄位名稱需依據股票代碼對應為：
        - `2330.TW` → `台積電`
        - `2303.TW` → `聯電`
        - `2454.TW` → `聯發科`
        - `2317.TW` → `鴻海`
    4. 此 function 最後回傳這個 DataFrame。


