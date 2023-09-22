from sqlalchemy import Column, ForeignKey, Integer, String, Date

from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    quantity = Column(Integer, default=0, index=True)


class FutureInventory(Base):
    __tablename__ = "future_inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    quantity = Column(Integer, default=0)
    available_date = Column(Date, index=True)


class ReservationInventory(Base):
    __tablename__ = "reservation_inventory"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    quantity = Column(Integer, default=0, index=True)
    expiration_date = Column(Date, index=True, nullable=True)
    status = Column(String, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))


    