class DataValidation():
  df = None
  def __init__(self, df):
    self.df = df
    pass

  def set_date_to_date_type(self):
    fecha_cols = [
      'order_purchase_timestamp',
      'order_approved_at',
      'order_delivered_carrier_date',
      'order_delivered_customer_date',
      'order_estimated_delivery_date',
      'shipping_limit_date'
    ]

    for col in fecha_cols:
        self.df[col] = self.df.to_datetime(self.df[col])
    return self.df

  def check_missing_data(self, df, columns=None):
    """
    Verifica valores nulos en el DataFrame.
    Si se proporciona una lista de columnas, solo verifica esas columnas.
    """
    if columns is None:
        columns = df.columns
    missing = df[columns].isnull().sum()
    return missing[missing > 0]

  def check_data_types(self, df, expected_dtypes):
    """
    Verifica que los tipos de datos coincidan con los esperados.
    expected_dtypes: diccionario {columna: tipo}
    """
    errors = []
    for col, expected_type in expected_dtypes.items():
        if col in df.columns:
            if not df[col].dtype == expected_type:
                errors.append(f"Columna {col}: esperaba {expected_type}, obtuvo {df[col].dtype}")
        else:
            errors.append(f"Columna {col} no encontrada")
    return errors