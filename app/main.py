from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cadastrar-produto", response_model=schemas.Inventory)
def create_user(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    inventory = crud.get_inventory_by_id(db, id=inventory.id)
    if inventory:
        raise HTTPException(status_code=400, detail="Este produto já existe, tente atualiza-lo")
    return crud.create_inventory(db=db, inventory=inventory)