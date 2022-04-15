# FastAPI Stock Screener
This is a stock screener that displays useful fundamental and price data for stocks in the SP 500.

Users can filter stocks based on a number of attributes, and view graphical price data.

**NOTE:** stock/price data is not updated regularly. This project is meant for demonstration and educational purposes only. See [license]().

Technologies used:
 - Databse built with PostgreSQL with SQLAlchemy ORMs and Alembic for migrations.
 - Initial market data stored with the yfinance module.
 - FastAPI for screener API and automatic documentation.
 - Frontend UI built with Bootstrap 5, AlpineJS, Axios, and Jinja2 templates.
 - Price charts done with Google Visualisations.
 - Deployed on Heroku.

## Installation

Install using `pip install -r requirements.txt` and run with `uvicorn app.main:app --reload`.