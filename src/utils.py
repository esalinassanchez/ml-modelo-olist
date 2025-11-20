import random
import numpy as np
import os


def set_seed(seed: int = 0):
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except Exception:
        pass


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True
)