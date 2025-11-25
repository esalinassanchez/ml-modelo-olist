import numpy as np
import pandas as pd

class ProductEngineering():
    df = None
    def __init__(self, df):
        self.df = df
        self.w_col = 'product_weight_g'
        self.l_col = 'product_length_cm'
        self.h_col = 'product_height_cm'
        self.wd_col = 'product_width_cm'

    def set_volume_density(self):
        # Calcular volumen y densidad de los productos
        # Columnas usadas: product_weight_g, product_length_cm, product_height_cm, product_width_cm
        missing = [c for c in [self.w_col,self.l_col,self.h_col,self.wd_col] if c not in self.df.columns]
        if missing:
            print('Faltan columnas para volumen/densidad:', missing)
        else:
            # Convertir a numérico (coerce para convertir valores extraños a NaN)
            w = pd.to_numeric(self.df[self.w_col], errors='coerce')
            l = pd.to_numeric(self.df[self.l_col], errors='coerce')
            h = pd.to_numeric(self.df[self.h_col], errors='coerce')
            wd = pd.to_numeric(self.df[self.wd_col], errors='coerce')

            # Considerar dimensiones válidas solo si son > 0
            valid_dims = (l > 0) & (h > 0) & (wd > 0)

            # Volumen en cm^3 y en litros
            self.df['product_volume_cm3'] = np.where(valid_dims, (l * h * wd), np.nan)
            self.df['product_volume_l'] = self.df['product_volume_cm3'] / 1000.0

            # Densidad: g/cm^3 (y kg/m^3)
            self.df['product_density_g_cm3'] = np.where(self.df['product_volume_cm3'].notna() & w.notna() & (self.df['product_volume_cm3']>0), w / self.df['product_volume_cm3'], np.nan)
            self.df['product_density_kg_m3'] = self.df['product_density_g_cm3'] * 1000.0

            created = ['product_volume_cm3','product_volume_l','product_density_g_cm3','product_density_kg_m3']
            print('Columnas creadas:', created)
            # display(self.df[created].head())
            print('Estadísticas de volumen y densidad:')
            print(self.df[created].describe())
        return self.df