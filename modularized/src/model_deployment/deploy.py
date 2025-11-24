# Este módulo puede ser implementado con Flask o FastAPI, por ejemplo.
# Por ahora, solo guardamos el modelo (ya lo hacemos en train.py) y podríamos cargarlo.

def load_model(file_path):
    return joblib.load(file_path)