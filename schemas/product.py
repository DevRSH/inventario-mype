from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class ProductBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    categoria: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
