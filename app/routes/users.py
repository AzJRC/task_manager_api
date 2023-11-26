from typing import Annotated
from psycopg2 import IntegrityError
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..auth import oauth2_scheme
from ..utils import get_current_user, get_password_hash
from .. import models, schemas, database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.returnUser)
def create_user(user: schemas.createUser, db: Session = Depends(database.get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = models.UsersTable(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User already exists.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        db.refresh(new_user)
        user_details = schemas.userDetails(username=new_user.username, email=new_user.email)
        return schemas.returnUser(operation="successful", user_details=user_details)


@router.get("/me/", response_model=schemas.returnCurrentUser)
def get_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    user = get_current_user(token=token, db=db) #This already handles inexistent user exceptions. No need for try except.
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    current_user = get_current_user(token=token, db=db) #This already handles inexistent user exceptions. No need for try except.
    db.query(models.UsersTable).filter(models.UsersTable.id == current_user.id).delete()
    db.commit()
    