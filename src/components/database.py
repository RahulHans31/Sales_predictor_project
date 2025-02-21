from src.database.connection import Session
from src.database.crud import create_sales_data, get_all_sales_data, get_sales_data_by_id, update_sales_data, delete_sales_data ,create_prediction_data, get_prediction_data_by_id , get_prediction_data, create_prediction_by_id, predict_sales , train_model , predict_and_add

# Function to create a sales record
def add_sales_data(name, store_revenue, store_size, temp, variety_score, quality_range, 
                    shop_area, city_tier, availability, discounts, weekday_sales, 
                    weekend_sales, total_sales, location):
    create_sales_data(name, store_revenue, store_size, temp, variety_score, quality_range, 
                      shop_area, city_tier, availability, discounts, weekday_sales, weekend_sales, 
                      total_sales, location)

# Function to fetch all sales data
def fetch_all_sales_data():
    return get_all_sales_data()

# Function to fetch a specific sales record by ID
def fetch_sales_data_by_id(sales_id):
    return get_sales_data_by_id(sales_id)

# Function to update sales data by ID
def modify_sales_data(sales_id, name=None, store_revenue=None, store_size=None, temp=None, variety_score=None,
                       quality_range=None, shop_area=None, city_tier=None, availability=None, discounts=None,
                       weekday_sales=None, weekend_sales=None, total_sales=None, location=None):
    update_sales_data(sales_id, name, store_revenue, store_size, temp, variety_score, quality_range, 
                      shop_area, city_tier, availability, discounts, weekday_sales, weekend_sales, 
                      total_sales, location)

# Function to delete a sales record by ID
def remove_sales_data(sales_id):
    delete_sales_data(sales_id)


# Function to add prediction data 1
def add_prediction_data():
    return create_prediction_data()
    
# Function to add prediction data by ID
def add_prediction_data_by_id(prediction_id):
    return create_prediction_by_id(prediction_id) 

# Function to fetch prediction data
def fetch_prediction_data():
    return get_prediction_data()

# Function to fetch prediction data by ID
def fetch_prediction_data_by_id(prediction_id):
    return get_prediction_data_by_id(prediction_id)

def predict_sales_data(input_data):
    return predict_sales(input_data)

def train_ml_model():
    return train_model()

def predict_sales_and_add(input_data):
    return predict_and_add(input_data)