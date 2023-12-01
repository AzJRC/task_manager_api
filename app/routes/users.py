from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_users
from app.utils import get_current_user
from app.database import get_db
from app.schemas import users_schm

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=users_schm.ReturnUserDetails)
def create_user_endpoint(user: users_schm.CreateUser, db: Session = Depends(get_db)):
    return crud_users.create_user(db, user)


@router.get("/me/", response_model=users_schm.GetCurrentUser)
def get_user_endpoint(user: users_schm.GetUser = Depends(get_current_user)):
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user: users_schm.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    crud_users.delete_user(db, user.id)
    