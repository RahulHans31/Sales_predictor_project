from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

Base = declarative_base()

class SalesData(Base):
    __tablename__ = 'sales_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    store_revenue = Column(Float)
    store_size = Column(String(10))
    temp = Column(String(10))
    variety_score = Column(Integer)
    quality_range = Column(Integer)
    shop_area = Column(Float)
    city_tier = Column(Integer)
    availability = Column(String(20))
    discounts = Column(Integer)
    weekday_sales = Column(Float)
    weekend_sales = Column(Float)
    total_sales = Column(Float)
    location = Column(String(30))

    # Define constraints using the correct logical condition
    __table_args__ = (
        CheckConstraint(
            expression.and_(variety_score >= 0, variety_score <= 10),
            name='variety_score_check'
        ),
        CheckConstraint(
            expression.and_(quality_range >= 0, quality_range <= 10),
            name='quality_range_check'
        ),
        CheckConstraint(
            expression.and_(city_tier >= 1, city_tier <= 3),
            name='city_tier_check'
        ),
        CheckConstraint(
            expression.and_(discounts >= 0, discounts <= 100),
            name='discounts_check'
        ),
        CheckConstraint(
            weekday_sales >= 0,
            name='weekday_sales_check'
        ),
        CheckConstraint(
            weekend_sales >= 0,
            name='weekend_sales_check'
        ),
        CheckConstraint(
            total_sales >= 0,
            name='total_sales_check'
        ),
    )

    # Add a __repr__ method to provide a readable output for the object
    def __repr__(self):
        return f"SalesData(id={self.id}, name={self.name}, store_revenue={self.store_revenue}, " \
               f"store_size={self.store_size}, variety_score={self.variety_score}, " \
               f"quality_range={self.quality_range}, city_tier={self.city_tier}, " \
               f"discounts={self.discounts}, weekday_sales={self.weekday_sales}, " \
               f"weekend_sales={self.weekend_sales}, total_sales={self.total_sales}, " \
               f"location={self.location})"
