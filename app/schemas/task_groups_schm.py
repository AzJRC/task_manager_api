import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr

class CreateTaskGroup(BaseModel):
    group_name: str
    group_description: Optional[str] = None


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