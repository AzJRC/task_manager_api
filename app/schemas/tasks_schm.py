import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None


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