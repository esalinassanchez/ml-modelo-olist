import pandas as pd
from src.features import extract_date_parts, product_volume_density


def test_extract_date_parts():
    df = pd.DataFrame({'order_purchase_timestamp': ['2020-01-01 10:00:00','2020-02-05 15:30:00']})
    out = extract_date_parts(df, 'order_purchase_timestamp')
    assert 'order_purchase_timestamp_day' in out.columns
    assert out['order_purchase_timestamp_day'].iloc[0] == 1


def test_product_volume_density():
    df = pd.DataFrame({'product_weight_g':[1000],'product_length_cm':[10],'product_height_cm':[5],'product_width_cm':[2]})
    out = product_volume_density(df)
    assert 'product_volume_cm3' in out.columns
    assert out['product_volume_cm3'].iloc[0] == 10*5*2
