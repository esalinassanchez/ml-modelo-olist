from src.data_extraction.extract import Extract
# from src.data_extraction.extract import load_multiple_files
from src.data_validation.validate import check_missing_data
from src.data_preprocessing.preprocess import convert_to_datetime, handle_missing_values
from src.feature_engineering.engineer import create_date_features
from src.model_training.train import split_data, train_model, save_model
from src.model_evaluation.evaluate import evaluate_model
from src.utils.config import DATA_PATH, MODEL_PATH

def main():
    # 1. Extracción de datos
    file_list = ['olist_orders_dataset.csv']  # listar todos los archivos necesarios
    extract = Extract('../dataset/')
    data = extract.load_multiple_files(file_list)
    print(df)

    
    # 2. Validación de datos
    for name, df in data.items():
        missing = check_missing_data(df)
        print(f"Missing data in {name}: {missing}")
    
    # # 3. Preprocesamiento
    # # Por ejemplo, en el dataset de órdenes, convertir las columnas de fecha.
    # orders = data['olist_orders_dataset']
    # orders = convert_to_datetime(orders, ['order_purchase_timestamp', 'order_approved_at', 
    #                                       'order_delivered_carrier_date', 'order_delivered_customer_date', 
    #                                       'order_estimated_delivery_date'])
    
    # # 4. Ingeniería de características
    # # Crear variable objetivo: tiempo de entrega en días (diferencia entre delivered y purchase)
    # orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    
    # # Crear características de fecha
    # orders = create_date_features(orders, 'order_purchase_timestamp')
    
    # # 5. Entrenamiento del modelo
    # # Seleccionar características y variable objetivo
    # features = ['order_purchase_timestamp_year', 'order_purchase_timestamp_month', 
    #             'order_purchase_timestamp_day', 'order_purchase_timestamp_dayofweek']
    # X = orders[features]
    # y = orders['delivery_time']
    
    # # Eliminar filas con delivery_time missing (entregas no completadas)
    # X = X[~y.isnull()]
    # y = y[~y.isnull()]
    
    # X_train, X_test, y_train, y_test = split_data(X, y)
    
    # model = train_model(X_train, y_train, model_type='random_forest')
    
    # # 6. Evaluación
    # metrics = evaluate_model(model, X_test, y_test)
    # print(metrics)
    
    # # 7. Guardar modelo
    # save_model(model, f"{MODEL_PATH}/delivery_time_model.pkl")

if __name__ == '__main__':
    main()