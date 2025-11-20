import pandas as pd
from typing import Tuple


def load_raw(path: str) -> pd.DataFrame:
    """Carga el csv y devuelve un DataFrame sin procesar"""
    df = pd.read_csv(path)
    return df


def validate_schema(df: pd.DataFrame) -> bool:
    required = ['order_purchase_timestamp', 'order_delivered_customer_date']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    return True


def sample_quick(df: pd.DataFrame, frac: float = 0.1) -> pd.DataFrame:
    return df.sample(frac=frac, random_state=0)
