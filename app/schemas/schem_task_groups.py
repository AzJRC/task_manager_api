import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


# In-code schemas (get)

class GetAssignedTask(BaseModel):
    id: int
    title: str


# Request schemas (create/update/asssign)

class CreateTaskGroup(BaseModel):
    group_name: str
    group_description: Optional[str] = None


class UpdateTaskGroup(BaseModel):
    group_name: str
    group_description: Optional[str] = None
    

# Response schemas (return)

class ReturnCreatedTaskGroup(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime

class returnTaskGroup(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime
    tasks: List[GetAssignedTask]

    class Config:
        from_attributes: True