import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter import font

class NameSearchApp:
    def __init__(self, root, names_filepath):
        self.root = root
        root.title("🔍 姓名搜尋器 (Name Searcher)")
        root.geometry("500x600")
        root.minsize(450, 500)
        
        # 設定主題顏色
        self.colors = {
            'primary': '#2E86AB',      # 藍色
            'secondary': '#A23B72',    # 紫紅色
            'accent': '#F18F01',       # 橙色
            'background': '#F5F5F5',   # 淺灰色
            'surface': '#FFFFFF',      # 白色
            'text': '#2C3E50',         # 深灰色
            'success': '#27AE60',      # 綠色
            'warning': '#F39C12'       # 黃色
        }
        
        # 設定視窗背景色
        root.configure(bg=self.colors['background'])
        
        # 設定字體
        self.fonts = {
            'title': font.Font(family="Microsoft JhengHei", size=16, weight="bold"),
            'heading': font.Font(family="Microsoft JhengHei", size=12, weight="bold"),
            'body': font.Font(family="Microsoft JhengHei", size=10),
            'button': font.Font(family="Microsoft JhengHei", size=10, weight="bold")
        }
        
        # 設定樣式
        self.setup_styles()
        
        self.names_filepath = names_filepath
        self.names_list = self.load_names(self.names_filepath)
        
        # 建立主要容器
        self.create_widgets()
        
        # 將焦點設定在搜尋框
        self.search_entry.focus()

    def setup_styles(self):
        """設定 ttk 樣式"""
        style = ttk.Style()
        
        # 設定標題標籤樣式
        style.configure('Title.TLabel', 
                       font=self.fonts['title'],
                       foreground=self.colors['primary'],
                       background=self.colors['background'])
        
        # 設定標題標籤樣式
        style.configure('Heading.TLabel', 
                       font=self.fonts['heading'],
                       foreground=self.colors['text'],
                       background=self.colors['background'])
        
        # 設定一般標籤樣式
        style.configure('Body.TLabel', 
                       font=self.fonts['body'],
                       foreground=self.colors['text'],
                       background=self.colors['background'])
        
        # 設定按鈕樣式
        style.configure('Search.TButton',
                       font=self.fonts['button'],
                       foreground='white',
                       background=self.colors['primary'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Search.TButton',
                 background=[('active', self.colors['secondary']),
                           ('pressed', self.colors['accent'])])
        
        # 設定輸入框樣式
        style.configure('Search.TEntry',
                       font=self.fonts['body'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=2,
                       relief='solid')
        
        # 設定框架樣式
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='raised',
                       borderwidth=1)

    def create_widgets(self):
        """建立所有 GUI 元件"""
        # 主標題
        title_frame = ttk.Frame(self.root)
        title_frame.configure(style='TFrame')
        title_frame.pack(pady=(20, 10), padx=20, fill=tk.X)
        
        title_label = ttk.Label(title_frame, 
                               text="🔍 姓名搜尋系統", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="輸入關鍵字即時搜尋姓名", 
                                  style='Body.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # 搜尋區域
        search_card = ttk.Frame(self.root, style='Card.TFrame')
        search_card.pack(pady=10, padx=20, fill=tk.X, ipady=15)
        
        # 搜尋提示標籤
        self.search_prompt_label = ttk.Label(search_card, 
                                           text="🔎 請輸入姓名關鍵字：", 
                                           style='Heading.TLabel')
        self.search_prompt_label.pack(pady=(10, 5))

        # 搜尋輸入框和按鈕的框架
        search_frame = ttk.Frame(search_card)
        search_frame.pack(pady=10, padx=20)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, 
                                    textvariable=self.search_var, 
                                    width=35,
                                    style='Search.TEntry',
                                    font=self.fonts['body'])
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        # 綁定事件
        self.search_entry.bind("<KeyRelease>", self.perform_search_on_event)
        self.search_entry.bind("<Return>", self.perform_search_on_event)

        # 搜尋按鈕
        self.search_button = ttk.Button(search_frame, 
                                      text="🔍 搜尋", 
                                      command=self.perform_search_from_button,
                                      style='Search.TButton')
        self.search_button.pack(side=tk.LEFT, ipady=5, ipadx=10)
        
        # 狀態標籤
        self.status_label = ttk.Label(search_card, 
                                    text=f"📊 資料庫共有 {len(self.names_list)} 筆姓名資料", 
                                    style='Body.TLabel')
        self.status_label.pack(pady=(5, 10))

        # 結果區域
        results_card = ttk.Frame(self.root, style='Card.TFrame')
        results_card.pack(pady=10, padx=20, fill=tk.BOTH, expand=True, ipady=10)
        
        # 搜尋結果標籤
        self.results_label = ttk.Label(results_card, 
                                     text="📋 搜尋結果：", 
                                     style='Heading.TLabel')
        self.results_label.pack(pady=(10, 5), padx=20, anchor='w')

        # 搜尋結果列表框框架
        self.results_listbox_frame = ttk.Frame(results_card)
        self.results_listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # 列表框樣式設定
        self.results_listbox = tk.Listbox(self.results_listbox_frame, 
                                        width=50, 
                                        height=15,
                                        font=self.fonts['body'],
                                        bg=self.colors['surface'],
                                        fg=self.colors['text'],
                                        selectbackground=self.colors['primary'],
                                        selectforeground='white',
                                        borderwidth=1,
                                        relief='solid',
                                        highlightthickness=0)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 垂直捲軸
        self.scrollbar_y = ttk.Scrollbar(self.results_listbox_frame, 
                                       orient=tk.VERTICAL, 
                                       command=self.results_listbox.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox.config(yscrollcommand=self.scrollbar_y.set)

        # 水平捲軸
        self.scrollbar_x = ttk.Scrollbar(results_card, 
                                       orient=tk.HORIZONTAL, 
                                       command=self.results_listbox.xview)
        self.scrollbar_x.pack(fill=tk.X, padx=20, side=tk.BOTTOM)
        self.results_listbox.config(xscrollcommand=self.scrollbar_x.set)
        
        # 底部資訊
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        info_label = ttk.Label(info_frame, 
                              text="💡 提示：輸入關鍵字後會即時顯示搜尋結果", 
                              style='Body.TLabel')
        info_label.pack()

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

    def populate_listbox_with_names(self, names_to_display, search_was_active=False, search_term=""):
        """
        用指定的姓名列表填充列表框。
        :param names_to_display: 要顯示的姓名列表。
        :param search_was_active: 布林值，指示此調用是否為實際搜尋操作的結果。
        :param search_term: 搜尋關鍵字，用於顯示狀態。
        """
        self.results_listbox.delete(0, tk.END)  # 清空現有內容
        
        if names_to_display:
            for i, name in enumerate(names_to_display, 1):
                self.results_listbox.insert(tk.END, f"{i:3d}. {name}")
            # 更新結果標籤
            self.results_label.config(text=f"📋 搜尋結果：找到 {len(names_to_display)} 筆符合「{search_term}」的資料")
        elif search_was_active:
            self.results_listbox.insert(tk.END, "❌ 找不到符合條件的姓名")
            self.results_listbox.insert(tk.END, "💡 請嘗試其他關鍵字")
            # 更新結果標籤
            self.results_label.config(text=f"📋 搜尋結果：「{search_term}」無符合資料")
        else:
            # 初始狀態或清空搜尋框
            self.results_label.config(text="📋 搜尋結果：")

    def _execute_search(self, search_term):
        """核心搜尋邏輯並更新列表框。"""
        if not search_term:
            # 如果搜尋詞為空，則清空列表框並重置狀態
            self.results_listbox.delete(0, tk.END)
            self.results_label.config(text="📋 搜尋結果：")
            self.update_search_status("")
            return

        # 更新搜尋狀態
        self.update_search_status(f"正在搜尋「{search_term}」...")
        
        # 執行搜尋
        found_names = [name for name in self.names_list if search_term in name]
        
        # 更新結果
        self.populate_listbox_with_names(found_names, search_was_active=True, search_term=search_term)
        
        # 更新搜尋狀態
        if found_names:
            self.update_search_status(f"✅ 搜尋完成，找到 {len(found_names)} 筆資料")
        else:
            self.update_search_status(f"❌ 未找到符合「{search_term}」的資料")

    def update_search_status(self, message):
        """更新搜尋狀態顯示"""
        if message:
            self.status_label.config(text=f"🔍 {message}")
        else:
            self.status_label.config(text=f"📊 資料庫共有 {len(self.names_list)} 筆姓名資料")

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
