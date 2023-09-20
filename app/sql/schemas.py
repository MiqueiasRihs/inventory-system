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

class FutureInventory(FutureInventoryBase):
    class Config:
        orm_mode = True