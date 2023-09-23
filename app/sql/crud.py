from sqlalchemy.orm import Session

from . import models, schemas
from typing import Union

from datetime import date


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


def create_inventory_reservation(db: Session, product: schemas.ReservationInventoryCreate, inventory_id: int):
    db_inventory = models.ReservationInventory(
        quantity=product.quantity,
        expiration_date=product.expiration_date,
        status=product.status,
        inventory_id=inventory_id,
    )
    
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def update_inventory_quantity(db: Session, inventory_id: int, new_quantity: int):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()

    if db_inventory:
        db_inventory.quantity = new_quantity
        db.commit()
        db.refresh(db_inventory)
        return db_inventory

    return

def update_future_inventory(db: Session, inventory_id: int, product: schemas.FutureInventoryUpdate):
    db_inventory = db.query(models.FutureInventory).filter(models.FutureInventory.id == inventory_id).first()

    if db_inventory:
        db_inventory.quantity = product.quantity if product.quantity else db_inventory.quantity
        db_inventory.available_date = product.available_date if product.available_date else db_inventory.available_date
        db.commit()
        db.refresh(db_inventory)
        return db_inventory

    return


def get_inventory_by_id(db: Session, id: int):
    return db.query(models.Inventory).filter(models.Inventory.id == id).first()


def get_future_inventory_by_id(db: Session, id: int):
    return db.query(models.FutureInventory).filter(models.FutureInventory.id == id).first()


def get_reservation_inventory_by_id(db: Session, id: int):
    return db.query(models.ReservationInventory).filter(models.ReservationInventory.id == id).first()