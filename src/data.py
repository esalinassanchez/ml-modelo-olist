import pandas as pd


class Data():
    path = None
    df = None
    def __init__(self,path: str):
        self.path = path
    def load_raw(self) -> pd.DataFrame:
        self.df = pd.read_csv(self.path)

    def load_data_from_database(self) -> pd.DataFrame:
        pass
        return None

    def validate_schema(self, df: pd.DataFrame) -> bool:
        required = ['order_purchase_timestamp', 'order_delivered_customer_date']
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f'Missing required columns: {missing}')
        return True

    def sample_quick(self, df: pd.DataFrame, frac: float = 0.1) -> pd.DataFrame:
        return df.sample(frac=frac, random_state=0)
