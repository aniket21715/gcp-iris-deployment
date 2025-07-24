from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import numpy as np

app = FastAPI(title="Iris Species Predictor API")
model = load("app/model.joblib")
iris_species = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Welcome! API is running."}

@app.post("/predict")
def predict_species(iris_input: IrisInput):
    input_data = np.array([[
        iris_input.sepal_length,
        iris_input.sepal_width,
        iris_input.petal_length,
        iris_input.petal_width
    ]])
    prediction_code = model.predict(input_data)[0]
    predicted_species = iris_species[prediction_code]
    return {
        "prediction_code": int(prediction_code),
        "predicted_species": predicted_species
    }