import tkinter as tk
from tkinter import ttk, messagebox
import tools

def calculate_bmi_and_display():
    try:
        height_str = height_entry.get()
        weight_str = weight_entry.get()

        if not height_str or not weight_str:
            messagebox.showwarning("輸入錯誤", "請輸入身高和體重")
            return

        height = int(height_str)
        weight = int(weight_str)

        if height <= 0 or weight <= 0:
            messagebox.showwarning("輸入錯誤", "身高和體重必須是正數")
            return

        bmi = tools.caculate_bmi(height, weight)
        state = tools.get_state(bmi)

        result_label.config(text=f"您的 BMI 值為: {bmi:.2f}")
        state_label.config(text=f"健康狀態: {state}")

        if state == "正常範圍":
            result_label.config(foreground="black")
            state_label.config(foreground="black")
        else:
            result_label.config(foreground="red")
            state_label.config(foreground="red")

    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的數字身高和體重")
    except Exception as e:
        messagebox.showerror("發生錯誤", f"計算過程中發生錯誤: {e}")

# 建立主視窗
root = tk.Tk()
root.title("BMI 計算器")
root.geometry("450x350") # 設定視窗大小

# 設定樣式
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14)) # 字體加大
style.configure("TButton", font=("Arial", 14)) # 字體加大
style.configure("TEntry", font=("Arial", 14)) # 字體加大

# 建立主框架
main_frame = ttk.Frame(root, padding="30 30 30 30") # 增加 padding
main_frame.pack(expand=True, fill=tk.BOTH)

# 身高輸入
height_label = ttk.Label(main_frame, text="請輸入身高 (cm):")
height_label.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
height_entry = ttk.Entry(main_frame, width=15)
height_entry.grid(row=0, column=1, padx=5, pady=10)

# 體重輸入
weight_label = ttk.Label(main_frame, text="請輸入體重 (kg):")
weight_label.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
weight_entry = ttk.Entry(main_frame, width=15)
weight_entry.grid(row=1, column=1, padx=5, pady=10)

# 計算按鈕
calculate_button = ttk.Button(main_frame, text="計算 BMI", command=calculate_bmi_and_display)
calculate_button.grid(row=2, column=0, columnspan=2, pady=15)

# 結果顯示
result_label = ttk.Label(main_frame, text="您的 BMI 值為: ")
result_label.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

state_label = ttk.Label(main_frame, text="健康狀態: ")
state_label.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)

# 讓元件在視窗縮放時能自動調整
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(3, weight=1)
main_frame.rowconfigure(4, weight=1)


if __name__ == '__main__':
    root.mainloop()
