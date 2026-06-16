from Schema.UserInput import UserDetail
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal, Annotated
from fastapi.responses import JSONResponse
from Model.predict import predict_data
from Schema.response import PredictionResponse



app = FastAPI()

#home page
@app.get('/')
def home():
    return {'message':'Customer Churn Prediction Api'}

@app.get('/health_check')
def health_check():
    return {
        'status_code':'Ok'
    }
@app.post('/predict',response_model=PredictionResponse)
def predict_customer(data:UserDetail):
    user_input={
        'CreditScore':data.CreditScore,
        'Geography':data.Geography,
        'Gender':data.Gender,
        'Age':data.Age,
        'Balance':data.Balance,
        'Tenure':data.Tenure,
        'NumOfProducts':data.NumOfProducts,
        'HasCrCard':data.HasCrCard,
        'IsActiveMember':data.IsActiveMember,
        'EstimatedSalary':data.EstimatedSalary
    }

    try:
        result=predict_data(user_input)
        return JSONResponse(status_code=200,content={'response':result})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))


