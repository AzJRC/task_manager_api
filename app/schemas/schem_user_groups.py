import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field


# In-code schemas (get)

class GetGroupMember(BaseModel):
    username: str 
    role: str

# Request schemas (create/update/asssign)

class CreateUserGroup(BaseModel): 
    group_name: str
    group_description: Optional[str] = None


class CreateUserGroupMember(BaseModel):
    member_id: int
    member_role: int = Field(..., ge=1, le=4)


# Response schemas (return)

class ReturnCreatedUserGroup(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime


class ReturnUserGroups(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime
    members_list: List[GetGroupMember]

    class Config:
        from_attributes: True

