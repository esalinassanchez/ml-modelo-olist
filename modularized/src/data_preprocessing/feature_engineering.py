import pandas as pd
from src.data_preprocessing.feature_engineering_process.latitude_engineering import LatitudeEngineering
from src.data_preprocessing.feature_engineering_process.product_engineering import ProductEngineering
from src.data_preprocessing.feature_engineering_process.target_variable import TargetVariable

class FeatureEngineering():
    df = None
    def __init__(self, df):
        self.df = df
    def split_date_into_day_month_year(self, columns):
        new_cols = []
        for col in columns:
            if col in self.df.columns:
                # Asegurarse que la columna sea datetime (si no, intentar convertir)
                if not pd.api.types.is_datetime64_any_dtype(self.df[col]):
                    try:
                        self.df[col] = pd.to_datetime(self.df[col])
                    except Exception:
                        # Si no se puede convertir, saltar esa columna
                        continue

                self.df[col + '_day'] = self.df[col].dt.day
                self.df[col + '_month'] = self.df[col].dt.month
                self.df[col + '_year'] = self.df[col].dt.year
                self.df[col + '_hour'] = self.df[col].dt.hour
                new_cols += [col + '_day', col + '_month', col + '_year', col + '_hour']

                print('Se añadieron columnas derivadas:', new_cols)
        return self.df
    
    def product_process(self):
        product_engineering = ProductEngineering(self.df)
        self.df = product_engineering.set_volume_density()
        return self.df
    def latitude_engineering(self):
        latitude_engineering = LatitudeEngineering(self.df)
        self.df = latitude_engineering.calculate_distance_between_consumer_seller()
        return self.df
    
    def target_variable(self):
        target_variable = TargetVariable(self.df)
        self.df = target_variable.set_target_variable()
        return self.df
    
    
    