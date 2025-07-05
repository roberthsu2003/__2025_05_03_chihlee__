import pandas as pd

class PopulationDensity:
    """
    處理人口密度相關的數據處理和分析
    """
    def __init__(self, filepath:str):
        """
        初始化
        Args:
            filepath (str): csv檔案的路徑
        """
        self.filepath = filepath
        self.df = None

    def get_processed_data(self) -> pd.DataFrame:
        """
        讀取並處理csv檔案
        Returns:
            pd.DataFrame: 處理後的DataFrame
        """
        # 讀取CSV，使用第二行作為標頭，並僅選擇所需欄位
        self.df = pd.read_csv(
            self.filepath,
            encoding='utf-8',
            header=1,
            usecols=['區域別', '年底人口數', '土地面積', '人口密度']
        )
        # 重新命名欄位
        self.df.columns = ['鄉鎮市區', '人口數', '面積', '人口密度']
        
        # 刪除最後7列
        self.df = self.df.iloc[:-7]

        # 新增縣市欄位
        self.df['縣市'] = self.df['鄉鎮市區'].str[:3]

        # 更新鄉鎮市區欄位
        self.df['鄉鎮市區'] = self.df['鄉鎮市區'].str[3:]

        # 將 '縣市' 設為索引
        self.df.set_index('縣市', inplace=True)

        # 將None值替換為0
        self.df = self.df.fillna(0)

        # 轉換資料型態
        self.df['人口數'] = self.df['人口數'].astype(int)
        self.df['面積'] = self.df['面積'].astype(float)
        self.df['人口密度'] = self.df['人口密度'].astype(float)
        
        return self.df
