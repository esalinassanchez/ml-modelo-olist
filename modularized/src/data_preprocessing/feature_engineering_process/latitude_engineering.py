import pandas as pd
import numpy as np
import re

class LatitudeEngineering():
    df = None
    def __init__(self, df):
        self.df = df

    def _normalize_col(self, name):
        s = name.lower()
        # quitar palabras lat/lon/latitude/longitude/lng/long
        s = re.sub(r'latitude|longitude|long|lng|lat|lon', '', s)
        s = re.sub(r'[^a-z0-9_]', '', s)
        s = s.strip('_')
        return s
    
    def haversine_series(self, lat1, lon1, lat2, lon2):
        # espera series pandas o arrays; devuelve distancia en km
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
    
    def get_latitude_longitude_columns(self, cols):
        
        lat_candidates = [c for c in cols if 'lat' in c.lower() or 'latitude' in c.lower()]
        lon_candidates = [c for c in cols if any(k in c.lower() for k in ['lon','lng','long','longitude'])]
        return lat_candidates, lon_candidates
    
    def calculate_distance_between_consumer_seller(self):
        pairs = []
        cols = list(self.df.columns)
        lat_candidates, lon_candidates = self.get_latitude_longitude_columns(cols)
        for lat in lat_candidates:
            for lon in lon_candidates:
                if self._normalize_col(lat) == self._normalize_col(lon):
                    pairs.append((lat, lon))

        if not pairs and len(lat_candidates) == 1 and len(lon_candidates) == 1:
            pairs = [(lat_candidates[0], lon_candidates[0])]

        if not pairs and lat_candidates and lon_candidates:
            for lat in lat_candidates:
                lat_pref = lat.split('_')[:-1]
                for lon in lon_candidates:
                    lon_pref = lon.split('_')[:-1]
                    if lat_pref and lon_pref and lat_pref == lon_pref:
                        pairs.append((lat, lon))

        distance_cols = []
        for lat_col, lon_col in pairs:
            # Intentar convertir a numérico y manejar nulos
            lat_series = pd.to_numeric(self.df[lat_col], errors='coerce')
            lon_series = pd.to_numeric(self.df[lon_col], errors='coerce')
            # Buscar un posible compañero (por ejemplo seller vs customer). Nombrado por la normalización
            base = self._normalize_col(lat_col) or 'pair'
            dist_name = f'distance_{base}_km'
            self.df[dist_name] = haversine_series(lat_series, lon_series, lat_series, lon_series) if False else None
            # La línea anterior es un placeholder. Queremos la distancia entre dos puntos diferentes;
            # si los pares representan buyer/seller deben estar en columnas distintas.
            # Recalcular correctamente: asumimos que lat_col y lon_col son del mismo punto; por eso intentamos encontrar la pareja opuesta
            # Buscaremos por convención si el nombre contiene 'customer' y existe 'seller_lat'/'seller_lng' etc.
            # Intentar buscar pareja opuesta (buyer vs seller)
            alt_prefixes = ['seller', 'seller', 'seller', 'customer', 'buyer']
            # Buscar explícitamente columnas típicas
            candidate_pairs = []
            # Si normalización vacía, usar raw names
            # Construir búsqueda de pareja: reemplazar el fragmento lat/latitude por posible lon variants of other actor
            # En la mayoría de datasets hay columnas 'customer_lat','customer_lng' y 'seller_lat','seller_lng'
            # Si el par detectado viene de, por ejemplo, 'customer_lat'+'customer_lng', buscaremos 'seller_lat'+'seller_lng'
            norm = self._normalize_col(lat_col)
            if 'customer' in lat_col.lower() or 'buyer' in lat_col.lower():
                # proponer seller como pareja
                for s in ['seller', 'seller_lat', 'seller_lng', 'seller_long', 'seller_longitude']:
                    pass
            # Búsqueda práctica: si existen columnas 'seller_lat' y 'seller_lng' usarlas
            found = False
            possible_lat_names = [n for n in cols if re.search(r'seller.*lat|.*seller.*latitude', n.lower())] or [n for n in cols if re.search(r'seller', n.lower()) and 'lat' in n.lower()]
            possible_lon_names = [n for n in cols if re.search(r'seller.*(lon|lng|long|longitude)', n.lower())] or [n for n in cols if re.search(r'seller', n.lower()) and any(k in n.lower() for k in ['lon','lng','long'])]
            if possible_lat_names and possible_lon_names:
                # usar la primera pareja seller encontrada
                other_lat = possible_lat_names[0]
                other_lon = possible_lon_names[0]
                try:
                    lat1 = pd.to_numeric(self.df[lat_col], errors='coerce')
                    lon1 = pd.to_numeric(self.df[lon_col], errors='coerce')
                    lat2 = pd.to_numeric(self.df[other_lat], errors='coerce')
                    lon2 = pd.to_numeric(self.df[other_lon], errors='coerce')
                    self.df[f'distance_{self._normalize_col(lat_col)}_to_{self._normalize_col(other_lat)}_km'] = self.haversine_series(lat1, lon1, lat2, lon2)
                    distance_cols.append(f'distance_{self._normalize_col(lat_col)}_to_{self._normalize_col(other_lat)}_km')
                    found = True
                except Exception as e:
                    print('Error calculando distancia para', lat_col, other_lat, e)
            if not found:
                # Si no se encontró pareja opuesta, calcular distancia entre lat/lon de la misma fila no tiene sentido (0), así que omitimos
                print(f'No se encontró pareja opuesta para {lat_col}/{lon_col}; omitido')

        print('Columnas de distancia creadas (si las hay):', distance_cols)
        if distance_cols:
            # display(self.df[distance_cols].head())
            print(self.df[distance_cols].describe())
        return self.df