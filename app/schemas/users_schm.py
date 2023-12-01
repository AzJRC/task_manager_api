import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes: True


class GetUser(BaseModel):
    username: str
    email: EmailStr 
    user_state: bool

    class Config:
        from_attributes: True


class GetCurrentUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    user_creation: datetime.datetime
    valid_email: bool
    user_state: bool

    class Config:
        from_attributes: True


class ReturnUserDetails(BaseModel):
    operation: str
    user_details: GetUser

    class Config:
        from_attributes: True


