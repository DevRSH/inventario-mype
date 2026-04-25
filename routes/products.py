from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.connection import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


def _get_product_or_404(db: Session, product_id: int) -> Product:
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar productos",
        ) from exc

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    db_product = Product(
        nombre=product.nombre,
        precio=product.precio,
        stock=product.stock,
        categoria=product.categoria,
    )

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear producto",
        ) from exc

    return db_product


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    try:
        return db.query(Product).all()
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar productos",
        ) from exc


@router.get("/{id}", response_model=ProductRead)
def get_product(id: int = Path(gt=0), db: Session = Depends(get_db)) -> Product:
    return _get_product_or_404(db=db, product_id=id)


@router.put("/{id}", response_model=ProductRead)
def update_product(product: ProductUpdate, id: int = Path(gt=0), db: Session = Depends(get_db)) -> Product:
    db_product = _get_product_or_404(db=db, product_id=id)

    db_product.nombre = product.nombre
    db_product.precio = product.precio
    db_product.stock = product.stock
    db_product.categoria = product.categoria

    try:
        db.commit()
        db.refresh(db_product)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar producto",
        ) from exc

    return db_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int = Path(gt=0), db: Session = Depends(get_db)) -> None:
    db_product = _get_product_or_404(db=db, product_id=id)

    try:
        db.delete(db_product)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar producto",
        ) from exc
