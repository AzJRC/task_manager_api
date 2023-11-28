from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, database
from .auth import ALGORITHM, SECRET_KEY

# current user utilities

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user = db.query(models.UsersTable).filter(models.UsersTable.username == username).one_or_none()
    if user is None:
        raise credentials_exception
    return user


# password hashing

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# utils for tasks

def get_title_standard(title: str):
    standarized_title = title.replace("_", " ")
    return standarized_title