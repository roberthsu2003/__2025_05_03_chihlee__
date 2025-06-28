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

- [x] 請建立一個 Streamlit 應用程式，具體需求如下：

    1. 畫面上需有一個標題（title）。
    2. 版面需分為兩個 column。
    3. 在左側 column，建立一個多選下拉式選單（multiselect），
       - 預設選項為「台積電2330.TW」。
       - 其它選項依據 `load_adjclose_dataframe()` 回傳的 DataFrame 欄位名稱動態產生。

- [x] 請完成以下兩項任務：

    1. 解決 Streamlit 應用程式出現的警告訊息：
        ```
        /Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py:48: UserWarning: Could not infer format, so each element will be parsed individually, falling back to `dateutil`. To ensure parsing is consistent and as-expected, please specify a format.
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)
        ```
        請在讀取 CSV 時，明確指定日期格式，避免出現此警告。

    2. 確保每次執行 Streamlit 應用程式時都會自動執行 `download_tw_stocks()`，以檢查並下載最新的資料檔案。

- [x]請解決以下問題：
    ```
    time data "Ticker" doesn't match format "%Y-%m-%d", at position 0. You might want to try: - passing `format` if your strings have a consistent format; - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format; - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.
Traceback:
File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 61, in <module>
    df = load_adjclose_dataframe()
File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 49, in load_adjclose_dataframe
    df = pd.read_csv(filepath, index_col=0, parse_dates=True, date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 1026, in read_csv
    return _read(filepath_or_buffer, kwds)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 626, in _read
    return parser.read(nrows)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 1923, in read
    ) = self._engine.read(  # type: ignore[attr-defined]
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/c_parser_wrapper.py", line 333, in read
    index, column_names = self._make_index(date_data, alldata, names)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/base_parser.py", line 372, in _make_index
    index = self._agg_index(simple_index)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/base_parser.py", line 469, in _agg_index
    arr = self._date_conv(
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/io/parsers/base_parser.py", line 1213, in converter
    pre_parsed = parsing.try_parse_dates(
File "parsing.pyx", line 799, in pandas._libs.tslibs.parsing.try_parse_dates
File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 49, in <lambda>
    df = pd.read_csv(filepath, index_col=0, parse_dates=True, date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/tools/datetimes.py", line 1101, in to_datetime
    result = convert_listlike(np.array([arg]), format)[0]
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/tools/datetimes.py", line 433, in _convert_listlike_datetimes
    return _array_strptime_with_fallback(arg, name, utc, format, exact, errors)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/tools/datetimes.py", line 467, in _array_strptime_with_fallback
    result, tz_out = array_strptime(arg, fmt, exact=exact, errors=errors, utc=utc)
File "strptime.pyx", line 501, in pandas._libs.tslibs.strptime.array_strptime
File "strptime.pyx", line 451, in pandas._libs.tslibs.strptime.array_strptime
```
- [x] 請在左側欄位（column）中，於股票多選選單下方，新增讓使用者選擇「開始時間」和「結束時間」的日期選擇器。
    - 預設值為 DataFrame 最後 7 個交易日的日期範圍（即預設顯示最近 7 天的資料）。
    - 由於股市開市日並非連續日期，請根據 DataFrame 的 index 取最後 7 筆日期作為預設值。

- [x] 錯誤解決:

```
AttributeError: 'str' object has no attribute 'date'

File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 79, in <module>
    start_default = last_7_dates[0].date()
```
- [x]錯誤解決:
```
pandas._libs.tslibs.parsing.DateParseError: Unknown datetime string format, unable to parse: Ticker, at position 0

File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 80, in <module>
    df.index = pd.to_datetime(df.index)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/tools/datetimes.py", line 1076, in to_datetime
    result = convert_listlike(arg, format, name=arg.name)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/tools/datetimes.py", line 435, in _convert_listlike_datetimes
    result, tz_parsed = objects_to_datetime64(
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/core/arrays/datetimes.py", line 2398, in objects_to_datetime64
    result, tz_parsed = tslib.array_to_datetime(
File "tslib.pyx", line 414, in pandas._libs.tslib.array_to_datetime
File "tslib.pyx", line 596, in pandas._libs.tslib.array_to_datetime
File "tslib.pyx", line 553, in pandas._libs.tslib.array_to_datetime
File "conversion.pyx", line 641, in pandas._libs.tslibs.conversion.convert_str_to_tsobject
File "parsing.pyx", line 336, in pandas._libs.tslibs.parsing.parse_datetime_string
File "parsing.pyx", line 666, in pandas._libs.tslibs.parsing.dateutil_parse
```


