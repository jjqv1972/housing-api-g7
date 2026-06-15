
from fastapi import FastAPI
from pydantic import BaseModel, Field
from ml_model import predict_price

app = FastAPI()

#schema validador
class Housing(BaseModel):
    rooms: int
    
@app.get("/")
def home():
    return {"message":"Housing API"}

@app.post("/housing_price")
def housing_price(housing: Housing):
    rooms = housing.rooms
    price = predict_price(rooms)
    
    return{
        "rooms": rooms,
        "price": price
    }
    
