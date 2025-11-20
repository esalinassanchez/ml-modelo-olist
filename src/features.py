import pandas as pd
import numpy as np


def extract_date_parts(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = df.copy()
    if col not in df.columns:
        return df
    df[col] = pd.to_datetime(df[col], errors='coerce')
    df[f'{col}_day'] = df[col].dt.day
    df[f'{col}_month'] = df[col].dt.month
    df[f'{col}_year'] = df[col].dt.year
    df[f'{col}_hour'] = df[col].dt.hour
    return df


def product_volume_density(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    w_col = 'product_weight_g'
    l_col = 'product_length_cm'
    h_col = 'product_height_cm'
    wd_col = 'product_width_cm'
    if all(c in df.columns for c in [w_col,l_col,h_col,wd_col]):
        w = pd.to_numeric(df[w_col], errors='coerce')
        l = pd.to_numeric(df[l_col], errors='coerce')
        h = pd.to_numeric(df[h_col], errors='coerce')
        wd = pd.to_numeric(df[wd_col], errors='coerce')
        valid = (l>0)&(h>0)&(wd>0)
        df['product_volume_cm3'] = np.where(valid, l*h*wd, np.nan)
        df['product_volume_l'] = df['product_volume_cm3']/1000.0
        df['product_density_g_cm3'] = np.where(df['product_volume_cm3'].notna() & w.notna() & (df['product_volume_cm3']>0), w/df['product_volume_cm3'], np.nan)
        df['product_density_kg_m3'] = df['product_density_g_cm3']*1000.0
    return df


def haversine_series(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad = np.radians(lat1.astype(float))
    lon1_rad = np.radians(lon1.astype(float))
    lat2_rad = np.radians(lat2.astype(float))
    lon2_rad = np.radians(lon2.astype(float))
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat/2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # date parts
    for col in ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date','shipping_limit_date']:
        if col in df.columns:
            df = extract_date_parts(df, col)
    # product volume/density
    df = product_volume_density(df)
    return df
