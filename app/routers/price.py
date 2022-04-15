from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/prices",
    tags=['Prices']
)


@router.get("/{symbol}", response_model=List[schemas.PriceOut])
def get_prices(symbol: str, db: Session = Depends(get_db), limit: int = 50, skip: int = 0):
    """Get low, open, close, and high prices, with volume for 30 days"""
    price = db.query(models.Price).filter(models.Price.stock_symbol == symbol.upper()).limit(limit).offset(skip).all()

    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prices for stock: {symbol} not found")

    return price