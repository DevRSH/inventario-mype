from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MovementBase(BaseModel):
    producto_id: int = Field(gt=0)
    tipo: Literal["entrada", "salida"]
    cantidad: int = Field(gt=0)
    fecha: datetime = Field(default_factory=datetime.utcnow)


class MovementCreate(MovementBase):
    pass


class MovementRead(MovementBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
