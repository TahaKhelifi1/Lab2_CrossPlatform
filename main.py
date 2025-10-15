from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ---------------------- DATABASE CONFIG ----------------------
# Read the database URL from the environment so Docker and local runs work the same.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Taha2004@localhost:5432/product_catalog")

# Create engine and session factory. Disable autoflush/autocommit for predictable behavior.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------- MODEL ----------------------
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)


# ---------------------- SCHEMA ----------------------
class ProductCreate(BaseModel):
    name: str
    price: float

class ProductResponse(ProductCreate):
    id: int
    class Config:
        orm_mode = True


# ---------------------- APP ----------------------
app = FastAPI(title="Product Catalog API")


@app.get("/products", response_model=List[ProductResponse])
def get_products():
    """Retourne tous les produits de la base de données"""
    with SessionLocal() as db:
        products = db.query(Product).all()
        return products


@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    """⚠️ Cet endpoint NE sera PAS exposé dans MCP"""
    with SessionLocal() as db:
        new_product = Product(name=product.name, price=product.price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
