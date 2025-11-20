import pandas as pd


def preprocess_train(df: pd.DataFrame) -> pd.DataFrame:
    """Basic preprocessing for training: parse dates, basic imputations."""
    df = df.copy()
    # parse dates
    date_cols = [c for c in ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date','shipping_limit_date'] if c in df.columns]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors='coerce')
    # basic imputations for numeric cols
    num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    # no aggressive imputations here; leave for feature functions
    return df


def preprocess_infer(df: pd.DataFrame, fitted_objects=None) -> pd.DataFrame:
    # same as train for now
    return preprocess_train(df)
