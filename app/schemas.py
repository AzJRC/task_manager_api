import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

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


# Task schemas

class returnTaskOwner(BaseModel): # Schema of model UsersTable
    username: str

class createTask(BaseModel): # Schema of model TasksTable
    title: str
    description: Optional[str] = None

class returnTask(BaseModel): # Schema of model TasksTable
    id: int
    title: str
    description: str
    task_creation: datetime.datetime
    task_owner: returnTaskOwner

class returnUserTask(BaseModel): # Schema of model TasksTable
    id: int
    title: str
    description: str
    task_creation: datetime.datetime

    class Config:
        from_attributes: True

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
    