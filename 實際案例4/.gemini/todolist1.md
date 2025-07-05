# 專案任務清單 (Project Todolist)

- [x] **任務 1: 建立 CLI 應用程式框架 (`app.py`)**
    - 建立 `app.py` 檔案。
    - 使用 `argparse` 模組設定命令列介面，需包含 `--csv` (輸入) 和 `--excel` (輸出) 兩個參數。

- [x] **任務 2: 實作資料讀取功能**
    - 在 `app.py` 中，使用 `pandas` 讀取由 `--csv` 參數指定的 CSV 檔案。

- [x] **任務 3: 實作樞紐分析表建立功能**
    - 使用 `pandas` 的 `pivot_table` 功能，對讀入的資料進行處理。
    - *注意：樞紐分析表的具體欄位設定將在後續步驟中提供。*

- [x] **任務 4: 實作檔案匯出功能**
    - 將產生的樞紐分析表 DataFrame 匯出至由 `--excel` 參數指定的 Excel 檔案。

- [x] **任務 5: 程式碼輸出請依據lesson17_2.ipynb**
    - 確保程式碼符合 `WORKSPACE.md` 中的規範。
    - 使用 `pandas` 的 `to_excel` 方法將 DataFrame 匯出為 Excel 檔案。
- [x] **任務 6: 完善程式碼與註解**
    - 確保所有函式都有符合 `WORKSPACE.md` 規範的 docstring 說明。
    - 整合所有功能，讓程式可以透過 `python app.py --csv <in.csv> --excel <out.xlsx>` 完整執行。
