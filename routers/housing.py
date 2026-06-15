from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Housing
from ml_model import predict_price

from schemas import (
    HousingCreate,
    HousingPredictionResponse
)

router = APIRouter(
    prefix="/housing",
    tags=["Housing"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/price",response_model=HousingPredictionResponse)
def housing_price(data: HousingCreate):
    price = predict_price(data.rooms)

    return {
        "message": "precio predicho",
        "habitaciones": data.rooms,
        "precio": price
    }