import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr

# In-code schemas (get)


# Request schemas (create/update/asssign)

class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None


# Response schemas (return)

class ReturnTaskOwner(BaseModel): 
    username: str


class ReturnTask(BaseModel):
    id: int
    title: str
    description: str
    task_creation: datetime.datetime
    task_owner: ReturnTaskOwner


class ReturnUserTask(BaseModel):
    id: int
    title: str
    description: str
    task_creation: datetime.datetime

    class Config:
        from_attributes: True

