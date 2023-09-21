from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.constants import inventory_reservation_difference, future_inventory_difference
from sql.database import SessionLocal, engine

from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/estoque/estoque-fisico", response_model=List[schemas.Inventory])
def register_product(products: List[schemas.InventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if inventory:
            raise HTTPException(status_code=400, detail=f"O produto com ID {product.id} já existe, tente atualizá-lo")
        
        created_product = crud.create_inventory(db=db, inventory=product)
        created_products.append(created_product)
    
    return created_products


@app.put("/estoque/estoque-fisico/{product_id}", response_model=schemas.Inventory)
def update_product_inventory(product_id: int, product: schemas.UpdateProductQuantity, db: Session = Depends(get_db)):
    inventory_prod = crud.get_inventory_by_id(db, id=product_id)
    if not inventory_prod:
        raise HTTPException(status_code=400, detail="Este produto não existe, tente cria-lo antes")

    return crud.update_inventory_quantity(db, inventory_prod.id, product.quantity)


@app.post("/estoque/estoque-futuro", response_model=List[schemas.FutureInventory])
def register_future_inventory(products: List[schemas.FutureInventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        future_inventory = crud.get_future_inventory_by_id(db, id=product.id)

        if future_inventory:
            raise HTTPException(status_code=400, detail=f"O estoque futuro do produto com ID {product.id} já existe, tente atualizá-lo")
            
        created_product = crud.create_future_inventory(db=db, product=product)
        created_products.append(created_product)

    return created_products


@app.post("/estoque/reserva", response_model=List[schemas.ReservationInventory])
def inventory_reservation(products: List[schemas.ReservationInventoryCreate], db: Session = Depends(get_db)):
    reservations_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if not inventory:
            raise HTTPException(status_code=400, detail=f"Não é possivel realizar a reserva pois o produto com ID {product.id} não existe")

        reservation_result = inventory_reservation_difference(db, product.id)
        if reservation_result and product.quantity > reservation_result.get("difference", 0):
            raise HTTPException(status_code=400, detail=f"Não é possivel reservar pois não existe estoque suficiente para o produto com ID {product.id}, o estoque atual é {difference['difference']}")
            
        created_product = crud.create_inventory_reservation(db=db, product=product, inventory_id=inventory.id)
        reservations_products.append(created_product)

    return reservations_products


@app.post("/estoque/consulta/{strategy}", response_model=List[schemas.ConsultResult])
def consult_inventory(strategy: str, products: List[schemas.Consult], db: Session = Depends(get_db)):
    products_result = []

    for product in products:
        if strategy == "estoque-fisico":
            reservation_result = inventory_reservation_difference(db, product.id)
            products_result.append(schemas.ConsultResult(
                id=product.id,
                quantity=product.quantity,
                available_inventory_quantity=reservation_result.get("difference", 0),
                available=product.quantity <= reservation_result.get("difference", 0)
            ))
            
        elif strategy == "estoque-futuro":
            future_result = future_inventory_difference(db, product.id)
            products_result.append(schemas.ConsultResultFutureInventory(
                id=product.id,
                quantity=product.quantity,
                available_inventory_quantity=future_result.get("difference", 0),
                available=product.quantity <= future_result.get("difference", 0),
                inventory_available_date=future_result.get("inventory_available_date", None)
            ))
            
    return products_result
            
