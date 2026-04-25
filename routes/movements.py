from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.movement import Movement
from models.product import Product
from schemas.movement import MovementCreate, MovementRead

router = APIRouter(prefix="/movements", tags=["Movements"])


@router.post("", response_model=MovementRead, status_code=status.HTTP_201_CREATED)
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)) -> Movement:
    product = db.query(Product).filter(Product.id == movement.producto_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    if movement.tipo == "entrada":
        product.stock += movement.cantidad
    else:
        if product.stock < movement.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente para registrar salida",
            )
        product.stock -= movement.cantidad

    db_movement = Movement(
        producto_id=movement.producto_id,
        tipo=movement.tipo,
        cantidad=movement.cantidad,
        fecha=movement.fecha,
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement


@router.get("", response_model=list[MovementRead])
def list_movements(db: Session = Depends(get_db)) -> list[Movement]:
    return db.query(Movement).order_by(Movement.fecha.desc(), Movement.id.desc()).all()
