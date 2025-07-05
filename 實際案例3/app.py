import argparse
import pandas as pd
import os


def parse_args():
    """解析命令列參數"""
    parser = argparse.ArgumentParser(description='CSV/Excel 樞紐表轉 Excel 工具')
    parser.add_argument('--csv', type=str, help='輸入的 CSV 或 Excel 檔案路徑', required=True)
    parser.add_argument('--excel', type=str, help='輸出的 Excel 檔案路徑', required=True)
    return parser.parse_args()


def read_input_file(file_path: str) -> pd.DataFrame:
    """根據副檔名自動讀取 CSV 或 Excel 檔案"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError('只支援 CSV 或 Excel 檔案作為輸入')
    return df


def process_csv_to_excel(input_path: str, excel_path: str):
    """讀取CSV/Excel，建立樞紐表，並輸出為Excel"""
    df = read_input_file(input_path)
    # 欄位命名需根據實際csv內容調整，這裡假設與tips.csv一致
    df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
    df['小費比例'] = df['小費'] / df['總票價']
    grouped = df.groupby(by=['吸煙者', '日期'])
    functions = [('數量', 'count'), ('平均', 'mean'), ('最大值', 'max')]
    pivot_df = grouped[['小費', '總票價']].agg(functions)
    pivot_df.to_excel(excel_path)
    print(f"已將樞紐表輸出至 {excel_path}")


def main():
    """主程式入口，處理 CSV/Excel 轉樞紐表並輸出 Excel"""
    args = parse_args()
    process_csv_to_excel(args.csv, args.excel)


if __name__ == '__main__':
    main()
