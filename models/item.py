from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    precio: Mapped[float] = mapped_column(Float, nullable=False, default=0)
