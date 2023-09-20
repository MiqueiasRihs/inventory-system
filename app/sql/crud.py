from sqlalchemy.orm import Session

from . import models, schemas


def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(
        id=inventory.id,
        quantity=inventory.quantity,
        name=inventory.name if inventory.name else None
    )
    
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory
    

def get_inventory_by_id(db: Session, id: int):
    return db.query(models.Inventory).filter(models.Inventory.id == id).first()


def get_future_inventory_by_id(db: Session, id: int):
    return db.query(models.FutureInventory).filter(models.FutureInventory.id == id).first()


def update_inventory_quantity(db: Session, inventory_id: int, new_quantity: int, name: str):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()

    if db_inventory:
        if name:
            db_inventory.name = name
        
        db_inventory.quantity = new_quantity
        db.commit()
        db.refresh(db_inventory)
        return db_inventory

    return


def create_future_inventory(db: Session, product: schemas.FutureInventoryCreate):
    db_inventory = models.FutureInventory(
        id=product.id,
        quantity=product.quantity,
        available_date=product.available_date,
        name=product.name if product.name else None
    )
    
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory