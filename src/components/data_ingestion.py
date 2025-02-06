import pandas as pd
from src.components.database import create_sales_data, get_all_sales_data
from src.components.database import Session  # Corrected import path

# Function to ingest data from the frontend and store it in the database
def ingest_sales_data(data):
    """
    This function takes data as input (usually a dictionary or JSON object from frontend), 
    and stores it in the database using the create_sales_data function from database.py.
    """
    name = data.get("name")
    store_revenue = data.get("store_revenue")
    store_size = data.get("store_size")
    temp = data.get("temp")
    variety_score = data.get("variety_score")
    quality_range = data.get("quality_range")
    shop_area = data.get("shop_area")
    city_tier = data.get("city_tier")
    availability = data.get("availability")
    discounts = data.get("discounts")
    weekday_sales = data.get("weekday_sales")
    weekend_sales = data.get("weekend_sales")
    total_sales = data.get("total_sales")
    location = data.get("location")
    
    # Storing data in the database using the provided function
    create_sales_data(name, store_revenue, store_size, temp, variety_score, quality_range, 
                      shop_area, city_tier, availability, discounts, weekday_sales, 
                      weekend_sales, total_sales, location)

# Function to extract data from the database and save it as a Pandas DataFrame
def extract_sales_data_to_dataframe():
    """
    This function fetches all sales data from the database and converts it into a Pandas DataFrame.
    """
    # Fetching all sales data from the database using the function from database.py
    sales_data = get_all_sales_data()
    
    # Converting the result into a Pandas DataFrame for easier analysis and manipulation
    data = pd.DataFrame([{
        'id': record.id,
        'name': record.name,
        'store_revenue': record.store_revenue,
        'store_size': record.store_size,
        'temp': record.temp,
        'variety_score': record.variety_score,
        'quality_range': record.quality_range,
        'shop_area': record.shop_area,
        'city_tier': record.city_tier,
        'availability': record.availability,
        'discounts': record.discounts,
        'weekday_sales': record.weekday_sales,
        'weekend_sales': record.weekend_sales,
        'total_sales': record.total_sales,
        'location': record.location
    } for record in sales_data])
    
    # Return the DataFrame
    return data

# Example usage:
# 1. Ingest new sales data (this will come from the frontend)
new_sales_data = {
    'name': 'Store A',
    'store_revenue': 10000.5,
    'store_size': 'Large',
    'temp': 'Low',
    'variety_score': 8,
    'quality_range': 7,
    'shop_area': 500.0,
    'city_tier': 1,
    'availability': 'Online',
    'discounts': 15,
    'weekday_sales': 200.0,
    'weekend_sales': 250.0,
    'total_sales': 450.0,
    'location': 'Downtown'
}


