from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/stocks",
    tags=['Stocks']
)


@router.get("/{symbol}", response_model=schemas.StockOut)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    """Get fundamental information on a stock chosen by symbol."""
    stock = db.query(models.Stock).filter(models.Stock.symbol == symbol.upper()).first()

    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with symbol: {symbol} not found")

    return stock 


@router.get("/", response_model=List[schemas.StockOut])
def get_stocks(db: Session = Depends(get_db), limit: int = 25, skip: int = 0, search: str | None = ""):
    """Get fundamental information on a number of stocks (default: 25) with search."""
    stocks = db.query(models.Stock).group_by(models.Stock.symbol).filter(
        models.Stock.symbol.contains(search.upper())).limit(limit).offset(skip).all()
    
    if search and not stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stocks with following search: {search} not found")
    
    return stocks