from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Global variable to store the engine and session
engine = None
Session = None

def create_connection():
    global engine, Session

    if engine is None:
        try:
            # Replace the following with your actual database URI
            db_uri = "mysql+pymysql://avnadmin:AVNS_qvEBzX9oMVXmcHFoxl_@sales-predictor-rknldeals-1e64.f.aivencloud.com:17496/sales_predictor"
            
            # Create the database engine
            engine = create_engine(db_uri)
            
            # Create the session
            Session = sessionmaker(bind=engine)
            print("Connection established successfully")
        except SQLAlchemyError as e:
            print(f"Error connecting to database: {e}")
            return None

    return engine

# Call create_connection() to ensure the engine and session are initialized
create_connection()
