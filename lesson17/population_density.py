import pandas as pd
from typing import Optional

class PopulationDensity:
    """
    處理各鄉鎮市區人口密度資料的類別。
    """
    def __init__(self, csv_path: str):
        """
        初始化，讀取指定路徑的 csv 檔案。
        :param csv_path: csv 檔案路徑
        """
        self.csv_path = csv_path
        self.data: Optional[pd.DataFrame] = None
        self.error_message: Optional[str] = None
        self.load_data()

    def load_data(self):
        """
        讀取 csv 檔案並存為 DataFrame，並處理欄位名稱、index 與刪除第一筆資料。
        若欄位數不符，將記錄錯誤訊息。
        """
        try:
            df = pd.read_csv(self.csv_path)
            expected_columns = ['鄉鎮市區', '人口數', '面積', '人口密度']
            # 自動移除多餘欄位（如序號或 index）
            if len(df.columns) > 4:
                df = df.iloc[:, -4:]
            if len(df.columns) == 4:
                df.columns = expected_columns
                df.set_index('鄉鎮市區', inplace=True)
                if len(df) > 0:
                    df = df.iloc[1:]
                self.data = df
                self.error_message = None
            else:
                self.data = None
                self.error_message = f"欄位數不符，檔案實際欄位數: {len(df.columns)}，預期: 4。請檢查 csv 檔案格式。"
        except Exception as e:
            self.data = None
            self.error_message = f"讀取失敗: {e}"

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """
        取得人口密度的 DataFrame。
        :return: DataFrame 或 None
        """
        return self.data

    def get_error(self) -> Optional[str]:
        """
        取得錯誤訊息。
        :return: str 或 None
        """
        return self.error_message

    def get_summary(self) -> Optional[pd.DataFrame]:
        """
        取得人口密度資料的簡易摘要（可擴充）。
        :return: DataFrame 或 None
        """
        if self.data is not None:
            return self.data.describe(include='all')
        return None
