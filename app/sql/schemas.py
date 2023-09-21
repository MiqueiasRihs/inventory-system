from typing import Union

from pydantic import BaseModel, validator

from datetime import datetime, date


###### Inventory ######
class InventoryBase(BaseModel):
    id: int
    quantity: int
    name: Union[str, None] = None

class InventoryCreate(InventoryBase):
    @validator('quantity')
    def validate_quantity(cls, value):
        if value < 0:
            raise ValueError('A quantidade não pode ser negativa')
        return value

class Inventory(InventoryBase):
    class Config:
        orm_mode = True
        
        
###### FutureInventory ######
class UpdateProductQuantity(BaseModel):
    quantity: int

    @validator('quantity')
    def validate_quantity(cls, value):
        if value < 0:
            raise ValueError('A quantidade não pode ser negativa')
        return value


###### FutureInventory ######
class FutureInventoryBase(BaseModel):
    id: int
    quantity: int
    available_date: Union[str, date]
    name: Union[str, None] = None
    
class FutureInventoryCreate(FutureInventoryBase):

    @validator('available_date')
    def validate_available_date(cls, value):
        try:
            date_obj = datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError('Data de disponibilidade inválida')
    
        return str(date_obj)

class   FutureInventory(FutureInventoryBase):
    class Config:
        orm_mode = True
        
        
###### ReservationInventory ######
class ReservationInventoryBase(BaseModel):
    id: int
    status: str
    quantity: int
    expiration_date: Union[str, date]

class ReservationInventoryCreate(ReservationInventoryBase):

    @validator('expiration_date')
    def validate_expiration_date(cls, value):
        try:
            date_obj = datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError('Data de expiração inválida')
    
        return str(date_obj)

class ReservationInventory(ReservationInventoryBase):
    class Config:
        orm_mode = True
        
        
class Consult(BaseModel):
    id: int
    quantity: int

class ConsultResulCreate(Consult):
    id: int
    quantity: int

class ConsultResult(Consult):
    available_inventory_quantity: int
    available: bool
    inventory_available_date: Union[str, None] = None