from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
