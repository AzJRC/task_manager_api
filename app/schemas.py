import datetime
from typing import Any, ForwardRef, List, Optional
from pydantic import BaseModel, EmailStr
from .database import Base

from app.models import UserGroupsTable, UsersTable

# Token schemas (For login)

class returnToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes: True


class getTokenData(BaseModel):
    username: str | None = None

    class Config:
        from_attributes: True


# User groups schemas

class returnUserGroupInformation(BaseModel): #Schema of model UserGroupsTable for returnFullCurrentUserInformation schema
    id: int
    group_name: str
    group_creation: datetime.datetime


# Task group schemas

class returnTaskGroupInformation(BaseModel): # Schema of model TaskGroupsTable for returnFullCurrentUserInformation schema
    id: int
    group_name: str
    group_creation: datetime.datetime



# User schemas

class getUser(BaseModel):
    username: str
    email: EmailStr 
    state: str

    class Config:
        from_attributes: True


class createUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes: True


class userDetails(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes: True


class returnUser(BaseModel):
    operation: str
    user_details: userDetails

    class Config:
        from_attributes: True


class returnCurrentUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    user_creation: datetime.datetime
    valid_email: bool
    user_state: bool

    class Config:
        from_attributes: True


class returnFullCurrentUserInformation(returnCurrentUser):
    owned_user_groups: Optional[List[returnUserGroupInformation]] = None
    owned_task_groups: Optional[List[returnTaskGroupInformation]] = None
    class Config:
        from_attributes: True
    