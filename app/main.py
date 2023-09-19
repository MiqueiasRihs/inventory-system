from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

from typing import List

import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cadastrar-produto", response_model=List[schemas.Inventory])
def register_product(products: List[schemas.InventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if inventory:
            raise HTTPException(status_code=400, detail=f"O produto com ID {product.id} já existe, tente atualizá-lo")
        
        created_product = crud.create_inventory(db=db, inventory=product)
        created_products.append(created_product)
    
    return created_products


@app.put("/atualizar-produto", response_model=schemas.Inventory)
def update_product_inventory(product: schemas.InventoryCreate, db: Session = Depends(get_db)):
    inventory = crud.get_inventory_by_id(db, id=product.id)
    if not inventory:
        raise HTTPException(status_code=400, detail="Este produto não existe, tente cria-lo antes")
    return crud.update_inventory_quantity(db, product.id, product.quantity, product.name)

