from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    nombre: str
    stock: int
    precio: float


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
