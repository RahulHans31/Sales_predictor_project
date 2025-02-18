from src.database.connection import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database.schemas import SalesData , PredictionData
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

pipeline = pickle.load(open('src/model.pkl', 'rb'))

def preprocess_data(df):
    # Drop irrelevant columns
    df_cleaned = df.drop(columns=["id", "Name", "Weekend_sales", "Weekday_sales"], errors='ignore')

    # Convert categorical variables into numeric using one-hot encoding
    categorical_cols = ["Store_size", "Availability", "Location", "Temp"]
    df_cleaned = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True, dtype=int)

    # Handle missing values by filling with the median
    df_cleaned = df_cleaned.fillna(df_cleaned.median(numeric_only=True))

    # Define expected columns from model training
    expected_columns = ['Store_revenue', 'Variety_score', 'Quality_range', 'Shop_area', 'City_tier', 
                         'Discounts', 'Store_size_Mid', 'Store_size_Small', 'Availability_Online', 
                         'Location_Outskirts', 'Temp_Low', 'Temp_Mid', 'Temp_low']

    # Add missing columns with default value 0
    for col in expected_columns:
        if col not in df_cleaned.columns:
            df_cleaned[col] = 0

    # Drop any extra columns not seen during model training
    df_cleaned = df_cleaned.reindex(columns=expected_columns, fill_value=0)

    return df_cleaned

def train_model():
    session = Session()
    try:
        records = session.query(SalesData).all()

        # Convert to DataFrame
        data = pd.DataFrame([{
            'Store_revenue': record.store_revenue,
            'Store_size': record.store_size,
            'Temp': record.temp,
            'Variety_score': record.variety_score,
            'Quality_range': record.quality_range,
            'Shop_area': record.shop_area,
            'City_tier': record.city_tier,
            'Availability': record.availability,
            'Discounts': record.discounts,
            'Location': record.location,
            'Total_sales': record.total_sales
        } for record in records])
        print('done')

        # Preprocess data
        cleaned_data = preprocess_data(data)
        print('done')
        # Split features and target
        X = cleaned_data.drop(columns=['Total_sales'], errors='ignore')
        y = cleaned_data['Total_sales']
        print('done')
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print('done')
        model = pickle.load(open('src/model.pkl', 'rb'))
        # # Train the Random Forest Regressor model
        # model = RandomForestRegressor(random_state=42)
        # model.fit(X_train, y_train)
        # print('done')

        # Evaluate the model
        # y_pred = model.predict(X_test)
        # mse = mean_squared_error(y_test, y_pred)
        # print(f"Model trained successfully with MSE: {mse}")
        # print('done')

        # Save the model as a pickle file
        # with open('src/model.pkl', 'wb') as file:
        #     pickle.dump(model, file)

        # Predict and store predictions in the database
        data['Predicted_sales'] = model.predict(X)

        for i, record in data.iterrows():
            prediction = PredictionData(
                id=records[i].id,  # Link to the SalesData ID
                predicted_sales=record['Predicted_sales']
            )
            session.add(prediction)

        session.commit()
        print("Predictions saved successfully!")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error training model: {e}")
    finally:
        session.close()


# CREATE: Add a new sales record to the database
def create_sales_data(name, store_revenue, store_size, temp, variety_score, quality_range, 
                      shop_area, city_tier, availability, discounts, weekday_sales, 
                      weekend_sales, total_sales, location):
    session = Session()  # Create a session instance
    try:
        new_sales = SalesData(
            name=name,
            store_revenue=store_revenue,
            store_size=store_size,
            temp=temp,
            variety_score=variety_score,
            quality_range=quality_range,
            shop_area=shop_area,
            city_tier=city_tier,
            availability=availability,
            discounts=discounts,
            weekday_sales=weekday_sales,
            weekend_sales=weekend_sales,
            total_sales=total_sales,
            location=location
        )
        session.add(new_sales)
        session.commit()
        print(f"New sales data for {name} added successfully!")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding sales data: {e}")
    finally:
        session.close()

# READ: Get all sales records from the database
def get_all_sales_data():
    session = Session()
    try:
        sales_data = session.query(SalesData).all()
        return sales_data
    except SQLAlchemyError as e:
        print(f"Error fetching sales data: {e}")
    finally:
        session.close()

# READ: Get a specific sales record by ID
def get_sales_data_by_id(sales_id):
    session = Session()
    try:
        sales_data = session.query(SalesData).filter(SalesData.id == sales_id).first()
        if sales_data:
            return sales_data
        else:
            print(f"No sales data found with ID {sales_id}")
    except SQLAlchemyError as e:
        print(f"Error fetching sales data: {e}")
    finally:
        session.close()

# UPDATE: Update a specific sales record by ID
def update_sales_data(sales_id, name=None, store_revenue=None, store_size=None, temp=None, variety_score=None,
                       quality_range=None, shop_area=None, city_tier=None, availability=None, discounts=None,
                       weekday_sales=None, weekend_sales=None, total_sales=None, location=None):
    session = Session()
    try:
        sales_data = session.query(SalesData).filter(SalesData.id == sales_id).first()
        if sales_data:
            if name:
                sales_data.name = name
            if store_revenue:
                sales_data.store_revenue = store_revenue
            if store_size:
                sales_data.store_size = store_size
            if temp:
                sales_data.temp = temp
            if variety_score is not None:
                sales_data.variety_score = variety_score
            if quality_range is not None:
                sales_data.quality_range = quality_range
            if shop_area:
                sales_data.shop_area = shop_area
            if city_tier:
                sales_data.city_tier = city_tier
            if availability:
                sales_data.availability = availability
            if discounts is not None:
                sales_data.discounts = discounts
            if weekday_sales:
                sales_data.weekday_sales = weekday_sales
            if weekend_sales:
                sales_data.weekend_sales = weekend_sales
            if total_sales:
                sales_data.total_sales = total_sales
            if location:
                sales_data.location = location

            session.commit()
            print(f"Sales data for ID {sales_id} updated successfully!")
        else:
            print(f"No sales data found with ID {sales_id}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating sales data: {e}")
    finally:
        session.close()

# DELETE: Delete a specific sales record by ID
def delete_sales_data(sales_id):
    session = Session()
    try:
        sales_data = session.query(SalesData).filter(SalesData.id == sales_id).first()
        if sales_data:
            session.delete(sales_data)
            session.commit()
            print(f"Sales data for ID {sales_id} deleted successfully!")
        else:
            print(f"No sales data found with ID {sales_id}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting sales data: {e}")
    finally:
        session.close()


def create_prediction_data():
    session = Session() 
    try :
        sales_data_records = session.query(SalesData).all()
        for record in sales_data_records:
            prediction_data = pd.DataFrame([{
                'Store_revenue': record.store_revenue,
            'Store_size': record.store_size,
            'Temp': record.temp,
            'Variety_score': record.variety_score,
            'Quality_range': record.quality_range,
            'Shop_area': record.shop_area,
            'City_tier': record.city_tier,
            'Availability': record.availability,
            'Discounts': record.discounts,
            'Location': record.location
            }])
            cleaned_data = preprocess_data(prediction_data)
            predicted_sales = pipeline.predict(cleaned_data)
            
            prediction = PredictionData(
                id=record.id,  # Link to the SalesData ID
                predicted_sales=predicted_sales
            )
            
            session.add(prediction)
        
        session.commit()
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding prediction data: {e}")
    finally:
        session.close()
        
            
def create_prediction_by_id(sales_id):
    session = Session()
    try:
        record = session.query(SalesData).filter(SalesData.id == sales_id).first()
        if not record:
            print(f"No sales data found with ID {sales_id}")
            return
        prediction_data = pd.DataFrame([{
                'Store_revenue': record.store_revenue,
            'Store_size': record.store_size,
            'Temp': record.temp,
            'Variety_score': record.variety_score,
            'Quality_range': record.quality_range,
            'Shop_area': record.shop_area,
            'City_tier': record.city_tier,
            'Availability': record.availability,
            'Discounts': record.discounts,
            'Location': record.location
            }])
        
        cleaned_data = preprocess_data(prediction_data)
        predicted_sales = pipeline.predict(cleaned_data)
        
        prediction = PredictionData(
            id=record.id,  # Link to the SalesData ID
            predicted_sales=predicted_sales
        )
        
        session.add(prediction)
    
        session.commit()
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding prediction data: {e}")
    finally:
        session.close()
        

def get_prediction_data():
    session = Session()
    try:
        # Fetch all prediction records
        predictions = session.query(PredictionData).all()
        return predictions
    except SQLAlchemyError as e:
        print(f"Error fetching predictions: {e}")
    finally:
        session.close()
        
def get_prediction_data_by_id(prediction_id):  
    session = Session() 
    try:
        prediction = session.query(PredictionData).filter(PredictionData.id == prediction_id).first()
        if prediction:
            return prediction
        else:
            print(f"No prediction data found with ID {prediction_id}")
    except SQLAlchemyError as e:
        print(f"Error fetching prediction data: {e}")
    finally:
        session.close()
        
def predict_sales(input_data):
    try:
        # Prepare the input data (convert to DataFrame)
        prediction_data = pd.DataFrame([input_data])

        # Preprocess the data
        cleaned_data = preprocess_data(prediction_data)

        # Predict sales using the model
        predicted_sales = pipeline.predict(cleaned_data)[0]
        return predicted_sales

    except Exception as e:
        print(f"Error predicting sales: {e}")
        return None
    
def predict_and_add(record):
    
    prediction_data = pd.DataFrame([{
            'Store_revenue': record.store_revenue,
        'Store_size': record.store_size,
        'Temp': record.temp,
        'Variety_score': record.variety_score,
        'Quality_range': record.quality_range,
        'Shop_area': record.shop_area,
        'City_tier': record.city_tier,
        'Availability': record.availability,
        'Discounts': record.discounts,
        'Location': record.location
        }])
    
    cleaned_data = preprocess_data(prediction_data)
    predicted_sales = pipeline.predict(cleaned_data)
    print(predicted_sales)
    
    
    return predicted_sales
    

