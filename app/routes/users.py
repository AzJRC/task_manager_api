from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_users
from ..utils import get_current_user
from ..database import get_db
from .. import schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.returnUser)
def create_user_endpoint(user: schemas.createUser, db: Session = Depends(get_db)):
    return crud_users.create_user(db, user)


@router.get("/me/", response_model=schemas.returnFullCurrentUserInformation)
def get_user_endpoint(user: schemas.returnFullCurrentUserInformation = Depends(get_current_user)):
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    crud_users.delete_user(db, user.id)
    