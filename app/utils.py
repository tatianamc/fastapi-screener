import yfinance as yf
from . import models
from time import sleep
from .database import SessionLocal
import datetime as dt


stocks_name_index = {
    "symbol": "Symbol",
    "name": "Name",
    "price": "Price",
    "market_cap": "Market cap",
    "pe_ratio": "PE ratio",
    'long_summary': 'Long Summary',
    "peg_ratio": "PEG ratio",
    'volume': 'Volume',
    "low_52_week": "52 week low",
    "high_52_week": "52 week high",
    'forward_eps': 'Forward EPS',
    "beta": "Beta"
}


def populate_db():
    """Populate database if it is empty at startup."""
    db = SessionLocal()
    tickers = []
    with open("app/sp500tickers.txt") as file:
        tickers = file.read().split('\n')

    for symbol in tickers:
        symbol_data = yf.Ticker(symbol).info
        print(symbol, symbol_data)
        if 'symbol' not in symbol_data:
            print(f"Skipping {symbol}, is invalid")
            continue
        if 'longBusinessSummary' not in symbol_data:
            symbol_data['longBusinessSummary'] = "No summary available."          
        stock = {
            'symbol': symbol_data['symbol'],
            'name': symbol_data['shortName'],
            'price': symbol_data['currentPrice'],
            'market_cap': symbol_data['marketCap'],
            'pe_ratio': symbol_data['forwardPE'],
            'long_summary': symbol_data['longBusinessSummary'],
            'peg_ratio': symbol_data['pegRatio'],
            'volume': symbol_data['volume'],
            'low_52_week': symbol_data['fiftyTwoWeekLow'],
            'high_52_week': symbol_data['fiftyTwoWeekHigh'],
            'forward_eps': symbol_data['forwardEps'],
            'beta': symbol_data['beta']
        }
        
        # For now we skip over any stocks that have null items
        skip = False
        for key, val in stock.items():
            if val is None:
                skip = True
                break
        if skip:
            print(f"Skipped {stock['symbol']}")
            continue

        new_stock = models.Stock(**stock)
        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)
        print(f"Added {stock['symbol']}")
        sleep(0.65)

        # Get price data for a month ago
        month_ago = dt.date.today() - dt.timedelta(days=32)
        symbol_history = yf.Ticker(symbol).history(start=month_ago)
        print(symbol_history)
        for index, row in symbol_history.iterrows():
            print(index)
            price_data = {
                'price_date': index.date(), 
                'open': row[0],
                'high': row[1],
                'low': row[2],
                'close': row[3],
                'volume': row[4],
                'stock_symbol': symbol_data['symbol']
            }
            new_price = models.Price(**price_data)
            db.add(new_price)
            db.commit()
            db.refresh(new_price)
        sleep(0.65)
        print(f"Added price data for {stock['symbol']}")

    db.close()


def db_populated(model):
    """Ping database table, check if empty."""
    db = SessionLocal()
    row_exists = db.query(model).first()
    db.close()
    return True if row_exists else False