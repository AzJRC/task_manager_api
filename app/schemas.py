import datetime
from typing import Optional
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

# User schemas

class getUser(BaseModel):
    username: str
    email: EmailStr
    state: Optional[str] = "active"

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
    creation: datetime.datetime
    valid_email: bool
    user_state: bool

    class Config:
        from_attributes: True
    