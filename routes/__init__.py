from routes.health import router as health_router
from routes.movements import router as movements_router
from routes.products import router as products_router

__all__ = ["health_router", "products_router", "movements_router"]
