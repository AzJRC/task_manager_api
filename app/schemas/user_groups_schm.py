import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


class CreateUserGroup(BaseModel): #Schema of model UserGroupsTable to create a user group
    group_name: str
    group_description: Optional[str] = None


class ReturnCreatedUserGroup(BaseModel): #Schema of model UserGroupsTable for recently created user group
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime


class GetGroupMember(BaseModel):
    username: str = None
    role: str = None

class ReturnUserGroups(BaseModel):
    id: int
    group_name: str
    group_description: Optional[str]
    group_creation: datetime.datetime
    members_list: List[GetGroupMember]


class CreateUserGroupMember(BaseModel):
    member_id: int
    member_role: int
