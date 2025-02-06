import streamlit as st
import requests
import pandas as pd
from utils import format_sales_data

# FastAPI URL
API_URL = "https://sales-predictor-project.onrender.com/sales/"

# Streamlit UI
def main():
    st.title("Sales Prediction Dashboard")
    
    # Sidebar for navigation
    st.sidebar.header("Sales Data Operations")
    choice = st.sidebar.selectbox("Select Operation", ["Add Sales Data", "View All Sales", "View Sales by ID", "Update Sales Data", "Delete Sales Data"])

    # Add Sales Data Form
    if choice == "Add Sales Data":
        add_sales_data()

    # View All Sales Data
    elif choice == "View All Sales":
        view_all_sales()

    # View Sales by ID
    elif choice == "View Sales by ID":
        view_sales_by_id()

    # Update Sales Data
    elif choice == "Update Sales Data":
        update_sales_data()

    # Delete Sales Data
    elif choice == "Delete Sales Data":
        delete_sales_data()
    
    elif choice == "Predict Sales Data" :
        predict_sales_data()

# Function to add sales data
def add_sales_data():
    st.subheader("Add Sales Data")
    name = st.text_input("Store Name")
    store_revenue = st.number_input("Store Revenue", min_value=0.0)
    store_size = st.text_input("Store Size")
    temp = st.text_input("Temperature")
    variety_score = st.slider("Variety Score", 0, 10)
    quality_range = st.slider("Quality Range", 0, 10)
    shop_area = st.number_input("Shop Area", min_value=0.0)
    city_tier = st.slider("City Tier", 1, 3)
    availability = st.text_input("Availability")
    discounts = st.number_input("Discounts", min_value=0)
    weekday_sales = st.number_input("Weekday Sales", min_value=0.0)
    weekend_sales = st.number_input("Weekend Sales", min_value=0.0)
    total_sales = weekday_sales + weekend_sales
    location = st.text_input("Location")

    if st.button("Submit"):
        payload = {
            "name": name,
            "store_revenue": store_revenue,
            "store_size": store_size,
            "temp": temp,
            "variety_score": variety_score,
            "quality_range": quality_range,
            "shop_area": shop_area,
            "city_tier": city_tier,
            "availability": availability,
            "discounts": discounts,
            "weekday_sales": weekday_sales,
            "weekend_sales": weekend_sales,
            "total_sales": total_sales,
            "location": location
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 201:
            st.success("Sales Data Added Successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")

# Function to view all sales data
def view_all_sales():
    st.subheader("View All Sales Data")
    response = requests.get(API_URL)
    if response.status_code == 200:
        sales_data = response.json()
        if sales_data:
            sales_df = pd.DataFrame(sales_data)
            st.dataframe(sales_df)
        else:
            st.warning("No data found.")
    else:
        st.error(f"Error: {response.json()['detail']}")

# Function to view sales data by ID
def view_sales_by_id():
    st.subheader("View Sales Data by ID")
    sales_id = st.number_input("Sales ID", min_value=1, step=1)
    if st.button("Fetch Data"):
        response = requests.get(f"{API_URL}{sales_id}")
        if response.status_code == 200:
            sales_data = response.json()
            st.json(sales_data)
        else:
            st.error(f"Error: {response.json()['detail']}")

# Function to update sales data
def update_sales_data():
    st.subheader("Update Sales Data")
    sales_id = st.number_input("Sales ID", min_value=1, step=1)
    if st.button("Fetch Data"):
        response = requests.get(f"{API_URL}{sales_id}")
        if response.status_code == 200:
            sales_data = response.json()
            updated_data = st.text_area("Updated Data", value=str(sales_data))
            if st.button("Update"):
                response = requests.put(f"{API_URL}{sales_id}", json=updated_data)
                if response.status_code == 200:
                    st.success("Sales Data Updated Successfully!")
                else:
                    st.error(f"Error: {response.json()['detail']}")
        else:
            st.error(f"Error: {response.json()['detail']}")

# Function to delete sales data
def delete_sales_data():
    st.subheader("Delete Sales Data")
    sales_id = st.number_input("Sales ID", min_value=1, step=1)
    if st.button("Delete"):
        response = requests.delete(f"{API_URL}{sales_id}")
        if response.status_code == 200:
            st.success("Sales Data Deleted Successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")
            
def predict_sales_data():
    st.subheader("Predict Sales Data")
    name = st.text_input("Store Name")
    store_revenue = st.number_input("Store Revenue", min_value=0.0)
    store_size = st.text_input("Store Size")
    temp = st.text_input("Temperature")
    variety_score = st.slider("Variety Score", 0, 10)
    quality_range = st.slider("Quality Range", 0, 10)
    shop_area = st.number_input("Shop Area", min_value=0.0)
    city_tier = st.slider("City Tier", 1, 3)
    availability = st.text_input("Availability")
    discounts = st.number_input("Discounts", min_value=0)
    weekday_sales = st.number_input("Weekday Sales", min_value=0.0)
    weekend_sales = st.number_input("Weekend Sales", min_value=0.0)
    total_sales = weekday_sales + weekend_sales
    location = st.text_input("Location")
    
    if st.button("Predict"):
        payload = {
            "name": name,
            "store_revenue": store_revenue,
            "store_size": store_size,
            "temp": temp,
            "variety_score": variety_score,
            "quality_range": quality_range,
            "shop_area": shop_area,
            "city_tier": city_tier,
            "availability": availability,
            "discounts": discounts,
            "weekday_sales": weekday_sales,
            "weekend_sales": weekend_sales,
            "total_sales": total_sales,
            "location": location
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            sales_data = response.json()
            formatted_data = format_sales_data(sales_data)
            st.json(formatted_data)
        else:
            st.error(f"Error: {response.json()['detail']}")

if __name__ == '__main__':
    main()
