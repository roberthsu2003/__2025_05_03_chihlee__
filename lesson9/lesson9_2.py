import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class NameSearchApp:
    def __init__(self, root, names_filepath):
        self.root = root
        root.title("姓名搜尋器 (Name Searcher)")
        root.geometry("400x450") # 設定視窗初始大小

        self.names_filepath = names_filepath
        self.names_list = self.load_names(self.names_filepath)

        # --- GUI 元素 ---

        # 搜尋提示標籤
        self.search_prompt_label = ttk.Label(root, text="請輸入姓名關鍵字進行搜尋：")
        self.search_prompt_label.pack(pady=(10, 5))

        # 搜尋輸入框和按鈕的框架
        search_frame = ttk.Frame(root)
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        # 綁定事件，當使用者在輸入框中釋放按鍵時，執行搜尋
        self.search_entry.bind("<KeyRelease>", self.perform_search_on_event)

        # 搜尋按鈕
        self.search_button = ttk.Button(search_frame, text="搜尋", command=self.perform_search_from_button)
        self.search_button.pack(side=tk.LEFT)


        # 搜尋結果標籤
        self.results_label = ttk.Label(root, text="搜尋結果：")
        self.results_label.pack(pady=(10, 5))

        # 搜尋結果列表框
        self.results_listbox_frame = ttk.Frame(root)
        self.results_listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.results_listbox = tk.Listbox(self.results_listbox_frame, width=50, height=15)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 垂直捲軸
        self.scrollbar_y = ttk.Scrollbar(self.results_listbox_frame, orient=tk.VERTICAL, command=self.results_listbox.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox.config(yscrollcommand=self.scrollbar_y.set)

        # 水平捲軸 (如果名字可能很長)
        self.scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.results_listbox.xview)
        self.scrollbar_x.pack(fill=tk.X, padx=10, side=tk.BOTTOM)
        self.results_listbox.config(xscrollcommand=self.scrollbar_x.set)


        # 初始不載入任何名字到列表框
        # self.populate_listbox_with_names(self.names_list) # <--- 移除此行

        # 將焦點設定在搜尋框
        self.search_entry.focus()

    def load_names(self, filepath):
        """從指定的檔案路徑載入姓名列表。"""
        if not os.path.exists(filepath):
            messagebox.showerror("錯誤", f"找不到檔案：{filepath}\n請確認 'names.txt' 存在於正確的路徑。")
            self.root.quit() # 如果檔案不存在，可能直接關閉應用程式或處理
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                # 讀取每一行，去除前後空白(包括換行符)，並過濾掉空行
                names = [name.strip() for name in f.readlines() if name.strip()]
            return names
        except Exception as e:
            messagebox.showerror("讀取錯誤", f"讀取檔案時發生錯誤：{e}")
            return []

    def populate_listbox_with_names(self, names_to_display, search_was_active=False):
        """
        用指定的姓名列表填充列表框。
        :param names_to_display: 要顯示的姓名列表。
        :param search_was_active: 布林值，指示此調用是否為實際搜尋操作的結果。
        """
        self.results_listbox.delete(0, tk.END)  # 清空現有內容
        if names_to_display:
            for name in names_to_display:
                self.results_listbox.insert(tk.END, name)
        elif search_was_active: # 只有在進行了搜尋且沒有結果時顯示 "無此人"
            self.results_listbox.insert(tk.END, "無此人")
        # 如果 names_to_display 為空且 search_was_active 為 False (例如初始狀態或清空搜尋框)，列表框將保持空白

    def _execute_search(self, search_term):
        """核心搜尋邏輯並更新列表框。"""
        if not search_term:
            # 如果搜尋詞為空 (例如，使用者清空了輸入框)，則清空列表框
            self.results_listbox.delete(0, tk.END)
            return

        found_names = [name for name in self.names_list if search_term in name]
        # 因為 search_term 不為空，所以 search_was_active 應為 True
        self.populate_listbox_with_names(found_names, search_was_active=True)

    def perform_search_on_event(self, event=None):
        """當輸入框內容改變 (按鍵釋放) 時執行搜尋。"""
        search_term = self.search_var.get().strip()
        self._execute_search(search_term)

    def perform_search_from_button(self):
        """當點擊搜尋按鈕時執行搜尋。"""
        search_term = self.search_var.get().strip()
        self._execute_search(search_term)


if __name__ == "__main__":
    names_file_path = "/Users/roberthsu2003/Documents/GitHub/__2025_05_03_chihlee__/lesson9/names.txt"
    # 確保 names_file_path 是正確的
    if not os.path.exists(names_file_path):
        # 在主應用程式啟動前處理檔案不存在的情況
        root_temp = tk.Tk()
        root_temp.withdraw() # 隱藏臨時主視窗
        messagebox.showerror("啟動錯誤", f"找不到姓名檔案：{names_file_path}\n應用程式無法啟動。")
        root_temp.destroy()
    else:
        root = tk.Tk()
        app = NameSearchApp(root, names_file_path)
        root.mainloop()
