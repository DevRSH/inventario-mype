from database.connection import Base, engine
from models.item import Item
from models.movement import Movement
from models.product import Product


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
