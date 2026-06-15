from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Housing
from ml_model import predict_price

from schemas import (
    HousingCreate,
    HousingPredictionResponse,
    HousingResponse
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
    
@router.post("/",response_model=HousingResponse)
def create_housing(data: HousingCreate,db: Session = Depends(get_db)):
    price = predict_price(data.rooms)

    new_housing = Housing(
        rooms = data.rooms,
        price = price
    )
    
    db.add(new_housing)
    db.commit()
    db.refresh(new_housing)

    return new_housing

@router.get("/",response_model=list[HousingResponse])
def get_housing(db: Session = Depends(get_db)):
    return db.query(Housing).all()

@router.get("/{housing_id}", response_model=HousingResponse)
def get_housing_by_id(housing_id: int, db: Session = Depends(get_db)):
    housing = db.query(Housing).filter(Housing.id == housing_id).first()

    if not housing:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return housing

@router.put("/{housing_id}", response_model=HousingResponse)
def update_housing(
    housing_id: int,
    data: HousingCreate,
    db: Session = Depends(get_db)
):
    housing = db.query(Housing).filter(Housing.id == housing_id).first()

    if not housing:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    price = predict_price(data.rooms)

    housing.rooms = data.rooms
    housing.price = price

    db.commit()
    db.refresh(housing)

    return housing

@router.delete("/{housing_id}")
def delete_housing(housing_id: int, db: Session = Depends(get_db)):
    housing = db.query(Housing).filter(Housing.id == housing_id).first()

    if not housing:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(housing)
    db.commit()

    return {"message": "Registro eliminado correctamente"}