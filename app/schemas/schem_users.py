import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr


# In-code schemas (get)

class GetUser(BaseModel):
    id: int
    username: str
    email: EmailStr 
    user_state: bool

    class Config:
        from_attributes: True


# Request schemas (create/update/asssign)

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes: True

# Response schemas (return)

class ReturnCurrentUser(BaseModel):
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








