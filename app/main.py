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


@app.put("/atualizar-produto", response_model=List[schemas.Inventory])
def update_product_inventory(products: List[schemas.InventoryCreate], db: Session = Depends(get_db)):
    updated_products = []
    
    for product in products:
        inventory = crud.get_inventory_by_id(db, id=product.id)
        if not inventory:
            raise HTTPException(status_code=400, detail="Este produto não existe, tente cria-lo antes")

        else:
            updated_product = crud.update_inventory_quantity(db, product.id, product.quantity, product.name) 
            updated_products.append(updated_product)
    
    return updated_products


@app.post("/cadastrar-estoque-futuro", response_model=List[schemas.FutureInventory])
def register_future_inventory(products: List[schemas.FutureInventoryCreate], db: Session = Depends(get_db)):
    created_products = []
    
    for product in products:
        future_inventory = crud.get_future_inventory_by_id(db, id=product.id)

        if future_inventory:
            raise HTTPException(status_code=400, detail=f"O estoque futuro do produto com ID {product.id} já existe, tente atualizá-lo")
            
        created_product = crud.create_future_inventory(db=db, product=product)
        created_products.append(created_product)

    return created_products