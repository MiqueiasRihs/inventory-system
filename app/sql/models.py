from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    quantity = Column(Integer, default=0, index=True)


# Todo:
# Inventory é uma foreing key de FutureInventory, a ideia é que caso o Inventory não exista
# ao criar um FutureInventory crie um inventory zerado
class FutureInventory(Base):
    __tablename__ = "future_inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    quantity = Column(Integer, default=0)
    available_date = Column(Date, index=True, nullable=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))


# Todo: 
# Ao reservar um produto o Inventory precisa ser atualizado o valor
class InventoryReservation(Base):
    __tablename__ = "inventory_reservation"
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=0, index=True)
    expiration_date = Column(Date, index=True, nullable=True)
    status = Column(String, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))


    