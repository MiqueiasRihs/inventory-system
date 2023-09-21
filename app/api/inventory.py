from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.constants import get_stock_availability_inventory
from sql.database import SessionLocal, engine

from typing import List, Union

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/estoque/estoque-fisico", response_model=List[schemas.Inventory])
def register_product(products: List[schemas.InventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if inventory:
            raise HTTPException(status_code=400, detail=f"O produto com ID {product.id} já existe, tente atualizá-lo")
        
        created_product = crud.create_inventory(db=db, inventory=product)
        created_products.append(created_product)
    
    return created_products


@router.put("/estoque/estoque-fisico/{product_id}", response_model=schemas.Inventory)
def update_product_inventory(product_id: int, product: schemas.UpdateProductQuantity, db: Session = Depends(get_db)):
    inventory_prod = crud.get_inventory_by_id(db, id=product_id)
    if not inventory_prod:
        raise HTTPException(status_code=400, detail="Este produto não existe, tente cria-lo antes")

    return crud.update_inventory_quantity(db, inventory_prod.id, product.quantity)


@router.post("/estoque/estoque-futuro", response_model=List[schemas.FutureInventory])
def register_future_inventory(products: List[schemas.FutureInventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        future_inventory = crud.get_future_inventory_by_id(db, id=product.id)

        if future_inventory:
            raise HTTPException(status_code=400, detail=f"O estoque futuro do produto com ID {product.id} já existe, tente atualizá-lo")
            
        created_product = crud.create_future_inventory(db=db, product=product)
        created_products.append(created_product)

    return created_products


@router.post("/estoque/reserva", response_model=List[schemas.ReservationInventory])
def inventory_reservation(products: List[schemas.ReservationInventoryCreate], db: Session = Depends(get_db)):
    reservations_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if not inventory:
            raise HTTPException(status_code=400, detail=f"Não é possivel realizar a reserva pois o produto com ID {product.id} não existe")

        stock_availability = get_stock_availability_inventory(db, product.id, None)
        if product.quantity > stock_availability["current_difference"]:
            raise HTTPException(status_code=400, detail=f"Não é possivel reservar pois não existe estoque suficiente para o produto com ID {product.id}, o estoque atual é {stock_availability['current_difference']}")
            
        created_product = crud.create_inventory_reservation(db=db, product=product, inventory_id=inventory.id)
        reservations_products.append(created_product)

    return reservations_products


@router.post("/estoque/consulta/{strategy}")
def consult_inventory(strategy: str, products: List[schemas.Consult], db: Session = Depends(get_db)):
    result = []

    for product in products:
        stock_availability = get_stock_availability_inventory(db, product.id, strategy)

        if strategy == "estoque-fisico":
            result.append(schemas.ConsultResult(
                id=product.id,
                quantity=product.quantity,
                stock_availability=stock_availability.get("stock_availability"),
                available=product.quantity <= stock_availability.get("stock_availability")
            ))

        elif strategy == "estoque-futuro":
            result.append(schemas.ConsultResultFutureInventory(
                id=product.id,
                quantity=product.quantity,
                stock_availability=stock_availability.get("stock_availability"),
                available=product.quantity <= stock_availability.get("stock_availability"),
                inventory_available_date=stock_availability.get("available_date")
            ))
    
    return result
            