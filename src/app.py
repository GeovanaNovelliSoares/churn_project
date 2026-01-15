from fastapi import FastAPI
import pandas as pd
import mlflow.pyfunc
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Churn Prediction Service")
model = None

RUN_ID = "9f62a1fdb22c4322b2fbecd4d3aa5b91"
MODEL_URI = f"runs:/{RUN_ID}/churn_model_pipeline"

print(f"🔄 Carregando modelo do Run ID: {RUN_ID}...")

try:
    model = mlflow.pyfunc.load_model(MODEL_URI)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"ERRO CRÍTICO AO CARREGAR O MODELO: {e}")

class CustomerData(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    ltv_ratio: float
    is_flexible: int

@app.get("/")
def home():
    return {"message": "API Online! Vá para /docs para testar."}

@app.post("/predict")
async def predict(data: CustomerData):
    if model is None:
        return {"error": "O modelo não está carregado no servidor.", "status": 500}
    
    try:
        input_df = pd.DataFrame([data.dict()])
        prediction = model.predict(input_df)
        
        return {
            "churn_prediction": int(prediction[0]),
            "status": "Success"
        }
    except Exception as e:
        return {"error": str(e), "status": "Error during prediction"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)