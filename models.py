from sqlalchemy import Column, Integer, Float
from database import Base

class Housing(Base):
    __tablename__ = "housing"
    
    id = Column(Integer, primary_key=True, index=True)
    rooms = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)