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

- [x] 請在右側欄位（column）中，根據左側欄位使用者所選的股票名稱和時間區間，繪製折線圖。
    - 折線圖需顯示所有被選取的股票，每一條線對應一個股票名稱。
    - 時間區間需根據使用者在左側所選的「開始時間」和「結束時間」進行資料篩選。

- [x] 請將版面修改為單欄（只使用一個 column），將圖表顯示在頁面最下方。
    - 請調整折線圖的 y 軸範圍，使其不會過長（可自動縮放或設定適當的最大/最小值，讓圖表更容易閱讀）。

- [x] 錯誤解決:
```
TypeError: no numeric data to plot

File "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson16/app.py", line 97, in <module>
    filtered_df.plot(ax=ax)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/plotting/_core.py", line 1030, in __call__
    return plot_backend.plot(data, kind=kind, **kwargs)
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/plotting/_matplotlib/__init__.py", line 71, in plot
    plot_obj.generate()
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/plotting/_matplotlib/core.py", line 499, in generate
    self._compute_plot_data()
File "/opt/miniconda3/envs/chihlee/lib/python3.10/site-packages/pandas/plotting/_matplotlib/core.py", line 698, in _compute_plot_data
    raise TypeError("no numeric data to plot")
```

- [x] 由於使用 matplotlib 圖片無法良好展示，請改用 Streamlit 內建的圖表元件（如 st.line_chart）來顯示折線圖。
    - 每一檔股票請分開顯示一張獨立的圖表。
    - 圖表需根據使用者所選的股票動態產生（有幾檔就顯示幾張）。
    - 圖表的 y 軸刻度（tick label）請只顯示整數，不要有小數點。

- [x] app.py有程式碼結構的錯誤,請修改

