from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    db_product = Product(
        nombre=product.nombre,
        precio=product.precio,
        stock=product.stock,
        categoria=product.categoria,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return db.query(Product).all()


@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, db: Session = Depends(get_db)) -> Product:
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product


@router.put("/{id}", response_model=ProductRead)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)) -> Product:
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    db_product.nombre = product.nombre
    db_product.precio = product.precio
    db_product.stock = product.stock
    db_product.categoria = product.categoria

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)) -> None:
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    db.delete(db_product)
    db.commit()
