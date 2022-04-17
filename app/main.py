from . import models
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from .utils import db_populated, populate_db
from .routers import page, stock, price
from starlette.responses import FileResponse


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")


# Add favicon
favicon_path = 'app/favicon.ico'
@app.get('/favicon.ico', include_in_schema=False)
def favicon():
    return FileResponse(favicon_path)

# Fill database from supporting API if empty
if not db_populated(models.Stock):
    populate_db()

app.include_router(page.router)
app.include_router(stock.router)
app.include_router(price.router)

