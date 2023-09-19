from typing import Union

from pydantic import BaseModel, validator


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