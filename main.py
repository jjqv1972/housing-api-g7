
from fastapi import FastAPI

from database import engine
from models import Base
from routers import housing

app = FastAPI(
    title="Housing API con FastAPI",
    description="API para predicción de precios de viviendas usando Machine Learning, FastAPI y SQLAlchemy",
    version="1.0.0"
)

app.include_router(housing.router)

@app.get("/")
def index():
    return {
        "title": "FASTAPI HOUSING API VERSION 1.0",
        "message": "Bienvenido a mi API"
    }
