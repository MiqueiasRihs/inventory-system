from typing import Union

from pydantic import BaseModel


class InventoryBase(BaseModel):
    id: int
    quantity: int
    name: Union[str, None] = None

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    
    class Config:
        orm_mode = True