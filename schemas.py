from pydantic import BaseModel, Field

class HousingCreate(BaseModel):
    rooms: int = Field(..., example=5)
    
class HousingPredictionResponse(BaseModel):
    message: str
    habitaciones: int
    precio: float