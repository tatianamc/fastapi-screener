from . import models
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from .utils import db_populated, populate_db
from .routers import page, stock, price


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

# Fill database from supporting API if empty
if not db_populated(models.Stock):
    populate_db()

app.include_router(page.router)
app.include_router(stock.router)
app.include_router(price.router)
