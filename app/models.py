from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, nullable=False)
    price_date = Column(TIMESTAMP(timezone=True), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    stock_symbol = Column(String, ForeignKey("stocks.symbol", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("Stock")


class Stock(Base):
    __tablename__ = "stocks"
    symbol = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    market_cap = Column(BigInteger, nullable=False)
    pe_ratio = Column(Float, nullable=False)
    long_summary = Column(String, nullable=False)
    peg_ratio = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    low_52_week = Column(Float, nullable=False)
    high_52_week = Column(Float, nullable=False)
    forward_eps = Column(Float, nullable=False)
    beta = Column(Float, nullable=False)
    