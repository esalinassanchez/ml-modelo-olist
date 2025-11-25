import pandas as pd

class TargetVariable():
    df = None
    def __init__(self, df):
        self.df = df
        pass
    def set_target_variable(self):
        if 'order_purchase_timestamp' in self.df.columns and 'order_delivered_customer_date' in self.df.columns:
            self.df['order_purchase_timestamp'] = pd.to_datetime(self.df['order_purchase_timestamp'], errors='coerce')
            self.df['order_delivered_customer_date'] = pd.to_datetime(self.df['order_delivered_customer_date'], errors='coerce')
            self.df['delivery_time_days'] = (self.df['order_delivered_customer_date'] - self.df['order_purchase_timestamp']).dt.total_seconds() / 86400.0
            if 'order_estimated_delivery_date' in self.df.columns:
                self.df['order_estimated_delivery_date'] = pd.to_datetime(self.df['order_estimated_delivery_date'], errors='coerce')
                self.df['delivery_delay_days'] = (self.df['order_delivered_customer_date'] - self.df['order_estimated_delivery_date']).dt.total_seconds() / 86400.0
            else:
                self.df['delivery_delay_days'] = pd.NA
            print('Target creado: delivery_time_days (y delivery_delay_days si hay fecha estimada)')
            # display(self.df['delivery_time_days'].describe())
        else:
            print('No se encuentran las columnas necesarias para calcular delivery_time_days: order_purchase_timestamp y/o order_delivered_customer_date')
        return self.df