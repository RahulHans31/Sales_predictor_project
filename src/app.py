from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.components.database import add_sales_data, fetch_all_sales_data, fetch_sales_data_by_id, modify_sales_data, remove_sales_data , predict_sales_data , add_prediction_data , fetch_prediction_data , fetch_prediction_data_by_id , add_prediction_data_by_id , train_ml_model , predict_sales_and_add

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Prediction API!"}

# Pydantic model to validate input data for sales data
class SalesData(BaseModel):
    name: str
    store_revenue: float
    store_size: str
    temp: str
    variety_score: int
    quality_range: int
    shop_area: float
    city_tier: int
    availability: str
    discounts: int
    weekday_sales: float
    weekend_sales: float
    total_sales: float
    location: str
    
class PredictionData(BaseModel):
    id: int
    predicted_sales: float

@app.post("/sales/", status_code=201)
def create_sales(sales_data: SalesData):
    try:
        add_sales_data(
            sales_data.name, sales_data.store_revenue, sales_data.store_size, sales_data.temp,
            sales_data.variety_score, sales_data.quality_range, sales_data.shop_area, sales_data.city_tier,
            sales_data.availability, sales_data.discounts, sales_data.weekday_sales, sales_data.weekend_sales,
            sales_data.total_sales, sales_data.location
        )
        return {"message": "Sales data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding sales data: {e}")

@app.get("/sales/", response_model=List[SalesData])
def get_all_sales():
    try:
        sales = fetch_all_sales_data()
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales data: {e}")

@app.get("/sales/{sales_id}", response_model=SalesData)
def get_sales(sales_id: int):
    try:
        sales = fetch_sales_data_by_id(sales_id)
        if sales:
            return sales
        else:
            raise HTTPException(status_code=404, detail="Sales data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales data: {e}")

@app.put("/sales/{sales_id}", status_code=200)
def update_sales(sales_id: int, sales_data: SalesData):
    try:
        modify_sales_data(
            sales_id, sales_data.name, sales_data.store_revenue, sales_data.store_size, sales_data.temp,
            sales_data.variety_score, sales_data.quality_range, sales_data.shop_area, sales_data.city_tier,
            sales_data.availability, sales_data.discounts, sales_data.weekday_sales, sales_data.weekend_sales,
            sales_data.total_sales, sales_data.location
        )
        return {"message": "Sales data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating sales data: {e}")

@app.delete("/sales/{sales_id}", status_code=200)
def delete_sales(sales_id: int):
    try:
        remove_sales_data(sales_id)
        return {"message": "Sales data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sales data: {e}")
    
@app.get("/predict/" , response_model=List[PredictionData])
def get_prediction_data():
    try:
        prediction = fetch_prediction_data()
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prediction data: {e}")
    
@app.get("/predict/{sales_id}" , response_model=PredictionData)
def get_prediction_data_by_id(sales_id: int):
    try:
        prediction = fetch_prediction_data_by_id(sales_id)
        if prediction:
            return prediction
        else:
            raise HTTPException(status_code=404, detail="Prediction data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prediction data: {e}")   
    
@app.post("/predict/" , status_code=201)
def create_prediction_data():
    try:
        add_prediction_data()
        return {"message": "Prediction data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding prediction data: {e}")
    
@app.post("/predict/{sales_id}" , status_code=201)
def update_prediction_data(sales_id: int):
    try:
        add_prediction_data_by_id(sales_id)
        return {"message": "Prediction data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding prediction data: {e}")
    

@app.post('/train/' , status_code=200)
def train_model_route():
    try:
        train_ml_model()
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model 1 : {e}")
    
@app.post("/predict_and_add/", status_code=201)
def create_sales(sales_data: SalesData):
    try:
        predicted_sales = predict_sales_and_add(
            sales_data
        )
        return {"message": "Sales data added successfully" , "predicted_sales": predicted_sales[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding sales data: {e}")