from typing import List, Literal
from pydantic import BaseModel
from datetime import datetime


class Stock(BaseModel):
    symbol: str
    name: str
    long_summary: str
    price: float
    market_cap: int
    pe_ratio: float
    peg_ratio: float
    low_52_week: float
    high_52_week: float
    beta: float


class StockOut(Stock):
    class Config:
        orm_mode = True


class FilterGroupIn(BaseModel):
    filter: Literal["Price", 
        "Market cap", 
        "PE ratio", 
        "PEG ratio", 
        "Volume", 
        "52 week low", 
        "52 week high", 
        "Forward EPS", 
        "Beta"
    ]
    operator: Literal["Greater than", "Less than", "Equal to"]
    value: float


class FilterSortIn(BaseModel):
    column: int = 0
    direction: Literal[-1, 1]


class FilterIn(BaseModel):
    filters: List[FilterGroupIn] | None = None
    sort: FilterSortIn


class FilterOut(FilterIn):
    stocks: List[StockOut]
    class config:
        orm_mode = True


class Price(BaseModel):    
    price_date: datetime
    open: float
    close: float
    low: float
    high: int
    volume: int
    stock_symbol: str
    id: int


class PriceOut(BaseModel):
    price_date: datetime
    open: float
    close: float
    low: float
    high: int
    volume: int
    
    class Config:
        orm_mode = True