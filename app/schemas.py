from pydantic import BaseModel
from typing import Optional,Literal

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
        

TaskStatus = Literal['todo','in_progress','done']

class TaskBase(BaseModel):
    name: str
    status: TaskStatus = 'todo'
    order: int = 0
    group_id: Optional[int] = None
    description: Optional[str] = None
    
class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[TaskStatus] = None
    order: Optional[int] = None
    group_id: Optional[int] = None
    description: Optional[str] = None
    
class TaskRead(TaskBase):
    id: int
    class Config:
        from_attributes = True