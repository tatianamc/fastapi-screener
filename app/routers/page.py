from typing import List
from fastapi import status, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates
from ..utils import stocks_name_index


router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, response_model=List[schemas.StockOut])
def screener_homepage(request: Request, db: Session = Depends(get_db), limit: int = 25, skip: int = 0):
    """"Home page: Display a table of stocks."""
    stocks = db.query(models.Stock).limit(limit).offset(skip).all()

    # Gather Stock table column names and remove non-numeric cols for UI 
    sql_col_names = models.Stock.__table__.c.keys()
    sql_col_names.remove("symbol")
    sql_col_names.remove("name")
    sql_col_names.remove("long_summary")

    return templates.TemplateResponse("screener.html", {
        "request": request,
        "stocks": stocks,
        # Include both sql and human versions of the table columns
        "sql_cols": sql_col_names,
        "name_index": stocks_name_index
    })


@router.post("/", response_model=schemas.FilterOut)
def screener_filter(request: Request, filter_data: schemas.FilterIn, db: Session = Depends(get_db)): 
    """Home page: Filter/search stocks by a number of filters, operands, and values."""
    filter_dict = filter_data.dict()['filters']
    stocks = db.query(models.Stock)

    for filter in filter_dict:
        # convert user-facing column names to database column names
        filter_sql = list(stocks_name_index.keys())[list(stocks_name_index.values()).index(filter['filter'])]

        if filter['operator'] == "Greater than":
            stocks = stocks.filter(getattr(models.Stock, filter_sql) >= filter['value'])
        elif filter['operator'] == "Less than":
            stocks = stocks.filter(getattr(models.Stock, filter_sql) <= filter['value'])
        else:
            stocks = stocks.filter(getattr(models.Stock, filter_sql) == filter['value'])
    
    # Handle sort direction of data
    sql_col_names = models.Stock.__table__.c.keys()
    if filter_data.sort.direction == 1:
        stocks = stocks.order_by(getattr(models.Stock, sql_col_names[filter_data.sort.column]))
    else:
        stocks = stocks.order_by(getattr(models.Stock, sql_col_names[filter_data.sort.column]).desc())
    
    stocks = stocks.all()
    
    if not stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stocks with filter criteria not found")
    
    response_data = filter_data.dict()
    response_data['stocks'] = stocks
    return response_data



# About page - info about screener
@router.get("/about", response_class=HTMLResponse, response_model=List[schemas.StockOut])
def screener_about(request: Request):
    """About page: Information about the project."""
    return templates.TemplateResponse("about.html", {"request": request})


# Price page - graphical info about prices
@router.get("/priceinfo/{symbol}")
def screener_price_chart(symbol: str, request: Request, db: Session = Depends(get_db)):
    """Price-info page: Candlestick chart and long summary for a stock."""
    stock = db.query(models.Stock).filter(models.Stock.symbol == symbol.upper()).first()

    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with symbol: {symbol} not found")

    return templates.TemplateResponse("prices.html", {
        "request": request,
        "stock": stock
    })