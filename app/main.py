from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.schemas import InventoryCreate
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