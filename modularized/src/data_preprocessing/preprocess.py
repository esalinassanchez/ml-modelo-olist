import pandas as pd
class Preprocess():
    df = None
    def _init__(self, df):
        self.df = df
    def convert_to_datetime(self, columns):
        """
        Convierte columnas a datetime.
        """
        for col in columns:
            self.df[col] = pd.to_datetime(self.df[col])
        return self.df

    def handle_missing_values(self, strategy='drop', columns=None, fill_value=None):
        """
        Maneja valores missing.
        Estrategias: 'drop', 'fill'
        """
        if columns is None:
            columns = self.df.columns
        if strategy == 'drop':
            self.df = self.df.dropna(subset=columns)
        elif strategy == 'fill':
            self.df[columns] = self.df[columns].fillna(fill_value)
        return self.df