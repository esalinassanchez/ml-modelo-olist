import pandas as pd
import os

class Extract():
    path = None
    def __init__(self, path: str):
        self.path = path

    def load_data(self, file_name):
        """
        Carga un archivo CSV desde la ruta especificada.
        """
        file_path = os.path.join(self.path, file_name)
        return pd.read_csv(file_path)

    def load_multiple_files(self, file_list):
        """
        Carga múltiples archivos CSV y devuelve un diccionario de DataFrames.
        """
        data = {}
        for file in file_list:
            name = file.replace('.csv', '')
            data[name] = self.load_data(file)
        return data