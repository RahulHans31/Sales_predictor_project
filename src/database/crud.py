from src.database.connection import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database.schemas import SalesData

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
            print(sales_data)
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
