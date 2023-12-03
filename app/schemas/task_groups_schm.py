import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


# Body models
class CreateTaskGroup(BaseModel):
    group_name: str
    group_description: Optional[str] = None


class assignTaskToTaskGroup(BaseModel):
    group_id: Optional[int] = None
    group_owner_id: Optional[int] = None
    group_name: Optional[str] = None


# Response models
class ReturnCreatedTaskGroup(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime

class GetAssignedTask(BaseModel):
    id: int
    title: str

class returnTaskGroup(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime
    tasks: List[GetAssignedTask]

    class Config:
        from_attributes: True