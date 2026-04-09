from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from app.db.session import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    order_items = relationship("app.models.order.OrderItem", back_populates="product")
    