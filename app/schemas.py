from pydantic import BaseModel
from typing import Optional

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name : Optional[str] = None
    description: Optional[str] = None
    
class GroupRead(GroupBase):
    id: int
    class Config:
        from_attributes = True