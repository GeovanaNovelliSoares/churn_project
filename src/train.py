import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def run_train():
    try:
        df = pd.read_csv('data/processed_data.csv')
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'data/processed_data.csv' não foi encontrado.")
        print("Execute primeiro: python src/data_ingestion.py")
        return

    mlflow.set_experiment("Churn_Prediction_Senior")
    
    with mlflow.start_run():
        X = df.drop(['churn', 'user_id'], axis=1)
        y = df['churn']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        numeric_features = ['tenure', 'monthly_charges', 'total_charges', 'ltv_ratio']
        categorical_features = ['contract_type']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])

        model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
        ])

        model_pipeline.fit(X_train, y_train)
        
        acc = model_pipeline.score(X_test, y_test)
        mlflow.log_metric("accuracy", acc)
        
        mlflow.sklearn.log_model(model_pipeline, "churn_model_pipeline")
        
        print(f"Treino finalizado!")
        print(f"Acurácia: {acc:.4f}")
        print(f"Modelo salvo no MLflow.")

if __name__ == "__main__":
    run_train()