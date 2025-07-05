'''
主應用程式入口點，用於處理命令列參數和執行核心邏輯。
'''
import argparse
import pandas as pd

def read_csv_data(csv_path):
    """
    從指定的路徑讀取 CSV 資料。

    Args:
        csv_path (str): CSV 檔案的路徑。

    Returns:
        pandas.DataFrame: 讀取的資料，如果失敗則返回 None。
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"成功讀取 CSV 檔案: {csv_path}")
        return df
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {csv_path}")
        return None
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return None

def create_pivot_table(df):
    """
    根據提供的 DataFrame 建立樞紐分析表。

    Args:
        df (pandas.DataFrame): 輸入的 DataFrame。

    Returns:
        pandas.DataFrame: 建立的樞紐分析表，如果失敗則返回 None。
    """
    try:
        df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
        df['小費比例'] = df['小費'] / df['總票價']
        grouped = df.groupby(by=['吸煙者','日期'])
        functions = [('數量','count'),('平均','mean'),('最大值','max')]
        pivot = grouped[['小費','總票價']].agg(functions)
        print("成功建立樞紐分析表。")
        return pivot
    except Exception as e:
        print(f"建立樞紐分析表時發生錯誤：{e}")
        return None

def export_to_excel(df, excel_path):
    """
    將 DataFrame 匯出至指定的 Excel 檔案路徑。

    Args:
        df (pandas.DataFrame): 要匯出的 DataFrame。
        excel_path (str): 輸出的 Excel 檔案路徑。
    """
    try:
        df.to_excel(excel_path)
        print(f"成功將資料匯出至: {excel_path}")
    except Exception as e:
        print(f"匯出檔案時發生錯誤：{e}")

def main():
    """
    主函式，解析命令列參數並啟動應用程式。
    """
    parser = argparse.ArgumentParser(description="讀取 CSV，建立樞紐分析表，並匯出為 Excel。")
    parser.add_argument("--csv", required=True, help="輸入的 CSV 檔案路徑。")
    parser.add_argument("--excel", required=True, help="輸出的 Excel 檔案路徑。")
    
    args = parser.parse_args()
    
    df = read_csv_data(args.csv)
    
    if df is not None:
        pivot_table = create_pivot_table(df)
        if pivot_table is not None:
            export_to_excel(pivot_table, args.excel)

if __name__ == "__main__":
    main()
