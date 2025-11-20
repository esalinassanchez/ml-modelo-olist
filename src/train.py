import argparse
import yaml
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from .data import load_raw, validate_schema
from .preprocess import preprocess_train
from .features import create_features
from .model import ModelWrapper
from .utils import set_seed


def run_train(config_path: str):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    data_path = cfg['data']['raw_path']
    target = cfg['data'].get('target','delivery_time_days')
    out_dir = Path(cfg.get('artifacts',{}).get('models_dir','./artifacts/models'))
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_raw(data_path)
    validate_schema(df)
    set_seed(cfg['training'].get('seed',0))
    df = preprocess_train(df)
    df = create_features(df)

    # filter rows with target
    df = df[df[target].notna()]
    X = df.select_dtypes(include=[np.number]).drop(columns=[target], errors='ignore').fillna(0)
    y = df[target]

    if X.shape[0] < 10:
        raise RuntimeError('Not enough rows after filtering target')

    # simple time-aware split: use train_test_split as fallback
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=cfg['training'].get('test_size',0.2), random_state=cfg['training'].get('seed',0))

    # train LightGBM if available otherwise RandomForest
    model_path = out_dir / 'model.joblib'
    try:
        import lightgbm as lgb
        params = cfg['training'].get('lgbm', {})
        lgbm = lgb.LGBMRegressor(**params)
        lgbm.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=cfg['training'].get('early_stopping_rounds',50), verbose=False)
        wrapper = ModelWrapper(model=lgbm, preproc=None)
    except Exception as e:
        print('LightGBM not available or failed, falling back to sklearn RF:', e)
        from sklearn.ensemble import RandomForestRegressor
        rf = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=cfg['training'].get('seed',0))
        rf.fit(X_train, y_train)
        wrapper = ModelWrapper(model=rf, preproc=None)

    preds = wrapper.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    print('Validation MAE:', mae)
    wrapper.save(str(model_path))
    print('Model saved to', model_path)
    return {'mae': mae, 'model_path': str(model_path)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    run_train(args.config)
