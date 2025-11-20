import argparse
import yaml
import pandas as pd
from pathlib import Path
from .model import ModelWrapper
from .data import load_raw


def run_predict(config_path: str, input_path: str, output_path: str):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    model_path = cfg.get('artifacts',{}).get('models_dir','./artifacts/models')
    model_file = Path(model_path) / 'model.joblib'
    m = ModelWrapper.load(str(model_file))
    df = load_raw(input_path)
    # minimal preprocessing - user should adapt
    X = df.select_dtypes(include=['number']).fillna(0)
    preds = m.predict(X)
    out = df.copy()
    out['pred_delivery_days'] = preds
    out.to_csv(output_path, index=False)
    print('Predictions saved to', output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    run_predict(args.config, args.input, args.output)
