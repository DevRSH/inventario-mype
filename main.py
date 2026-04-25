from fastapi import FastAPI

from database.init_db import init_db
from routes.health import router as health_router
from routes.movements import router as movements_router
from routes.products import router as products_router

app = FastAPI(title="Inventario MYPE API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(health_router)
app.include_router(products_router)
app.include_router(movements_router)
