import joblib
import os

class ModelWrapper:
    def __init__(self, model=None, preproc=None):
        self.model = model
        self.preproc = preproc

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({'model': self.model, 'preproc': self.preproc}, path)

    @classmethod
    def load(cls, path: str):
        d = joblib.load(path)
        return cls(model=d.get('model'), preproc=d.get('preproc'))
