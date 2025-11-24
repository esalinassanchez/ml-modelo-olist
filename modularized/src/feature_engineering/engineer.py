def create_date_features(df, date_column):
    """
    Crea características a partir de una columna de fecha.
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df[f'{date_column}_year'] = df[date_column].dt.year
    df[f'{date_column}_month'] = df[date_column].dt.month
    df[f'{date_column}_day'] = df[date_column].dt.day
    df[f'{date_column}_dayofweek'] = df[date_column].dt.dayofweek
    return df

# Aquí se pueden agregar más funciones de feature engineering