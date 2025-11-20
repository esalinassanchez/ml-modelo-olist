import pandas as pd
from src.preprocess import preprocess_train


def test_preprocess_train_dates():
    df = pd.DataFrame({'order_purchase_timestamp':['2020-01-01','not a date']})
    out = preprocess_train(df)
    assert 'order_purchase_timestamp' in out.columns
    assert pd.api.types.is_datetime64_any_dtype(out['order_purchase_timestamp'])
